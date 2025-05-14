
from datetime import datetime
import json
from typing import Optional
from nicegui import ui, app
import pandas as pd
import pytz
import logging
from components import dialogs, tables, cards
from dao.course_dao import CourseDao, CourseStudentsDao, StudentInSeatsDao, query_student_in_seat
from dao.classroom_dao import \
    ClassRoomSeatsDao, \
    get_class_room_seats_by_classes_id
from dao.h03_event_dao import H03EventDao
from dao.t1_attr_dao import T1AttrDao
from utils import global_vars

logger = logging.getLogger(__name__)

def show_course_detail_page(course_id: int) -> None:
    if 'course_dao' not in app.storage.user:
        app.storage.user['course_dao'] = CourseDao()
    app.storage.user['course_dao'].id = course_id
    status, result = app.storage.user['course_dao'].get_course_by_id()
    if status != 200:
        ui.notify(f'获取课程信息失败, {result}')
        return
    with ui.row().classes('w-full h-[80px] px-[20px] mt-0 items-center place-content-between') \
        .style('background-color: #FFFFFF !important; border-radius: 10px;'):
        with ui.row().classes('h-full items-center gap-0'):
            ui.label('XX中学智能学习教室').classes('text-[20px] text-[#333333]') \
                .bind_text_from(global_vars.get_class_room(), 'name')
            ui.label('三(2)班').classes('text-[20px] ml-2 text-[#333333]') \
                .bind_text_from(app.storage.user['course_dao'], 'classes')
            ui.label('代课老师: 王老师').classes('ml-10 text-[20px] text-[#888888]') \
                .bind_text_from(app.storage.user['course_dao'], 'teacher')
        with ui.row().classes('h-full items-center'):
            ui.button('批量导入', icon='img:/static/images/import@2x.png', on_click=import_students) \
                .classes('w-25 rounded-md text-white') \
                .style('background-color: #27CACA !important; border-radius: 6px;')
            ui.button('添加学生', icon='img:/static/images/add@2x.png', on_click=add_students) \
                .classes('w-25 rounded-md text-white') \
                .style('background-color: #65B6FF !important; border-radius: 6px;')
            
    with ui.card().classes('w-full mt-2 no-shadow') \
        .props('borderless') \
        .style('padding: 15px; background-color: #FFFFFF !important; border-radius: 10px;'):
        app.storage.client['student_card_column'] = ui.column().classes('w-full items-center place-content-start')
        refresh_student_seat_card()
        with ui.row().classes('w-full gap-0 mt-5 item-center place-content-start'):
            ui.icon('square').classes('text-[#27CACA] w-4 h-4').style('border-radius: 2px;')
            ui.label('深度专注').classes('text-[14px] font-bold text-[#333333]')
            ui.icon('square').classes('text-[#FFC100] ml-2 w-4 h-4').style('border-radius: 2px;')
            ui.label('中度专注').classes('text-[14px] font-bold text-[#333333]')
            ui.icon('square').classes('text-[#EF4444] ml-2 w-4 h-4').style('border-radius: 2px;')
            ui.label('浅度专注').classes('text-[14px] font-bold text-[#333333]')
            ui.icon('img:/static/images/on_line.png').classes('ml-5 w-4 h-4')
            ui.label('设备在线').classes('text-[14px] font-bold text-[#333333]')
            ui.icon('img:/static/images/off_line.png').classes('ml-2 w-4 h-4')
            ui.label('设备离线').classes('text-[14px] font-bold text-[#333333]')
        with ui.card().classes('w-full p-5 mt-2 no-shadow gap-0') \
            .props('borderless') \
            .style('padding: 15px; background-color: #EFF3FC !important; border-radius: 10px;'):
                with ui.row().classes('w-full place-content-start'):
                    ui.label('学习状况:').classes('text-[16px] text-[#333333]')
                with ui.scroll_area().classes('w-full h-[200px] gap-0'):
                    with ui.column().classes('w-full place-content-start gap-0') as study_status_column:
                        app.storage.client['study_status_column'] = study_status_column
                        with ui.row().classes('w-full'):
                            ui.label('10:46:05').classes('text-[14px] text-[#333333]')
                            ui.label('刘婷婷同学专注度下降到中度专注').classes('text-[14px] text-[#333333]')
                    study_status_column.clear()
        with ui.row().classes('w-full mt-2 items-center place-content-end'):
            app.storage.client['start_course_button'] = ui.button('开始上课', color=None, on_click=start_course) \
                .props('flat') \
                .classes('w-[120px] text-[16px] text-white font-[400]') \
                .style('background-color: #65B6FF !important; border-radius: 10px')
            app.storage.client['end_course_button'] = ui.button('结束上课', color=None, on_click=end_course) \
                .props('flat') \
                .classes('w-[120px] text-[16px] text-[#FF4D4D] font-[400]') \
                .style('background-color: rgba(255,77,77,0.39) !important; border-radius: 10px')
            if app.storage.user['course_dao'].status == 1:
                app.storage.client['start_course_button'].set_visibility(False)
                app.storage.client['end_course_button'].set_visibility(True)
            elif app.storage.user['course_dao'].status == 2:
                app.storage.client['start_course_button'].set_visibility(False)
                app.storage.client['end_course_button'].set_visibility(False)
            else:
                app.storage.client['start_course_button'].set_visibility(True)
                app.storage.client['end_course_button'].set_visibility(False)
            

#
# @description: 刷新学生座位卡片
# @param {*}
# @return {*}
#
def refresh_student_seat_card():
    if 'student_card_column' in app.storage.client:
        status, result = query_student_in_seat(global_vars.get_class_room().id, app.storage.user['course_dao'].id)
        if status != 200:
            ui.notify(f'查询学生座位失败: {result}')
            return
        app.storage.client['student_card_column'].clear()
        with app.storage.client['student_card_column']:
            for i in range(0, global_vars.get_class_room().seat_row):
                with ui.row().classes('w-full items-center place-content-evenly'):
                    row_label = chr(65 + i)  # Convert row index to letter (A, B, C, ...)
                    ui.label(f'{row_label}排').classes('text-[14px] font-bold text-[#333333]')
                    for j in range(0, global_vars.get_class_room().seat_col):
                        item = result[i * global_vars.get_class_room().seat_col + j]
                        if isinstance(item, StudentInSeatsDao):
                            obj: StudentInSeatsDao = item
                            if obj.mac is not None and obj.mac != "":
                                students_seat_subscribe(mac=obj.mac)
                            students = {'seat_number': obj.seat_no, 'mac': obj.mac, 'name': obj.name, 'status': obj.is_online}
                            cards.student_in_seat_card(students)
        if 'check_event_timer' in app.storage.client:
            app.storage.client['check_event_timer'].cancel()
        app.storage.client['check_event_timer'] = ui.timer(0.1, cards.check_student_status_queue)
        app.storage.client['check_event_timer'].activate()

#
# @description: 更新学生学习状态列表
# @param {str} name 学生姓名
# @param {int} concentration 学生专注度
# @param {bool} up 是否上升
# @return {*}
def update_study_status_column(name: str, concentration: int, up: int) -> None:
    if name is None or name == "" or concentration is None or concentration == 0:
        return
    if 'study_status_column' in app.storage.client:
        with app.storage.client['study_status_column']:
            with ui.row().classes('w-full'):
                if up == 1:
                    upstr = '上升至'
                elif up == -1:
                    upstr = '下降至'
                else:
                    upstr = '保持在'
                if concentration > 0 and up != 0:
                    ui.label(datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%H:%M:%S')).classes('text-[14px] text-[#333333]')
                    if concentration == 1: # 低专注
                        ui.label(f'{name}同学专注度{upstr}低度专注').classes('text-[14px] text-[#333333]')
                    elif concentration == 2: # 中专注
                        ui.label(f'{name}同学专注度{upstr}中度专注').classes('text-[14px] text-[#333333]')
                    elif concentration == 3: # 高专注
                        ui.label(f'{name}同学专注度{upstr}高度专注').classes('text-[14px] text-[#333333]')
#
# @description: 订阅学生座位消息
# @param {str} mac 学生的mac地址
# @return {*}
#
def students_seat_subscribe(mac: str) -> None:
    def online_msg(client, userdata, msg):
        jsobj = json.loads(msg.payload)
        cards.update_online_student_in_card(mac, jsobj['online'])
    global_vars.subscribe_online_topic(mac, online_msg)
    def event_msg(client, userdata, msg):
        logger.info(f'event_msg: {msg.payload}')
        jsobj = json.loads(msg.payload)
        event_dao = H03EventDao()
        event_dao.from_json(jsobj)
        cards.update_online_student_in_card(mac, 1)
        cards.update_concentration_student_in_card(event_dao.mac, event_dao.focus_status, update_study_status_column)
    global_vars.subscribe_event_topic(mac, event_msg)
    def attr_msg(client, userdata, msg):
        logger.info(f'attr_msg: {msg.payload}')
        jsobj = json.loads(msg.payload)
        attr_dao = T1AttrDao()
        attr_dao.from_json(jsobj)
        cards.update_online_student_in_card(mac, 1)
        cards.update_concentration_student_in_card(attr_dao.mac, attr_dao.focus_status, update_study_status_column)
    global_vars.subscribe_attr_topic(mac, attr_msg)
#
# @description: 批量导入学生
# @param {*}
# @return {*}
def import_students():
    status, seats_list = get_class_room_seats_by_classes_id(global_vars.get_class_room().id)
    if status != 200:
        ui.notify(f'查询教室座位失败: {seats_list}')
        return
    seat_dict = {}
    if isinstance(seats_list, list) and all(isinstance(item, ClassRoomSeatsDao) for item in seats_list):
        seat_dict = {item.seat_no: item.id for item in seats_list}
    def handle_upload(event):
        # event.content 是文件的二进制内容
        import io
        file_content = io.BytesIO(event.content.read())
        df = pd.read_excel(file_content)
        for index, row in df.iterrows():
            # 处理每一行数据
            seat_no = row['seat_no']
            name = row['name']
            gender = row['gender']
            students_dao = CourseStudentsDao( \
                class_room_id=global_vars.get_class_room().id, \
                seat_id=seat_dict.get(seat_no, 0), \
                course_id=app.storage.user['course_dao'].id, \
                name = name, \
                gender=0 if gender == '男' else 1, \
            )
            status, result = students_dao.add_students()
            if status is False:
                ui.notify(f'导入学生失败: {result}')
                upload.reset()
                return
        ui.notify('导入学生成功')
        refresh_student_seat_card()
        dialog.close()

    with ui.dialog().props('persistent') as dialog, ui.card().classes('w-1/3 h-1/3') \
        .style('background-color: #FFFFFF !important; border-radius: 10px;'):
        with ui.row().classes('size-full mt-5 place-content-between'):
            upload = ui.upload(label="请选择批量上传文件", on_upload=handle_upload) \
                .props('flat accept=".xls,.xlsx"') \
                .classes('size-full')
        with ui.row().classes('w-full place-content-end'):
            ui.button('关闭', color=None, on_click=dialog.close) \
                .props('flat') \
                .classes('w-[120px] text-[16px] text-[#888888] font-[400]') \
                .style('background-color: #FFFFFF !important;border-radius: 10px;border: 1px solid #888888;')
            
    dialog.open()

#
# @description: 添加学生
# @param {*}
# 
def add_students():
    def on_ok(seat_no, name, gender):
        status, seats_list = get_class_room_seats_by_classes_id(global_vars.get_class_room().id)
        if status != 200:
            ui.notify(f'查询教室座位失败: {seats_list}')
            return
        seat_dict = {}
        if isinstance(seats_list, list) and all(isinstance(item, ClassRoomSeatsDao) for item in seats_list):
            seat_dict = {item.seat_no: item.id for item in seats_list}
        students_dao = CourseStudentsDao( \
            class_room_id=global_vars.get_class_room().id, \
            seat_id=seat_dict.get(seat_no, 0), \
            course_id=app.storage.user['course_dao'].id, \
            name = name, \
            gender=0 if gender == '男' else 1, \
        )
        status, result = students_dao.add_students()
        if status is False:
            ui.notify(f'添加学生失败: {result}')
            return
        else:
            ui.notify('添加学生成功')
            refresh_student_seat_card()
            add_dialog.close()
    add_dialog = dialogs.show_add_student_dialog(app.storage.user['course_dao'].id, on_ok)

#
# @description: 开始上课
# @param {*}
# @return {*}
#
def start_course():
    if app.storage.user['course_dao'].status > 0:
        ui.notify('只有未开始的课程才能开始上课')
        return
    app.storage.user['course_dao'].begin_time = datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')
    app.storage.user['course_dao'].status = 1
    status, result = app.storage.user['course_dao'].update_course()
    if status:
        if 'start_course_button' in app.storage.client:
            app.storage.client['start_course_button'].set_visibility(False)
        if 'end_course_button' in app.storage.client:
            app.storage.client['end_course_button'].set_visibility(True)
    else:
        ui.notify(f'开始课程失败: {result}')
#
# @description: 结束上课
# @param {*}
# @return {*}
#
def end_course():
    if app.storage.user['course_dao'].status != 1:
        ui.notify('只有进行中的课程才能结束上课')
        return
    if app.storage.user['course_dao'].status == 2:
        ui.notify('课程已经结束')
        return
    app.storage.user['course_dao'].end_time = datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')
    app.storage.user['course_dao'].status = 2
    if app.storage.user['course_dao'].begin_time is not None and app.storage.user['course_dao'].end_time is not None:
        start = datetime.strptime(app.storage.user['course_dao'].begin_time, '%Y-%m-%d %H:%M:%S')
        end = datetime.strptime(app.storage.user['course_dao'].end_time, '%Y-%m-%d %H:%M:%S')
        app.storage.user['course_dao'].duration = (end - start).total_seconds() / 60
    status, result = app.storage.user['course_dao'].update_course()
    if status:
        ui.notify('结束课程成功，请返回课程列表')
    else:
        ui.notify(f'结束课程失败: {result}')



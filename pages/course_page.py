'''
Author: liguoqiang
Date: 2025-03-13 11:31:42
LastEditors: liguoqiang
LastEditTime: 2025-03-19 14:21:03
Description: 
'''
from dataclasses import dataclass
from nicegui import ui,app,events
from components import tables, inputs, dialogs
from pages.course_detail_page import show_course_detail_page
from pages.course_report_page import show_course_report_page
from pages.person_report_page import show_person_report_page
import navigation
from dao.course_dao import CourseDao, get_all_courses
from typing import Optional

@dataclass
class SearchCondition:
    class_name: str = ""
    subject_name: str = ""
    teacher_name: str = ""
    begin_time: str = ""
    select_status: str = ""
search_condition = SearchCondition()

#
# @description: 显示课程页面
# @return {*}
#
def show_course_page() -> None:
    with ui.row().classes('w-full h-[80px] px-[20px] mt-0 place-content-between gap-0') \
        .style('background-color: #FFFFFF !important; border-radius: 10px;'):
        with ui.row().classes('h-full items-center'):
            class_input = inputs.input_search_w40('班级', on_search)
            class_input.bind_value_to(search_condition, 'class_name')
            subject_input = inputs.input_search_w40('科目', on_search)
            subject_input.bind_value_to(search_condition, 'subject_name')
            teacher_input = inputs.input_search_w40('教师姓名', on_search)
            teacher_input.bind_value_to(search_condition, 'teacher_name')
            start_time_input = inputs.date_input_w40('开始时间', on_search)
            start_time_input.bind_value_to(search_condition, 'begin_time')
            course_status = [
                '全部',
                '未开始',
                '进行中',
                '已结束'
            ]
            def on_search_status(value):
                on_search()
            status_select = inputs.selection_w40(course_status, course_status[0], on_search_status)
            status_select.bind_value_to(search_condition, 'select_status')
        with ui.row().classes('h-full items-center'):
            ui.button('批量删除', icon='img:/static/images/delete@2x.png', on_click=del_select_course) \
                .classes('w-25 rounded-md text-red') \
                .style('background-color: rgba(255,77,77,0.39) !important')
            ui.button('创建课程', icon='img:/static/images/add_course@2x.png', on_click=add_course) \
                .classes('w-25 rounded-md text-white') \
                .style('background-color: #65B6FF !important')
            
    table_rows: list[dict] = []
    course_table: Optional[ui.table] = tables.show_course_table(table_rows, show_course_detail, show_course_report, show_course_delete)
    app.storage.client['course_table'] = course_table
    on_search()

def on_search() -> None:
    status = -1
    match search_condition.select_status:
        case '未开始':
            status = 0
        case '进行中':
            status = 1
        case '已结束':
            status = 2
        case _:
            status = -1
    status, result = get_all_courses(search_condition.class_name, search_condition.subject_name, search_condition.teacher_name, search_condition.begin_time, status)
    if 'course_table' in app.storage.client:
        app.storage.client['course_table'].rows.clear()
        if status == 200:
            for item in result:
                app.storage.client['course_table'].add_row(item.__dict__)
        else:
            ui.notify(f'查询课程失败: {result}')
        app.storage.client['course_table'].update()

#
# @description: 显示课堂删除操作，由table组件触发
#
def show_course_delete(e: events.GenericEventArguments) -> None:
    id = e.args['id']
    del_course_by_ids([id])

#
# @description: 显示个人报告页面
# @param {events.GenericEventArguments} e 事件参数
# @return {*}
#         
def show_person_report(e: events.GenericEventArguments) -> None:
    course_id = e.args['course_id']
    id = e.args['id']
    def onback():
        show_course_report_by_id(course_id)
    navigation.navigation_course_person_report_page(course_id, id, onback)

#
# @description: 显示课堂报告,由table组件中触发
# @param {events.GenericEventArguments} e 事件参数
# @return {*}
#
def show_course_report(e: events.GenericEventArguments) -> None:
    id = e.args['id']
    show_course_report_by_id(id)
#
# @description: 显示课堂报告页面,根据课程ID触发
# @param {int} course_id 课程ID
# @return {*}
#
def show_course_report_by_id(course_id: int) -> None:
    def onback():
        navigation.navigation_course_page()
    navigation.navigation_course_report_page(course_id, onback, show_person_report)
#
#
# @description: 显示课堂监控页面
# @param {events.GenericEventArguments} e 事件参数
# @return {*}
#
def show_course_detail(e: events.GenericEventArguments) -> None:
    id = e.args['id']
    def onback():
        navigation.navigation_course_page()
    navigation.navigation_course_detail_page(id, onback)


#
# @description: 显示添加课堂对话框
# @return {*}
#
def add_course():
    course = CourseDao()
    with ui.dialog().props('persistent') as dialog, ui.card().classes('w-1/2 h-1/2') \
        .style('background-color: #FFFFFF !important; border-radius: 10px;'):
        ui.label('创建课堂').classes('w-full text-[20px] text-[#333333] font-medium')
        with ui.row().classes('w-full mt-5 place-content-between'):
            ui.label('班级').classes('w-full text-[16px] text-[#333333] font-medium')
            classes_ui = ui.input(placeholder='请输入班级') \
                .props('rounded-md outlined dense') \
                .classes('w-full self-center item-center ')
            classes_ui.bind_value_to(course, 'classes')
        with ui.row().classes('w-full place-content-between'):
            ui.label('科目').classes('w-full text-[16px] text-[#333333] font-medium')
            subject_ui = ui.input(placeholder='请输入科目') \
                .props('rounded-md outlined dense') \
                .classes('w-full self-center item-center ')
            subject_ui.bind_value_to(course, 'subject')
        with ui.row().classes('w-full place-content-between'):
            ui.label('任课老师').classes('w-full text-[16px] text-[#333333] font-medium')
            teacher_ui = ui.input(placeholder='请输入教师姓名') \
                .props('rounded-md outlined dense') \
                .classes('w-full self-center item-center ')
            teacher_ui.bind_value_to(course, 'teacher')
        with ui.row().classes('w-full place-content-end'):         
            ui.button('取消', color=None, on_click=dialog.close) \
                .props('flat') \
                .classes('w-[120px] text-[16px] text-[#888888] font-[400]') \
                .style('background-color: #FFFFFF !important;border-radius: 10px;border: 1px solid #888888;')
            def on_create_course():
                if course.classes == "" or course.subject == "" or course.teacher == "":
                    ui.notify('班级、科目和教师姓名不能为空')
                    return
                status, ret = course.add_course()
                if status is True:
                    ui.notify('添加课程成功')
                    if 'course_table' in app.storage.client:
                        app.storage.client['course_table'].add_row(course.__dict__)
                        app.storage.client['course_table'].update()
                    dialog.close()
                else:
                    ui.notify(f'添加课程失败: {ret}')
            ui.button('确定', color=None, on_click=on_create_course) \
                .props('flat') \
                .classes('w-[120px] text-[16px] text-white font-[400]') \
                .style('background-color: #65B6FF !important; border-radius: 10px')
    dialog.open()

#
# @description: 批量删除课程
# @return {*}
#
def del_select_course():
    if 'course_table' not in app.storage.client:
        return
    selection = app.storage.client['course_table'].selected
    ids = [item['id'] for item in selection]
    del_course_by_ids(ids)

def del_course_by_ids(ids: list[int]) -> None:
    if ids is None or len(ids) == 0:
        ui.notify('请选择要删除的课程')
        return
    def make_delete():
        course_dao = CourseDao()
        status, ret = course_dao.delete_course(ids)
        if status is True:
            ui.notify('删除课程成功')
            on_search()
        else:
            ui.notify(f'删除课程失败: {ret}')
        dialog.close()

    with ui.dialog().props('persistent') as dialog, ui.card() \
        .style('background-color: #FFFFFF !important; border-radius: 10px;'):
        ui.label('确认要进行删除操作?').classes('w-full text-[20px] text-[#333333] font-medium')
        with ui.row().classes('w-full place-content-end'):
            ui.button('取消', color=None, on_click=dialog.close) \
                .props('flat') \
                .classes('w-[120px] text-[16px] text-[#888888] font-[400]') \
                .style('background-color: #FFFFFF !important;border-radius: 10px;border: 1px solid #888888;')
            ui.button('确定', color=None, on_click=make_delete) \
                .props('flat') \
                .classes('w-[120px] text-[16px] text-white font-[400]') \
                .style('background-color: #65B6FF !important; border-radius: 10px')
    
    dialog.open()


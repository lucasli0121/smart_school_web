'''
Author: liguoqiang
Date: 2025-03-13 11:31:42
LastEditors: liguoqiang
LastEditTime: 2025-03-19 14:21:03
Description: 
'''
from nicegui import ui,events
from components import tables, inputs, dialogs

def show_course_page(tab_panel):
    with ui.row().classes('w-full items-center place-content-between'):
        with ui.row().classes('items-center place-content-start content-around'):
            class_input = inputs.input_search_w40('班级', on_search)
            subject_input = inputs.input_search_w40('科目', on_search)
            teacher_input = inputs.input_search_w40('教师姓名', on_search)
            start_time_input = inputs.date_input_w40('开始时间', on_search)
            course_status = [
                '全部',
                '未开始',
                '进行中',
                '已结束'
            ]
            status_select = inputs.selection_w40(course_status, lambda value: ui.notify(value))
        with ui.row().classes('items-center place-content-end'):
            ui.button('创建课程', icon='add', on_click=add_course)
            ui.button('批量删除', icon='delete', on_click=del_course).style('background-color: #ff0000 !important')
    table_rows = [
        {'id': 1, 'class': '一年级一班', 'subject': '数学', 'teacher': '张三', 'start_time': '2025-03-13 10:00:00', 'end_time': '2025-03-13 12:00:00', 'status': '0', 'student_roster': '张三, 李四', 'operation': ''},
        {'id': 2, 'class': '一年级二班', 'subject': '语文', 'teacher': '李四', 'start_time': '2025-03-13 10:00:00', 'end_time': '2025-03-13 12:00:00', 'status': '0', 'student_roster': '张三, 李四', 'operation': ''},
        {'id': 3, 'class': '一年级三班', 'subject': '英语', 'teacher': '王五', 'start_time': '2025-03-13 10:00:00', 'end_time': '2025-03-13 12:00:00', 'status': '1', 'student_roster': '张三, 李四', 'operation': ''},
        {'id': 4, 'class': '一年级四班', 'subject': '物理', 'teacher': '赵六', 'start_time': '2025-03-13 10:00:00', 'end_time': '2025-03-13 12:00:00', 'status': '2', 'student_roster': '张三, 李四', 'operation': ''},
        {'id': 5, 'class': '一年级五班', 'subject': '化学', 'teacher': '孙七', 'start_time': '2025-03-13 10:00:00', 'end_time': '2025-03-13 12:00:00', 'status': '2', 'student_roster': '张三, 李四', 'operation': ''},
        {'id': 6, 'class': '一年级六班', 'subject': '生物', 'teacher': '周八', 'start_time': '2025-03-13 10:00:00', 'end_time': '2025-03-13 12:00:00', 'status': '0', 'student_roster': '张三, 李四', 'operation': ''},
    ]
    tables.show_course_table(table_rows, show_course_monitor, show_course_report, show_course_delete)

def on_search():
    ui.notify('search')

def show_course_report(e: events.GenericEventArguments) -> None:
    id = e.args['id']
    dialogs.show_course_report_dialog(print_course_report, download_course_report, show_person_report)

def show_course_delete(e: events.GenericEventArguments) -> None:
    id = e.args['id']
    del_course()

def show_course_monitor(e: events.GenericEventArguments) -> None:
    id = e.args['id']
    dialogs.show_course_monitor_dialog(import_students=import_students, add_students=add_students)

def add_course():
    with ui.dialog().props('persistent') as dialog, ui.card().classes('w-1/2 h-1/2'):
        ui.label('创建课堂').classes('w-full font-serif font-bold text-2xl text-black')
        with ui.row().classes('w-full mt-5 place-content-between'):
            ui.label('班级').classes('w-full font-serif font-normal text-sm text-black')
            ui.input(placeholder='请输入班级') \
                .props('rounded-md outlined dense') \
                .classes('w-full self-center item-center ')
        with ui.row().classes('w-full place-content-between'):
            ui.label('科目').classes('w-full font-serif font-normal text-sm text-black')
            ui.input(placeholder='请输入科目') \
                .props('rounded-md outlined dense') \
                .classes('w-full self-center item-center ')
        with ui.row().classes('w-full place-content-between'):
            ui.label('任课老师').classes('w-full font-serif font-normal text-sm text-black')
            ui.input(placeholder='请输入教师姓名') \
                .props('rounded-md outlined dense') \
                .classes('w-full self-center item-center ')            
        ui.button('Close', on_click=dialog.close)
    dialog.open()

def del_course():
    ui.notify('del course')

def print_course_report():
    ui.notify('print course report')

def download_course_report():
    ui.notify('download course report')
        
def show_person_report():
    dialogs.person_report_dialog()

# 导入学生
def import_students():
    ui.notify('import students')
#添加学生
def add_students():
    ui.notify('add students')    
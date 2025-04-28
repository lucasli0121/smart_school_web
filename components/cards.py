import copy
from typing import Callable
from nicegui import ui
from queue import Queue

def seat_card(seat):
    with ui.card().classes('w-[120px] h-[90px]') \
        .props('flat bordered') \
        .style('padding: 5px; border: 1px solid #65B6FF; border-radius: 10px; background: #EFF3FC') as card:
        with ui.column().classes('size-full items-center place-content-start gap-0 p-0 m-0'):
            with ui.row().classes('w-full items-center place-content-between'):
                ui.label(f'{seat["seat_no"]}').classes('text-[14px] text-[#888888] self-center font-bold')
                if seat['is_online'] == 0:
                    ui.icon('img:/static/images/off_line.png').classes('self-center')
                elif seat['is_online'] == 1:
                    ui.icon('img:/static/images/on_line.png').classes('self-center')
            with ui.column().classes('w-full mt-2 gap-0 items-center'):
                if seat['is_installed'] == 0:
                    ui.label('未安装设备').classes('w-full text-xs text-red-500')
                elif seat['is_installed'] == 1:
                    ui.label('已安装设备').classes('w-full text-xs text-green-500')
                    ui.label('设备码').classes('w-full text-xs text-gray-500')
                    ui.label(seat["mac"]).classes('w-full text-xs text-gray-500')

def seat_card_only_number(seat_no, is_installed, is_selected, on_click):
    with ui.card().classes('w-[80px] h-[60px] items-center') \
        .props('flat bordered') \
        .style('padding: 5px; border: 1px solid #65B6FF; border-radius: 4px; background: #FFFFFF') as card:
        def on_mouse_enter():
            card.style('padding: 5px; border: 1px solid #65B6FF; border-radius: 4px; background: #65B6FF')
            card_column.clear()
            with card_column:
                ui.label(seat_no).classes('text-[#FFFFFF] text-[18px] self-center')
        def on_mouse_leave():
            card.style('padding: 5px; border: 1px solid #65B6FF; border-radius: 4px; background: #FFFFFF')
            card_column.clear()
            with card_column:
                ui.label(seat_no).classes('text-[#65B6FF] text-[18px] self-center')
        def onclick():
            on_click(seat_no)
        if is_installed == 1:
            card.style('padding: 5px; border: 1px solid #888888; border-radius: 4px; background: #FFFFFF; text-color: #888888')
        else:
            # card.on('mouseenter', on_mouse_enter)
            # card.on('mouseleave', on_mouse_leave)
            card.on('click', onclick)
        with ui.column().classes('size-full items-center place-content-center gap-0 p-0 m-0') as card_column:
            if is_installed == 1:
                ui.label(seat_no).classes('text-[#888888] text-[18px] self-center')
            else:
                ui.label(seat_no).classes('text-[#65B6FF] text-[18px] self-center')
    if is_selected:
        card.style('padding: 5px; border: 1px solid #65B6FF; border-radius: 4px; background: #65B6FF')
        card_column.clear()
        with card_column:
            ui.label(seat_no).classes('text-[#FFFFFF] text-[18px] self-center')
# @description: 学生座位卡片
# @param {dict} student 学生信息字典
# @return {*}
#
class StudentCard:
    concentration_old_value: int
    student_name: str
    concentration_row: ui.row
    online_row: ui.row

    def __init__(self):
        self.concentration_old_value = 1
    

student_in_card_dict: dict[str, StudentCard] = {}

# @description: 定义学生学习状态对象，用来保存外部MQ传入专注度和在线状态以及回调函数
class StudyStatus:
    update_flag: int # 1: 更新在线状态 2: 更新专注度
    concentration_value: int
    concentration_callback: Callable[[str, int, int], None]
    is_online: int
    mac: str
    def __init__(self) -> None:
        self.update_flag = 0
        self.concentration_value = 1
        self.is_online = 0
        self.mac = ""
    def change_concentration(self):
        if self.mac in student_in_card_dict:
            student_card = student_in_card_dict[self.mac]
            if student_card.concentration_row is None:
                return
            concentration_up = 0
            if self.concentration_value > student_card.concentration_old_value:
                concentration_up = 1
            elif self.concentration_value < student_card.concentration_old_value:
                concentration_up = -1
            else:
                concentration_up = 0
            student_card.concentration_old_value = self.concentration_value
            if self.concentration_value == 1: # 低专注
                with student_card.concentration_row:
                    student_card.concentration_row.clear()
                    ui.icon('circle').classes('text-[#EF4444] w-4 h-4')
            elif self.concentration_value == 2: # 中专注
                with student_card.concentration_row:
                    student_card.concentration_row.clear()
                    ui.icon('circle').classes('text-[#FFC100] w-4 h-4')
            elif self.concentration_value == 3: # 高专注
                with student_card.concentration_row:
                    student_card.concentration_row.clear()
                    ui.icon('circle').classes('text-[#27CACA] w-4 h-4')
            if self.concentration_callback is not None:
                self.concentration_callback(student_card.student_name, self.concentration_value, concentration_up)
    def change_online(self):
        if self.mac in student_in_card_dict:
            student_card = student_in_card_dict[self.mac]
            if student_card.online_row is None:
                return
            with student_card.online_row:
                student_card.online_row.clear()
                if self.is_online == 0:
                    ui.icon('img:/static/images/off_line.png').classes('self-center')
                elif self.is_online == 1:
                    ui.icon('img:/static/images/on_line.png').classes('self-center')

student_status_queue: Queue[StudyStatus] = Queue()

#
# @description: 定义学生座位卡片,用于界面显示
# @param {dict} student 学生信息字典
# @return {*}
def student_in_seat_card(student) -> None:
    student_card = StudentCard()
    with ui.card().classes('w-[120px] h-[90px]') \
        .props('flat bordered') \
        .style('padding: 5px; border: 1px solid #65B6FF; border-radius: 10px; background: rgba(239,243,252,0.04)') as card:
        with ui.column().classes('size-full items-center place-content-around gap-0 p-0 m-0'):
            with ui.row().classes('w-full gap-0 place-content-between'):
                ui.label(student['seat_number']).classes('text-[14px] text-[#888888] self-center font-bold')
                with ui.row().classes('gap-0 place-content-end') as concentration_row:
                    student_card.concentration_row = concentration_row
                    ui.icon('circle').classes('text-gray-300 w-4 h-4')
            with ui.row().classes('w-full gap-0 place-content-center'):
                if student['name'] is not None:
                    ui.label(student['name']).classes('text-[14px] text-[#333333] self-center')
                else:
                    ui.label('未添加').classes('text-[14px] text-[#FF4D4D] self-center')
            with ui.row().classes('w-full gap-0 place-content-end') as online_row:
                student_card.online_row = online_row
                if student['status'] == 0:
                    ui.icon('img:/static/images/off_line.png').classes('self-center')
                elif student['status'] == 1:
                    ui.icon('img:/static/images/on_line.png').classes('self-center')
    mac = student['mac']
    student_card.student_name = student['name']
    if mac not in student_in_card_dict and mac is not None and mac != "":
        student_in_card_dict[mac] = student_card

# @description: 更新学生卡片的专注度
# @param {str} mac 学生的mac地址
# @param {int} concentration 学生的专注度
# @return {*}
def update_concentration_student_in_card(mac: str, concentration: int, concentration_callback: Callable[[str, int, int], None]):
    study_status = StudyStatus()
    study_status.mac = mac
    study_status.concentration_value = concentration
    study_status.concentration_callback = concentration_callback
    study_status.update_flag = 2
    student_status_queue.put(study_status)

# @description: 更新学生卡片的在线状态
# @param {str} mac 学生的mac地址
# @param {int} is_online 学生的在线状态 0:离线 1:在线
# @return {*}
def update_online_student_in_card(mac: str, is_online: int):
    study_status = StudyStatus()
    study_status.mac = mac
    study_status.is_online = is_online
    study_status.update_flag = 1
    student_status_queue.put(study_status)

# @description: 由外部线程定时器调用,定时检查队列
# 如果队列有内容，则调用更新学生卡片的专注度和在线状态
# @param None
# @return {*}
def update_student_status():
    if not student_status_queue.empty():
        study_status = student_status_queue.get()
        if study_status is None:
            return
        if isinstance(study_status, StudyStatus):
            if study_status.update_flag == 1:
                study_status.change_online()
            elif study_status.update_flag == 2:
                study_status.change_concentration()

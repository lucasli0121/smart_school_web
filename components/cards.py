from nicegui import ui

def seat_card(seat):
    with ui.card().classes('w-[120px] h-[90px]') \
        .props('flat bordered') \
        .style('padding: 5px; border: 1px solid #65B6FF; border-radius: 10px; background: #EFF3FC') as card:
        with ui.column().classes('size-full items-center place-content-start gap-0 p-0 m-0'):
            with ui.row().classes('w-full items-center place-content-between'):
                ui.label(f'{seat["seat_number"]}').classes('text-[14px] text-[#888888] self-center font-bold')
                if seat['status'] == 0:
                    ui.icon('img:/static/images/off_line.png').classes('self-center')
                elif seat['status'] == 1:
                    ui.icon('img:/static/images/on_line.png').classes('self-center')
            with ui.column().classes('w-full mt-2 gap-0 items-center'):
                if seat['status'] == 0:
                    ui.label('未安装设备').classes('w-full text-xs text-red-500')
                elif seat['status'] == 1:
                    ui.label('已安装设备').classes('w-full text-xs text-green-500')
                    ui.label('MAC').classes('w-full text-xs text-gray-500')
                    ui.label(seat["mac"]).classes('w-full text-xs text-gray-500')

# @description: 学生座位卡片
# @param {dict} student 学生信息字典
# @return {*}
#
def student_in_seat_card(student):
    with ui.card().classes('w-[120px] h-[90px]') \
        .props('flat bordered') \
        .style('padding: 5px; border: 1px solid #65B6FF; border-radius: 10px; background: #EFF3FC') as card:
        with ui.column().classes('size-full items-center place-content-around gap-0 p-0 m-0'):
            with ui.row().classes('w-full gap-0 place-content-between'):
                ui.label(student['seat_number']).classes('text-[14px] text-[#888888] self-center font-bold')
                ui.icon('circle').classes('text-[#27CACA] w-4 h-4')
            with ui.row().classes('w-full gap-0 place-content-center'):
                ui.label(student['name']).classes('text-[14px] text-[#333333] self-center')
            with ui.row().classes('w-full gap-0 place-content-end'):
                if student['status'] == 0:
                    ui.icon('img:/static/images/off_line.png').classes('self-center')
                elif student['status'] == 1:
                    ui.icon('img:/static/images/on_line.png').classes('self-center')
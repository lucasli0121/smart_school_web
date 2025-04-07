from nicegui import ui,events
from components import cards, inputs, tables


def show_device_page(tab_panel):
    with ui.row().classes('w-full h-[80px] px-[20px] mt-0 place-content-between gap-0') \
        .style('background-color: #FFFFFF !important; border-radius: 10px;'):
        with ui.row().classes('h-full items-center'):
            ui.label('总座位数:').classes('text-[20px] font-bold test-[#333333]')
            ui.label('48').classes('text-[20px] font-bold text-[#65B6FF]')
            ui.label('已使用座位:').classes('ml-3 text-[20px] font-bold test-[#333333]')
            ui.label('24').classes('text-[20px] font-bold text-[#65B6FF]')
        with ui.row().classes('h-full items-center'):
            ui.button('批量删除', icon='img:/static/images/delete@2x.png', on_click=delete_device) \
                .classes('w-25 rounded-md text-red') \
                .style('background-color: rgba(255,77,77,0.39) !important')
            ui.button('批量导入', icon='img:/static/images/import@2x.png', on_click=import_device) \
                .classes('w-25 rounded-md text-white') \
                .style('background-color: #65B6FF !important')
            ui.button('添加设备', icon='img:/static/images/add@2x.png', on_click=add_device) \
                .classes('w-25 rounded-md text-white') \
                .style('background-color: #65B6FF !important')
    
    with ui.card().classes('w-full mt-2 no-shadow') \
        .props('borderless') \
        .style('padding: 15px; background-color: #FFFFFF !important; border-radius: 10px;'):
        row_number = ['A', 'B', 'C', 'D', 'E', 'F']
        for i in row_number:
            with ui.row().classes('w-full items-center place-content-evenly'):
                ui.label(f'{i}排').classes('text-[14px] font-bold text-[#333333]')
                for j in range(1, 10):
                    seat_number = f'{i}-{j}'
                    seat = {'seat_number': seat_number, 'status': 1, 'mac': '00:01:00:00:00:00'}
                    cards.seat_card(seat)

    with ui.card().classes('w-full mt-2 no-shadow') \
        .props('borderless') \
        .style('padding: 15px; background-color: #FFFFFF !important; border-radius: 10px;'):
        with ui.column().classes('w-full gap-1 items-center place-content-start'):
            ui.label('设备列表').classes('w-full text-[16px] text-[#333333]')
            with ui.row().classes('w-full mt-[15px] items-center place-content-start'):
                device_status = [
                    '全部',
                    '已安装',
                    '未安装',
                ]
                inputs.selection_w40(device_status, device_status[0], on_change=lambda e: ui.notify(e))
                online_status = [
                    '全部',
                    '在线',
                    '离线',
                ]
                inputs.selection_w40(online_status, online_status[0], on_change=lambda e: ui.notify(e))
                inputs.input_search_w60('请输入设备码搜索', on_enterkey=lambda e: ui.notify(e))
            table_rows = [
                {'sn': 1, 'seat_number': 'A-1', 'mac': '00:1b:00:00:00:00', 'status': '1', 'online': '1', 'operation': ''},
                {'sn': 2, 'seat_number': 'A-2', 'mac': '00:2b:ff:00:00:00', 'status': '1', 'online': '0', 'operation': ''},
                {'sn': 3, 'seat_number': 'A-3', 'mac': '00:3b:fe:00:00:00', 'status': '0', 'online': '1', 'operation': ''},
                {'sn': 4, 'seat_number': 'A-4', 'mac': '00:4b:00:00:00:00', 'status': '0', 'online': '0', 'operation': ''},
                {'sn': 5, 'seat_number': 'A-5', 'mac': '00:5b:00:00:00:00', 'status': '0', 'online': '0', 'operation': ''},
            ]
            tables.show_devices_table(table_rows, device_edit, device_delete_one)
        
def add_device():
    ui.notify('添加设备')

def import_device():
    ui.notify('批量导入')

def delete_device():
    ui.notify('批量删除')

def device_edit(e: events.GenericEventArguments):
    ui.notify(f'编辑设备 {e.args["mac"]}')

def device_delete_one(e: events.GenericEventArguments):
    ui.notify(f'删除设备 {e.args["mac"]}')
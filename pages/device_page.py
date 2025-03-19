from nicegui import ui,events
from components import cards, inputs, tables


def show_device_page(tab_panel):
    with ui.row().classes('w-full items-center place-content-end'):
        ui.button('添加设备', icon='add', on_click=add_device)
        ui.button('批量导入', icon='upload', on_click=import_device).classes('bg-white text-black')
        ui.button('批量删除', icon='delete', on_click=delete_device).style('background-color: red !important')
    with ui.row().classes('w-full mt-5 items-center place-content-start'):
        ui.label('总座位数:').classes('text-sm font-bold')
        ui.label('48').classes('text-sm font-bold text-blue-500')
        ui.label('已使用座位:').classes('text-sm ml-3 font-bold')
        ui.label('24').classes('text-sm font-bold text-blue-500')
    seat = [
        {'seat_number': 'A-1', 'status': 1, 'mac': '00:01:00:00:00:00'},
        {'seat_number': 'A-2', 'status': 1, 'mac': '00:01:00:00:00:00'},
        {'seat_number': 'A-2', 'status': 0},
    ]
    with ui.row().classes('w-full items-center place-content-start'):
        for s in seat:
            cards.seat_card(s)
    with ui.column().classes('w-full gap-1 items-center place-content-start'):
        ui.label('设备列表').classes('w-full text-sm font-bold')
        with ui.row().classes('w-full items-center place-content-start'):
            device_status = [
                '全部',
                '已安装',
                '未安装',
            ]
            inputs.selection_w40(device_status, on_change=lambda e: ui.notify(e))
            online_status = [
                '全部',
                '在线',
                '离线',
            ]
            inputs.selection_w40(online_status, on_change=lambda e: ui.notify(e))
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
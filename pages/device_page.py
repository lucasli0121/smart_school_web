import pandas as pd
from dataclasses import dataclass
from nicegui import ui,events, app
from components import cards, inputs, tables, dialogs
from dao.classroom_dao import \
    ClassRoomDao, \
    ClassRoomSeatsDao, \
    get_class_room_seats_by_classes_id, \
    query_class_room_seats_by_condition, \
    add_device_to_class_room, \
    remove_device_from_seats
from utils import global_vars

@dataclass
class SearchCondition:
    mac: str = ""
    installed_value: str = ""
    isonline_value: str = ""
search_condition = SearchCondition()

def show_device_page(tab_panel):
    class_room = ClassRoomDao()
    status, result = class_room.get_class_room()
    if status != 200:
        ui.notify(f'查询教室失败: {result}')
    global_vars.set_class_room(class_room)
    with ui.row().classes('w-full h-[80px] px-[20px] mt-0 place-content-between gap-0') \
        .style('background-color: #FFFFFF !important; border-radius: 10px;'):
        with ui.row().classes('h-full items-center'):
            ui.label('总座位数:').classes('text-[20px] font-bold test-[#333333]')
            app.storage.client['seat_total_number_label'] = ui.label('48').classes('text-[20px] font-bold text-[#65B6FF]') \
                .bind_text_from(global_vars.get_class_room(), 'seat_total_number')
            ui.label('已使用座位:').classes('ml-3 text-[20px] font-bold test-[#333333]')
            app.storage.client['seat_used_label'] = ui.label('24').classes('text-[20px] font-bold text-[#65B6FF]') \
                .bind_text_from(global_vars.get_class_room(), 'seat_used')
        with ui.row().classes('h-full items-center'):
            ui.button('批量删除', icon='img:/static/images/delete@2x.png', on_click=delete_device) \
                .classes('w-25 rounded-md text-red') \
                .style('background-color: rgba(255,77,77,0.39) !important')
            ui.button('刷新', icon='img:/static/images/refresh@2x.png', on_click=refresh_all) \
                .classes('w-25 rounded-md text-white') \
                .style('background-color: #6C96FB !important')
            ui.button('批量导入', icon='img:/static/images/import@2x.png', on_click=import_device) \
                .classes('w-25 rounded-md text-white') \
                .style('background-color: #65B6FF !important')
            ui.button('添加设备', icon='img:/static/images/add@2x.png', on_click=add_device) \
                .classes('w-25 rounded-md text-white') \
                .style('background-color: #65B6FF !important')
    status, seats_list = get_class_room_seats_by_classes_id(global_vars.get_class_room().id)
    if status != 200:
        ui.notify(f'查询教室座位失败: {seats_list}')
    else:
        with ui.card().classes('w-full mt-2 no-shadow') \
            .props('borderless') \
            .style('padding: 15px; background-color: #FFFFFF !important; border-radius: 10px;') as seats_cards:
            app.storage.client['seats_cards'] = seats_cards
            for i in range(0, global_vars.get_class_room().seat_row):
                with ui.row().classes('w-full items-center place-content-evenly'):
                    row_label = chr(65 + i)  # Convert row index to letter (A, B, C, ...)
                    ui.label(f'{row_label}排').classes('text-[14px] font-bold text-[#333333]')
                    for j in range(0, global_vars.get_class_room().seat_col):
                        seat_item = seats_list[i * global_vars.get_class_room().seat_col + j]
                        if isinstance(seat_item, ClassRoomSeatsDao):
                            seats_dao: ClassRoomSeatsDao = seat_item
                            seat = {'seat_no': seats_dao.seat_no, 'is_installed': seats_dao.is_installed, 'mac': seats_dao.mac, 'is_online': seats_dao.is_online}
                            cards.seat_card(seat)
                        else:
                            continue

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
                inputs.selection_w40(device_status, device_status[0], on_change=lambda e: refresh_device_table()) \
                    .bind_value_to(search_condition, 'installed_value')
                online_status = [
                    '全部',
                    '在线',
                    '离线',
                ]
                inputs.selection_w40(online_status, online_status[0], on_change=lambda e: refresh_device_table()) \
                    .bind_value_to(search_condition, 'isonline_value')
                inputs.input_search_w60('请输入设备码搜索', on_enterkey=lambda e: refresh_device_table()) \
                    .bind_value_to(search_condition, 'mac')
            
            table_rows: list[dict] = []
            device_table = tables.show_devices_table(table_rows, device_edit, device_delete_one)
            app.storage.client['device_table'] = device_table
            if isinstance(seats_list, list):
                for i in range(0, len(seats_list)):
                    seat_item = seats_list[i]
                    if isinstance(seat_item, ClassRoomSeatsDao):
                        seats_dao: ClassRoomSeatsDao = seat_item
                        seat = {'sn': i + 1, 'seat_no': seats_dao.seat_no, 'mac': seats_dao.mac, 'is_installed': seats_dao.is_installed, 'is_online': seats_dao.is_online, 'operation': ''}
                        table_rows.append(seat)
                    else:
                        continue
    refresh_device_table()

def refresh_all():
    refresh_device_seats()
    refresh_device_table()

def refresh_device_seats():
    global_vars.get_class_room().get_class_room()
    if 'seat_used_label' in app.storage.client:
        app.storage.client['seat_used_label'].text = global_vars.get_class_room().seat_used
    status, seats_list = get_class_room_seats_by_classes_id(global_vars.get_class_room().id)
    if status != 200:
        ui.notify(f'查询教室座位失败: {str(seats_list)}')
    else:
        if 'seats_cards' in app.storage.client:
            app.storage.client['seats_cards'].clear()
            with app.storage.client['seats_cards']:
                for i in range(0, global_vars.get_class_room().seat_row):
                    with ui.row().classes('w-full items-center place-content-evenly'):
                        row_label = chr(65 + i)  # Convert row index to letter (A, B, C, ...)
                        ui.label(f'{row_label}排').classes('text-[14px] font-bold text-[#333333]')
                        for j in range(0, global_vars.get_class_room().seat_col):
                            seat_item = seats_list[i * global_vars.get_class_room().seat_col + j]
                            if isinstance(seat_item, ClassRoomSeatsDao):
                                seats_dao: ClassRoomSeatsDao = seat_item
                                seat = {'seat_no': seats_dao.seat_no, 'is_installed': seats_dao.is_installed, 'mac': seats_dao.mac, 'is_online': seats_dao.is_online}
                                cards.seat_card(seat)
                            else:
                                continue
'''
# @description: 刷新设备列表
# @param None
# @return: None
'''
def refresh_device_table():
    is_installed = -1
    match search_condition.installed_value:
        case '全部':
            is_installed = -1
        case '已安装':
            is_installed = 1
        case '未安装':
            is_installed = 0
        case _:
            is_installed = -1
    is_online = -1
    match search_condition.isonline_value:
        case '全部':
            is_online = -1
        case '在线':
            is_online = 1
        case '离线':
            is_online = 0
        case _:
            is_online = -1
    status, seats_list = query_class_room_seats_by_condition(global_vars.get_class_room().id, search_condition.mac, is_installed, is_online)
    if status == 200:
        table_rows: list[dict] = []
        if 'device_table' in app.storage.client:
            app.storage.client['device_table'].rows.clear()
            if isinstance(seats_list, list):
                for i in range(0, len(seats_list)):
                    seat_item = seats_list[i]
                    if isinstance(seat_item, ClassRoomSeatsDao):
                        seats_dao: ClassRoomSeatsDao = seat_item
                        seat = {'sn': i + 1, 'seat_no': seats_dao.seat_no, 'mac': seats_dao.mac, 'is_installed': seats_dao.is_installed, 'is_online': seats_dao.is_online, 'operation': ''}
                        table_rows.append(seat)
                    else:
                        continue
                app.storage.client['device_table'].add_rows(table_rows)
                app.storage.client['device_table'].update()

#
# @description: 添加设备
# @param None
# @return: None
#             
def add_device():
    def on_ok(seat_no, mac):
        seatsDao = ClassRoomSeatsDao( \
            class_room_id=global_vars.get_class_room().id, \
            mac=mac, \
            seat_no=seat_no, \
            is_online=0, \
            is_installed=1)
        status, result = add_device_to_class_room(seatsDao)
        if status is False:
            ui.notify(f'导入设备失败: {result}')
            return
        ui.notify('添加设备成功')
        refresh_all()
        dialog.close()
    dialog = dialogs.show_install_device_dialog(onok=on_ok)

#
# @description: 批量导入设备
# @param None
# @return: None
#
def import_device():
    def handle_upload(event):
        # event.content 是文件的二进制内容
        import io
        file_content = io.BytesIO(event.content.read())
        df = pd.read_excel(file_content)
        for index, row in df.iterrows():
            # 处理每一行数据
            mac = row['mac']
            seat_no = row['seat_no']
            seatsDao = ClassRoomSeatsDao( \
                class_room_id=global_vars.get_class_room().id, \
                mac=mac, \
                seat_no=seat_no, \
                is_online=0, \
                is_installed=1)
            status, result = add_device_to_class_room(seatsDao)
            if status is False:
                ui.notify(f'导入设备失败: {result}')
                return
        ui.notify('导入设备成功')
        refresh_all()
        dialog.close()

    with ui.dialog().props('persistent') as dialog, ui.card().classes('w-1/3 h-1/3') \
        .style('background-color: #FFFFFF !important; border-radius: 10px;'):
        with ui.row().classes('size-full mt-5 place-content-between'):
            ui.upload(label="请选择批量上传文件", on_upload=handle_upload) \
                .props('flat accept=".xls,.xlsx"') \
                .classes('size-full')
    dialog.open()
    
'''
# @description: 批量删除设备
# @param None  
# @return: None
# 
'''
def delete_device():
    if app.storage.client['device_table'] is not None:
        selection = app.storage.client['device_table'].selected
        seat_no_list = [item['seat_no'] for item in selection]
        for seat_no in seat_no_list:
            result, msg = delete_device_with_seatno(seat_no)
            if result is False:
                ui.notify(msg)
                break
        refresh_all()

def device_edit(e: events.GenericEventArguments):
    ui.notify(f'编辑设备 {e.args["mac"]}')

def device_delete_one(e: events.GenericEventArguments):
    seat_no = e.args['seat_no']
    result, msg = delete_device_with_seatno(seat_no)
    ui.notify(msg)
    if result is True:
        refresh_all()

def delete_device_with_seatno(seat_no: str) -> tuple[bool, str]:
    class_room_id = global_vars.get_class_room().id
    return remove_device_from_seats(class_room_id, seat_no)
'''
Author: liguoqiang
Date: 2025-03-04 18:39:13
LastEditors: liguoqiang
LastEditTime: 2025-03-04 21:45:28
Description: 
'''
from nicegui import ui
from resources import strings

def alarm_records() -> None:
    with ui.dialog() as dialog, ui.card():
        with ui.column():
            ui.label(strings.ALARM_RECORDS).classes('text-center font-bold text-xl w-full')
            show_records_table()
            with ui.row():
                ui.button('Close', on_click=dialog.close).classes('m-2')

def show_records_table() -> None:
    columns = [
        {'name':'ID', 'label': 'ID', 'field': 'id', 'sortable': True},
        {'name':'Device MAC', 'label': strings.DEVICE_MAC, 'field': 'device_mac', 'sortable': True},
        {'name':'Device Name', 'label': strings.DEVICE_NAME, 'field': 'device_name', 'sortable': True},
        {'name':'Log Content', 'label': strings.LOG_CONTENT, 'field': 'log_content', 'sortable': True},
        {'name':'Log Status', 'label': strings.LOG_STATUS, 'field': 'log_status', 'sortable': True},
        {'name':'Log Datetime', 'label': strings.LOG_DATETIME, 'field': 'log_datetime', 'sortable': True},
        {'name':'Operation', 'label': strings.OPERATION, 'field': 'operation', 'sortable': True}
    ]
    ui.table(
        columns = columns,
        rows = [],
        pagination=10).classes('w-full')
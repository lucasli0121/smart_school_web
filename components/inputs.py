'''
Author: liguoqiang
Date: 2025-03-15 16:18:09
LastEditors: liguoqiang
LastEditTime: 2025-03-16 17:13:05
Description: 
'''
from nicegui import ui

def input_user_w60(placeholder, on_enterkey) -> ui.input:
    with ui.input(placeholder=placeholder) \
        .props('autofocus rounded-md outlined dense') \
        .classes('w-60 self-center item-center ') as input:
        with input.add_slot('append'):
            ui.icon('person').on('click', on_enterkey).classes('cursor-pointer')
        # input.add_slot('append', r'''
        #     <q-btn flat round dense icon="person" @click="() => $parent.$emit('on_enterkey')"/>
        # ''')
    input.on('keydown.enter', on_enterkey)
    return input

def input_password_w60(placeholder, on_enterkey) -> ui.input:
    return ui.input(placeholder=placeholder, password=True, password_toggle_button=True) \
        .props('autofocus rounded-md outlined dense') \
        .classes('w-60 self-center item-center') \
        .on('keydown.enter', on_enterkey)

def input_search_w40(placeholder, on_enterkey) -> ui.input:
    with ui.input(placeholder=placeholder) \
        .props('autofocus rounded-md outlined dense') \
        .classes('w-40 self-center item-center ') as input:
        input.add_slot('append', r'''
            <q-btn flat round dense icon="search" @click="() => $parent.$emit('on_enterkey')"/>
        ''')
    input.on('on_enterkey', on_enterkey)
    input.on('keydown.enter', on_enterkey)
    return input

def input_search_w60(placeholder, on_enterkey) -> ui.input:
    with ui.input(placeholder=placeholder) \
        .props('autofocus rounded-md outlined dense') \
        .classes('w-60 self-center item-center ') as input:
        input.add_slot('append', r'''
            <q-btn flat round dense icon="search" @click="() => $parent.$emit('on_enterkey')"/>
        ''')
    input.on('on_enterkey', on_enterkey)
    input.on('keydown.enter', on_enterkey)
    return input

def date_input_w40(placeholder, on_enterkey) -> ui.input:
    with ui.input(placeholder=placeholder) \
        .props('autofocus rounded-md outlined dense') \
        .classes('w-40 self-center item-center ') as date_input:
        with ui.menu().props('no-parent-event') as menu:
            with ui.date().bind_value(date_input):
                with ui.row().classes('justify-end'):
                    ui.button('Close', on_click=menu.close).props('flat')
    with date_input.add_slot('append'):
        ui.icon('edit_calendar').on('click', menu.open).classes('cursor-pointer')
    date_input.on('keydown.enter', on_enterkey)
    return date_input

def selection_w40(options, on_change) -> ui.select:
    return ui.select(options=options, with_input=False, on_change=lambda e: on_change(e.value)) \
        .props('autofocus rounded-md outlined dense') \
        .classes('w-40 self-center item-center transition-all')
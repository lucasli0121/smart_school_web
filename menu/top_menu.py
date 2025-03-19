'''
Author: liguoqiang
Date: 2025-03-03 21:35:35
LastEditors: liguoqiang
LastEditTime: 2025-03-16 17:20:56
Description: 
'''
from nicegui import ui,app

def logout() -> None:
    app.storage.user.clear()
    ui.navigate.to('/login')

def top_menu() -> None:
    ui.button(icon='notifications', on_click=lambda: ui.notify('Hello, world!')).classes('text-white')
    ui.button(icon='logout', on_click=logout).classes('text-white')
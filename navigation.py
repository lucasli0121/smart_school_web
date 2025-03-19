'''
Author: liguoqiang
Date: 2025-03-03 21:20:50
LastEditors: liguoqiang
LastEditTime: 2025-03-13 10:11:12
Description: 
'''

from contextlib import contextmanager
from nicegui import ui
from resources import strings
from menu.top_menu import top_menu

HOME_NAVIGATION = 'Home'
COURSE_NAVIGATION = 'Course'
DEVICE_NAVIGATION = 'Device'

navigation_switcher = {
    HOME_NAVIGATION: strings.HOME_PAGE,
    COURSE_NAVIGATION: strings.COURSE_PAGE,
    DEVICE_NAVIGATION: strings.DEVICE_PAGE,
}

@contextmanager
def frame(navigation: str):
    ui.colors(primary='#6E93D6', secondary='#53B689', accent='#111B1E', positive='#53B689')
    navigation_title = navigation_switcher.get(navigation, '')
    with ui.header():
        ui.label(strings.APP_NAME).classes('font-bold')
        ui.space()
        ui.label(navigation_title)
        ui.space()
        with ui.row():
            top_menu()
    with ui.column().classes('absolute-center items-center'):
        if navigation == 'Home':
            yield

def navigation_content_page(navigation: str):
    pass
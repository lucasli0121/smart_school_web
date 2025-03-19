'''
Author: liguoqiang
Date: 2025-03-16 15:26:37
LastEditors: liguoqiang
LastEditTime: 2025-03-16 17:18:36
Description: 
'''
from nicegui import ui,app
from resources import strings
from menu.top_menu import top_menu
from navigation import navigation_switcher, HOME_NAVIGATION, COURSE_NAVIGATION, DEVICE_NAVIGATION
from pages.course_page import show_course_page
from pages.device_page import show_device_page


@ui.page('/')
def main_page() -> None:
    ui.add_css('''
        .custom-tabs .q-tab__label {
            font-size: 20px !important;  # 修改字体大小
            color: #ffff !important;  # 修改字体颜色
        }
        .custom-tabs .q-tab--active {
            background-color: #1f66a0 !important;  # 选中的 tab 背景颜色
        }

    ''')
    # ui.colors(primary='#6E93D6', secondary='#53B689', accent='#111B1E', positive='#53B689')
    with ui.header().classes('shadow-md').style('background-color: white') as header:
        ui.label(strings.APP_NAME).classes('font-serif font-bold text-2xl text-blue-500')
        ui.space()
        header_title = ui.label(navigation_switcher.get(HOME_NAVIGATION, '')).classes('font-serif font-bold text-2xl text-blue-500')
        ui.space()
        with ui.row():
            top_menu()
    # with ui.column().classes('absolute-center items-center'):
    tab_panels = show_tabs()
    header_title.bind_text_from(tab_panels, 'value', lambda value: value.props["label"] if not isinstance(value, str) else value)

def show_tabs() -> ui.tab_panels:
    with ui.left_drawer().style('width: 200px !important').classes('bg-blue-400') as left_drawer:
        with ui.tabs().props('vertical').classes('w-full text-white custom-tabs') as tabs:
            course = ui.tab('课程管理').props('icon-left')
            devices = ui.tab('设备管理').props('icon-left')
    with ui.tab_panels(tabs, value=course) \
        .props('vertical').classes('w-full h-full') as tab_panels:
        with ui.tab_panel(course) as course_panel:
            show_course_page(course_panel)
        with ui.tab_panel(devices) as device_panel:
            show_device_page(device_panel)
    return tab_panels
'''
Author: liguoqiang
Date: 2025-03-16 15:26:37
LastEditors: liguoqiang
LastEditTime: 2025-03-16 17:18:36
Description: 
'''
from fastapi.staticfiles import StaticFiles
from nicegui import ui,app
from resources import strings
from menu.top_menu import top_menu
from navigation import navigation_switcher, HOME_NAVIGATION, COURSE_NAVIGATION, DEVICE_NAVIGATION
from pages.course_page import show_course_page
from pages.device_page import show_device_page
from utils import global_vars


@ui.page('/')
def main_page() -> None:
    ui.add_css('''
        .custom-tabs .q-tab__indicator {
            display: none !important;  # 隐藏下划线
        }
        .custom-tabs .q-tab__label {
            font-size: 20px !important;  # 修改字体大小
            color: #ffff !important;  # 修改字体颜色
        }
        
        .custom-tabs .q-tab--active,
        .custom-tabs .q-tab.q-tab--active,
        .custom-tabs .q-tab[aria-selected="true"] {
            background-color: #449DEE !important;  /* 选中的 tab 背景颜色 */
        }
        .custom-tabs {
            padding: 0 !important;
            margin-top: 30px !important;
            margin-left: 0 !important;
            margin-right: 0 !important;
            width: 100% !important;
            height: 100% !important;
            align-items: center !important;
        }
        .custom-tabs .q-tab {
            background-color: #65B6FF !important;  /* 未选中的 tab 背景颜色 */
            border-radius: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            width: 100% !important;
            height: 80px !important;
        }
        /* 移除页面元素的内边距 */
        .q-page {
            padding: 0 !important;
            margin: 0 !important;
            width: 100% !important;
            background-color: #F4F9FD !important;
        }
        .q-drawer {
            top: 0;
            bottom: 0;
            padding: 0;
            margin: 0;
            height: 100%;
            background-color: #65B6FF;
        }
        .nicegui-drawer {
            padding: 0 !important;
            margin: 0 !important;
        }
        
    ''')
    
    with ui.header().classes('item-center place-content-between').style('background-color: white'):
        global_vars.header_title = ui.row().classes('h-full items-center place-content-start gap-0')
        ui.space()
        with ui.row():
            top_menu()
    global_vars.tab_panels = show_tabs()
    global_vars.show_main_page_title()

def show_tabs() -> ui.tab_panels:
    with ui.left_drawer(top_corner=True).props('width=260'):
        with ui.element('div').classes('flex pl-[16px] pt-[16px]'):
            ui.image('/static/images/logo@2x.png').classes('w-[206px] h-[47px] place-self-start')
        with ui.tabs().props('vertical no-caps inline-label').classes('mt-[30px] text-white custom-tabs') as tabs:
            course = ui.tab(strings.get('course_management'), icon='img:/static/images/course.png').props('icon-left').classes('w-full h-[80px]')
            devices = ui.tab(strings.get('device_management'), icon='img:/static/images/devices.png').props('icon-left').classes('w-full h-[80px]')
    with ui.tab_panels(tabs, value=course) \
        .props('vertical') \
        .classes('w-full h-full q-pa-none') \
        .style('margin: 0 !important; padding: 0 !important;') as tab_panels:
        global_vars.course_container = ui.tab_panel(course).classes('gap-0').style('margin: 0 !important; padding: 0 !important; background-color: #F4F9FD !important;')
        show_course_page()
        with ui.tab_panel(devices).classes('gap-0').style('margin: 0 !important; padding: 0 !important; background-color: #F4F9FD !important;') as device_panel:
            show_device_page(device_panel)
    return tab_panels


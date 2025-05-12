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
import navigation
from pages.course_page import show_course_page
from pages.device_page import show_device_page
from pages.course_report_page import show_course_report_page
from pages.person_report_page import show_person_report_page
from pages.course_detail_page import show_course_detail_page

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
    if 'navigation' not in app.storage.user:
        app.storage.user['navigation'] = navigation.HOME_NAVIGATION
    with ui.header().classes('item-center place-content-between').style('background-color: white'):
        header_row = ui.row().classes('h-full items-center place-content-start gap-0')
        ui.space()
        with ui.row():
            top_menu()
    tab_panels = show_tabs()
    if app.storage.user['navigation'] == navigation.HOME_NAVIGATION:
        with header_row:
            header_row.clear()
            title = ui.label(navigation.navigation_switcher.get(navigation.HOME_NAVIGATION, '')).classes('place-self-center').style('font-size: 24px; color:#65B6FF')
            title.bind_text_from(tab_panels, 'value', lambda value: value.props["label"] if not isinstance(value, str) else value)
    elif app.storage.user['navigation'] == navigation.COURSE_REPORT_NAVIGATION:
        with header_row:
            header_row.clear()
            ui.icon('img:/static/images/back@2x.png') \
                .classes('w-[24px] h-[24px]') \
                .on('click', app.storage.user['onback'])
            ui.label('课程管理 / ').classes('ml-2 text-[20px] text-[#333333]')
            ui.label('学习专注度报告').classes('text-[20px] text-[#65B6FF]')
    elif app.storage.user['navigation'] == navigation.COURSE_DETAIL_NAVIGATION:
        with header_row:
            header_row.clear()
            onback = app.storage.user['onback']
            ui.icon('img:/static/images/back@2x.png') \
                .classes('w-[24px] h-[24px]') \
                .on('click', onback)
            ui.label('课程管理 / ').classes('ml-2 text-[20px] text-[#333333]')
            ui.label('课程详情').classes('text-[20px] text-[#65B6FF]')
    elif app.storage.user['navigation'] == navigation.COURSE_PERSON_REPORT_NAVIGATION:
        with header_row:
            header_row.clear()
            onback = app.storage.user['onback']
            ui.icon('img:/static/images/back@2x.png') \
                .classes('w-[24px] h-[24px]') \
                .on('click', onback)
            ui.label('课程管理 / 学习专注度报告 / ').classes('ml-2 text-[20px] text-[#333333]')
            ui.label('个人报告').classes('text-[20px] text-[#65B6FF]')

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
        with ui.tab_panel(course).classes('gap-0').style('margin: 0 !important; padding: 0 !important; background-color: #F4F9FD !important;'):
            if 'course_container' not in app.storage.user:
                app.storage.user['course_container'] = navigation.COURSE_NAVIGATION

            if app.storage.user['course_container'] == navigation.COURSE_NAVIGATION:
                show_course_page()
            elif app.storage.user['course_container'] == navigation.COURSE_REPORT_NAVIGATION:
                person_report_func = app.storage.user['person_report']
                show_course_report_page(app.storage.user['course_id'], person_report_func)
            elif app.storage.user['course_container'] == navigation.COURSE_PERSON_REPORT_NAVIGATION:
                show_person_report_page(app.storage.user['course_id'], app.storage.user['user_id'])
            elif app.storage.user['course_container'] == navigation.COURSE_DETAIL_NAVIGATION:
                course_id = app.storage.user['course_id']
                show_course_detail_page(course_id)
        with ui.tab_panel(devices).classes('gap-0').style('margin: 0 !important; padding: 0 !important; background-color: #F4F9FD !important;') as device_panel:
            show_device_page(device_panel)
    return tab_panels


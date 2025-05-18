'''
Author: liguoqiang
Date: 2025-03-03 21:20:50
LastEditors: liguoqiang
LastEditTime: 2025-03-13 10:11:12
Description: 
'''

from contextlib import contextmanager
from nicegui import ui,app, events
from typing import Callable
from resources import strings
from menu.top_menu import top_menu

HOME_NAVIGATION = 'Home'
COURSE_NAVIGATION = 'Course'
COURSE_REPORT_NAVIGATION = 'CourseReport'
COURSE_DETAIL_NAVIGATION = 'CourseDetail'
COURSE_PERSON_REPORT_NAVIGATION = 'CoursePersonReport'
DEVICE_NAVIGATION = 'Device'

navigation_switcher = {
    HOME_NAVIGATION: strings.HOME_PAGE,
    COURSE_NAVIGATION: strings.COURSE_PAGE,
    DEVICE_NAVIGATION: strings.DEVICE_PAGE,
}
def show_main_page_title() -> None:
    app.storage.user['navigation'] = HOME_NAVIGATION
    ui.navigate.to('/')

            
def show_course_detail_title(onback) -> None:
    app.storage.user['navigation'] = COURSE_DETAIL_NAVIGATION
    app.storage.user['onback'] = onback
    ui.navigate.to('/')
            

def show_report_title(onback) -> None:
    app.storage.user['navigation'] = COURSE_REPORT_NAVIGATION
    app.storage.user['onback'] = onback
    ui.navigate.to('/')


def show_person_report_title(onback) -> None:
    app.storage.user['navigation'] = COURSE_PERSON_REPORT_NAVIGATION
    app.storage.user['onback'] = onback
    ui.navigate.to('/')

#
# @description: 定义课堂导航页面,设置课堂导航类型
# @param {str} navigation 课堂导航类型
def navigation_course_page() -> None:
    app.storage.user['navigation'] = HOME_NAVIGATION
    app.storage.user['course_container'] = COURSE_NAVIGATION
    ui.navigate.to('/')

def navigation_device_page() -> None:
    app.storage.user['navigation'] = DEVICE_NAVIGATION
    ui.navigate.to('/')
#
# @description: 定义课堂报告页面,设置课堂报告类型
# @param {int} course_id 课堂ID
# @param {Callable[[], None]} onback 回调函数
# @return {*}
#
def navigation_course_report_page(course_id: int, onback: Callable[[], None], person_report: Callable[[events.GenericEventArguments], None] ) -> None:
    app.storage.user['navigation'] = COURSE_REPORT_NAVIGATION
    app.storage.user['onback'] = onback
    app.storage.user['person_report'] = person_report
    app.storage.user['course_container'] = COURSE_REPORT_NAVIGATION
    app.storage.user['course_id'] = course_id
    ui.navigate.to('/')

#
# @description: 定义课堂个人报告页面,设置课堂个人报告类型
# @param {int} course_id 课堂ID
# @param {int} id 学生ID
# @param {Callable[[], None]} onback 回调函数
# @return {*}
#
def navigation_course_person_report_page(course_id: int, id: int, onback: Callable[[], None]) -> None:
    app.storage.user['navigation'] = COURSE_PERSON_REPORT_NAVIGATION
    app.storage.user['onback'] = onback
    app.storage.user['course_container'] = COURSE_PERSON_REPORT_NAVIGATION
    app.storage.user['course_id'] = course_id
    app.storage.user['user_id'] = id
    ui.navigate.to('/')

#
# @description: 定义课堂详情页面,设置课堂详情类型
# @param {int} course_id 课堂ID
# @param {Callable[[], None]} onback 回调函数
# @return {*}
#
def navigation_course_detail_page(course_id: int, onback: Callable[[], None]) -> None:
    app.storage.user['navigation'] = COURSE_DETAIL_NAVIGATION
    app.storage.user['onback'] = onback
    app.storage.user['course_container'] = COURSE_DETAIL_NAVIGATION
    app.storage.user['course_id'] = course_id
    ui.navigate.to('/')

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
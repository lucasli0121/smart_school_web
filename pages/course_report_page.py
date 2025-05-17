from dataclasses import dataclass
from datetime import datetime

from typing import Optional
from nicegui import ui, app
from components import tables, cards
from utils import global_vars
from dao.course_dao import CourseDao
from dao.course_report_dao import CourseReportDao, get_course_report_by_course_id, CourseStudentsConcentrationDao, query_course_student_concentration
from dao.progress_value import ProgressValue
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from utils.make_png import generate_png
import threading as thread
from queue import Queue

download_progress_value = ProgressValue(0.0)
#
# @description: 显示课程报告页面
# @param {int} course_id 课程ID
# @return {*}
#
def show_course_report_page(course_id: int, person_report_callback) -> None:
    course_dao = CourseDao()
    course_dao.id = course_id
    status, result = course_dao.get_course_by_id()
    if status != 200:
        ui.notify(f'获取课程信息失败, {result}')
        return
    app.storage.user['course_dao'] = course_dao
    status, report_result = get_course_report_by_course_id(global_vars.get_class_room().id, course_id)
    if status != 200:
        if isinstance(report_result, str):
            ui.notify(f'获取课程报告失败, {report_result}')
        return
    if not isinstance(report_result, CourseReportDao):
        ui.notify('获取课程报告失败, 数据格式错误')
        return
    report_dao: CourseReportDao = report_result
    trade_time = [datetime.strptime(item.create_time, '%Y-%m-%d %H:%M:%S').strftime('%H:%M') for item in report_dao.concentration_trade]
    deep_concentration = [item.deep_concentration_num for item in report_dao.concentration_trade]
    mid_concentration = [item.mid_concentration_num for item in report_dao.concentration_trade]
    low_concentration = [item.low_concentration_num for item in report_dao.concentration_trade]
    with ui.column().classes('w-full gap-0 mt-0 p-[15px] items-center place-content-start') \
        .style('background-color: #FFFFFF !important; border-radius: 10px;'):
        with ui.row().classes('w-full gap-0 items-center place-content-between'):
            with ui.row().classes('items-center place-content-start gap-0'):
                ui.icon('square').classes('text-[#65B6FF] w-[6px] h-[20px]')
                ui.label('课程详情').classes('ml-2 font-bold text-[#333333] text-[18px]')
            with ui.row().classes('items-center place-content-end'):
                ui.button('打印', icon='img:/static/images/printer@2x.png', on_click=print_course_report) \
                    .classes('w-25 rounded-md text-white') \
                    .style('background-color: #27CACA !important; border-radius: 6px;')
                app.storage.client['download_button'] = ui.button('下载', icon='img:/static/images/download@2x.png', on_click=download_course_report) \
                    .classes('w-25 rounded-md text-white') \
                    .style('background-color: #65B6FF !important; border-radius: 6px;')
                download_progress_ui = ui.circular_progress(value=0.0, min=0.0, max=1.0, show_value=True) \
                    .classes('w-[30px] h-[30px]') \
                    .style('color: #65B6FF !important; background-color: #FFFFFF !important; border-radius: 50% !important;')
                download_progress_ui.bind_value_from(download_progress_value, 'value')
                app.storage.client['download_progress_ui'] = download_progress_ui
                app.storage.client['download_progress_ui'].visible = False
        with ui.row().classes('w-full mt-2 items-center place-content-start'):
            ui.icon('img:/static/images/group_student@2x.png').classes('w-[40px] h-[40px]')
            ui.label('一(4)班').classes('ml-2 text-[#333333] text-[14px]') \
                .bind_text_from(course_dao, 'classes')
        with ui.row().classes('w-full mt-2 gap-0 items-center place-content-start'):
            ui.icon('img:/static/images/subject@2x.png').classes('w-[40px] h-[40px]')
            ui.label('科目').classes('ml-2 text-[#888888] text-[14px]')
            ui.label('数学').classes('ml-2 text-[#008DFF] text-[14px]') \
                .bind_text_from(course_dao, 'subject')
            ui.icon('img:/static/images/teacher@2x.png').classes('ml-5 w-[40px] h-[40px]')
            ui.label('任课老师').classes('ml-2 text-[#888888] text-[14px]')
            ui.label('张明华').classes('ml-2 text-[#008DFF] text-[14px]') \
                .bind_text_from(course_dao, 'teacher')
            ui.icon('img:/static/images/student@2x.png').classes('ml-5 w-[40px] h-[40px]')
            ui.label('学生人数').classes('ml-2 text-[#888888] text-[14px]')
            ui.label('46人').classes('ml-2 text-[#008DFF] text-[14px]') \
                .bind_text_from(course_dao, 'student_num')
            ui.label('人').classes('text-[#008DFF] text-[14px]')
            ui.icon('img:/static/images/calendar_2@2x.png').classes('ml-5 w-[40px] h-[40px]')
            ui.label('开始时间').classes('ml-2 text-[#888888] text-[14px]')
            ui.label('2024-01-08 08:00').classes('ml-2 text-[#008DFF] text-[14px]') \
                .bind_text_from(course_dao, 'begin_time')
            ui.icon('img:/static/images/course_time_long@2x.png').classes('ml-5 w-[40px] h-[40px]')
            ui.label('课程时长').classes('ml-2 text-[#888888] text-[14px]')
            ui.label('45分钟').classes('ml-2 text-[#008DFF] text-[14px]') \
                .bind_text_from(course_dao, 'duration')
            ui.label('分钟').classes('ml-2 text-[#008DFF] text-[14px]')
    with ui.row().classes('w-full h-[400px] mt-2 gap-0 items-center place-content-between'):
        with ui.column().classes('gap-0 p-[15px] items-center') \
            .style('background-color: #FFFFFF !important; border-radius: 10px; width: 40% !important; height: 100% !important;'):
            ui.label('专注度趋势').classes('w-full font-bold text-[16px] text-[#333333]')
            with ui.row().classes('w-full mt-2 items-center place-content-start'):
                ui.icon('img:/static/images/deep_focuson@2x.png').classes('w-[21px] h-[12px]')
                ui.label('深专注度').classes('ml-1 text-[#888888] text-[12px]')
                ui.icon('img:/static/images/mid_focuson@2x.png').classes('w-[21px] h-[12px]')
                ui.label('中专注度').classes('ml-1 text-[#888888] text-[12px]')
                ui.icon('img:/static/images/low_focuson@2x.png').classes('w-[21px] h-[12px]')
                ui.label('浅专注度').classes('ml-1 text-[#888888] text-[12px]')
                ui.space()
                ui.label('单位: 人数').classes('text-[#888888] text-[14px]')
            with ui.card().classes('w-full mt-2 flex-1').props('flat no-shadow'):
                ui.echart({
                    'tooltip': {
                        'trigger': 'axis',
                        'axisPointer': {
                            'type': 'cross',
                            'label': {
                                'backgroundColor': '#FFFFFF'
                            }
                        }
                    },
                    'grid': {
                        'left': '2%',
                        'right': '2%',
                        'bottom': '2%',
                        'containLabel': 1
                    },
                    'xAxis': {
                        'type': 'category',
                        'boundaryGap': 0,
                        'data': trade_time,
                    },
                    'yAxis': {
                        'type': 'value'
                    },
                    'series': [
                        {
                            'name':'深度专注',
                            'type': 'line',
                            'stack': 'Total',
                            'color': '#5DC72A',
                            'areaStyle': {},
                            'emphasis': {
                                'focus': 'series'
                            },
                            'data': deep_concentration
                        },
                        {
                            'name':'中度专注',
                            'type': 'line',
                            'stack': 'Total',
                            'color': '#FFC04F',
                            'areaStyle': {},
                            'emphasis': {
                                'focus': 'series'
                            },
                            'data': mid_concentration
                        },
                        {
                            'name':'浅度专注',
                            'type': 'line',
                            'stack': 'Total',
                            'color': '#F65058',
                            'areaStyle': {},
                            'emphasis': {
                                'focus': 'series'
                            },
                            'data': low_concentration
                        },
                    ]
                }).classes('w-full h-full')
        with ui.row().classes('pl-[5px] gap-[5px] items-center place-content-start') \
            .style('width: 60% !important; height: 100% !important;'):
            with ui.column().classes('gap-0 p-[15px] items-center') \
                .style('background-color: #FFFFFF !important; border-radius: 10px; width: 49% !important; height: 100% !important;'):
                ui.label('深度专注人数分布').classes('w-full font-bold text-[16px] text-[#333333]')
                with ui.row().classes('w-full mt-2 gap-0 items-center place-content-start'):
                    ui.icon('square').classes('text-[#FFA137] w-4 h-4')
                    ui.label('小于10分钟').classes('text-[#333333] text-[12px]')
                    ui.icon('square').classes('text-[#F4635E] w-4 h-4 ml-1')
                    ui.label('10-20分钟').classes('text-[#333333] text-[12px]')
                    ui.icon('square').classes('text-[#4D82FB] w-4 h-4 ml-1')
                    ui.label('20-30分钟').classes('text-[#333333] text-[12px]')
                    ui.icon('square').classes('text-[#65B6FF] w-4 h-4 ml-1')
                    ui.label('大于30分钟').classes('text-[#333333] text-[12px]')
                with ui.card().classes('w-full mt-2 flex-1').props('flat no-shadow'):
                    ui.echart({
                        'series': [
                            {
                                'type': 'pie',
                                'radius': ['30%', '60%'],
                                'color':['#FFA137','#F4635E','#4D82FB','#65B6FF'],
                                'data': [
                                    {'value': report_dao.deep_concentration_distribution.less_than_10_min_num, 'name': '小于10分钟'},
                                    {'value': report_dao.deep_concentration_distribution.less_than_20_min_num, 'name': '10-20分钟'},
                                    {'value': report_dao.deep_concentration_distribution.less_than_30_min_num, 'name': '20-30分钟'},
                                    {'value': report_dao.deep_concentration_distribution.greater_than_30_min_num, 'name': '大于30分钟'},
                                ],
                                'emphasis': {
                                    'itemStyle': {
                                        'shadowBlur': 10,
                                        'shadowOffsetX': 0,
                                        'shadowColor': 'rgba(0, 0, 0, 0.5)'
                                    }
                                }
                            },
                        ]
                    }).classes('w-full h-full')
            with ui.column().classes('gap-0 p-[15px] items-center') \
                .style('background-color: #FFFFFF !important; border-radius: 10px; width: 50% !important; height: 100% !important;'):
                ui.label('中度专注人数分布').classes('w-full font-bold text-[16px] text-[#333333]')
                with ui.row().classes('w-full mt-2 gap-0 items-center place-content-start'):
                    ui.icon('square').classes('text-[#674CF5] w-4 h-4')
                    ui.label('小于10分钟').classes('text-[#333333] text-[12px]')
                    ui.icon('square').classes('text-[#29B479] w-4 h-4 ml-1')
                    ui.label('10-20分钟').classes('text-[#333333] text-[12px]')
                    ui.icon('square').classes('text-[#FBB80F] w-4 h-4 ml-1')
                    ui.label('20-30分钟').classes('text-[#333333] text-[12px]')
                    ui.icon('square').classes('text-[#F96B3E] w-4 h-4 ml-1')
                    ui.label('大于30分钟').classes('text-[#333333] text-[12px]')
                with ui.card().classes('w-full mt-2 flex-1').props('flat no-shadow'):
                    ui.echart({
                        'series': [
                            {
                                'type': 'pie',
                                'radius': ['30%', '60%'],
                                'data': [
                                    {'value': report_dao.mid_concentration_distribution.less_than_10_min_num, 'name': '小于10分钟', 'itemStyle': {'color': '#674CF5'}},
                                    {'value': report_dao.mid_concentration_distribution.less_than_20_min_num, 'name': '10-20分钟', 'itemStyle': {'color': '#29B479'}},
                                    {'value': report_dao.mid_concentration_distribution.less_than_30_min_num, 'name': '20-30分钟', 'itemStyle': {'color': '#FBB80F'}},
                                    {'value': report_dao.mid_concentration_distribution.greater_than_30_min_num, 'name': '大于30分钟', 'itemStyle': {'color': '#F96B3E'}},
                                ],
                                'emphasis': {
                                    'itemStyle': {
                                        'shadowBlur': 10,
                                        'shadowOffsetX': 0,
                                        'shadowColor': 'rgba(0, 0, 0, 0.5)'
                                    }
                                }
                            },
                        ]
                    }).classes('w-full h-full')
    # 查询专注度
    status, concentration_list = query_course_student_concentration(course_id)
    if status != 200:
        if isinstance(concentration_list, str):
            ui.notify(f'获取课程专注度失败, {concentration_list}')
        return
    with ui.column().classes('w-full mt-2 gap-0 p-[15px] items-center place-content-start') \
        .style('background-color: #FFFFFF !important; border-radius: 10px;'):
        ui.label('学习专注度排名').classes('w-full font-bold text-[16px] text-[#333333]')
        sn = 1
        table_rows = []
        for item in concentration_list:
            if isinstance(item, CourseStudentsConcentrationDao):
                low :float = 0.0
                mid :float = 0.0
                deep :float = 0.0
                if item.total_concentration is not None and item.total_concentration > 0:
                    low = round(item.low_concentration / item.total_concentration * 100, 2)
                    mid = round(item.mid_concentration / item.total_concentration * 100, 2)
                    deep = round(item.deep_concentration / item.total_concentration * 100, 2)
                table_rows.append({
                    'course_id': course_id,
                    'id': item.student_id,
                    'sn': sn,
                    'name': item.name,
                    'gender': item.gender,
                    'deep_concentration': f'{deep}%',
                    'mid_concentration': f'{mid}%',
                    'low_concentration': f'{low}%',
                    'operation': ''
                })
            sn += 1
        tables.show_report_table(table_rows, person_report_callback)

#
# @description: 打印课程报告
# @param {*}
# @return {*}
#
def print_course_report():
    ui.notify('print course report')

@ui.page('/course_report/{course_id}')
def report_page(course_id: int):
    show_course_report_page(course_id, None)

download_status_queue = Queue[int]()
#
# @description: 下载课程报告
# @param {*}
# @return {*}
#
def download_course_report():
    if 'download_progress_ui' in app.storage.client:
        app.storage.client['download_progress_ui'].visible = True
    if 'download_button' in app.storage.client:
        app.storage.client['download_button'].visible = False
    download_progress_value.set_value(0.0)
    def check_download_queue():
        if not download_status_queue.empty():
            value = download_status_queue.get()
            if isinstance(value, int):
                if value == 10:
                    download_progress_value.set_value(1.0)
                    if 'download_progress_ui' in app.storage.client:
                        app.storage.client['download_progress_ui'].visible = False
                    if 'download_button' in app.storage.client:
                        app.storage.client['download_button'].visible = True
                    if 'download_timer' in app.storage.client:
                        app.storage.client['download_timer'].cancel()
                    course_id = app.storage.user['course_dao'].id
                    outfile= f'./static/course_report_{course_id}.png'
                    ui.download(outfile, f'course_report_{course_id}.png')
                    ui.notify('课程报告下载完成')
                else:
                    v = value / 10
                    download_progress_value.set_value(v)
                
            else:
                ui.notify('课程报告下载失败')
                if 'download_progress_ui' in app.storage.client:
                    app.storage.client['download_progress_ui'].visible = False
                if 'download_button' in app.storage.client:
                    app.storage.client['download_button'].visible = True
                if 'download_timer' in app.storage.client:
                    app.storage.client['download_timer'].cancel()
    if 'download_timer' in app.storage.client:
        app.storage.client['download_timer'].cancel()
    app.storage.client['download_timer'] = ui.timer(1, callback=check_download_queue, immediate=True)
    app.storage.client['download_timer'].activate()
    url = f"http://localhost:8083/course_report/{app.storage.user['course_dao'].id}"
    outfile = f'./static/course_report_{app.storage.user["course_dao"].id}.png'
    thr = thread.Thread(target=generate_png, args=(url, outfile, download_status_queue))
    thr.start()

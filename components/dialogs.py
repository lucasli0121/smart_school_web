'''
Author: liguoqiang
Date: 2025-03-16 17:25:54
LastEditors: liguoqiang
LastEditTime: 2025-03-19 17:27:38
Description: 
'''
from nicegui import ui
from components import labels, progress, tables

# 显示课程报告窗口   
def show_course_report_dialog(print_report, download_report, show_person_report) -> ui.dialog:
    with ui.dialog(value=True).props('persistent maximized') as dialog, ui.card().classes('size-full').style('background-color: #f5f5f5;'):
        with ui.column().classes('size-full'):
            with ui.row().classes('w-full items-center place-content-between'):
                ui.label('学习专注度报告').classes('place-content-start font-bold text-lg text-black')
                with ui.row().classes('items-center place-content-end'):
                    ui.button('打印', icon='printer', on_click=print_report)
                    ui.button('下载', icon='download', on_click=download_report)
                    ui.button(icon='close', on_click=dialog.close).props('flat round dense').classes('bg-red-500 text-white')
            with ui.row().classes('w-full mt-2 place-content-between'):
                ui.label('课程详情').classes('w-full font-bold text-sm text-black')
                with ui.card().classes('w-full').props('flat bordered'):
                    with ui.grid(columns=4).classes('w-full'):
                        with ui.row().classes('col-span-full item-center'):
                            ui.icon('class')
                            ui.label('班级').classes('font-normal text-sm text-black')
                        with ui.row().classes('item-center'):
                            ui.icon('subject')
                            ui.label('科目').classes('font-normal text-sm text-gray-300')
                            ui.label('数学').classes('font-normal text-sm text-black')
                        with ui.row().classes('col-span-3 item-center'):
                            ui.icon('groups')
                            ui.label('学生人数').classes('font-normal text-sm text-gray-300')
                            ui.label('46人').classes('font-normal text-sm text-black')
                        with ui.row().classes('item-center'):
                            ui.icon('face')
                            ui.label('任课老师').classes('font-normal text-sm text-gray-300')
                            ui.label('赵老师').classes('font-normal text-sm text-black')
                        with ui.row().classes('item-center'):
                            ui.icon('date')
                            ui.label('开始时间').classes('font-normal text-sm text-gray-300')
                            ui.label('2024-01-08 08:00').classes('font-normal text-sm text-black')
                        with ui.row().classes('col-span-2 item-center'):
                            ui.icon('timer')
                            ui.label('课程时长').classes('font-normal text-sm text-gray-300')
                            ui.label('45分钟').classes('font-normal text-sm text-black')
            with ui.scroll_area().classes('size-full mt-2'):
                with ui.row().classes('w-full place-content-between'):
                    ui.label('专注度趋势').classes('w-full font-bold text-sm text-black')
                    with ui.card().classes('w-full').props('flat bordered'):
                        ui.echart({
                            'legend': {'data': ['深度专注','中度专注','浅度专注']},
                            'xAxis': {
                                'type': 'category',
                                'boundaryGap': 'false',
                                'data': ['8:00', '8:10', '8:20', '8:30', '8:40', '8:50', '9:00', '9:10', '9:20', '9:30']
                            },
                            'yAxis': {
                                'type': 'value'
                            },
                            'series': [
                                {'name':'深度专注', 'type': 'line', 'data': [5, 8, 13, 21, 34, 55]},
                                {'name':'中度专注', 'type': 'line', 'data': [3, 10, 12, 19, 23, 30]},
                                {'name':'浅度专注', 'type': 'line', 'data': [8, 9, 18, 25, 27, 45]},
                            ]
                        }).classes('w-full h-100')
                with ui.card().classes('w-full').props('flat bordered'):
                    with ui.row().classes('w-full item-center place-content-between'):
                        with ui.column().classes('w-2/5'):
                            ui.label('深度专注人数分布').classes('w-full font-bold text-sm text-black')
                            ui.echart({
                                'legend': {'data': ['小于10分钟','10-20分钟','20-30分钟','大于30分钟']},
                                'series': [
                                    {
                                        'name':'深度专注人数分布',
                                        'type': 'pie',
                                        'radius': '70%',
                                        'data': [
                                            {'value': 8, 'name': '小于10分钟'},
                                            {'value': 10, 'name': '10-20分钟'},
                                            {'value': 15, 'name': '20-30分钟'},
                                            {'value': 12, 'name': '大于30分钟'},
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
                            }).classes('w-full h-100')
                        with ui.column().classes('w-2/5'):
                            ui.label('中度专注人数分布').classes('w-full font-bold text-sm text-black')
                            ui.echart({
                                'legend': {'data': ['小于10分钟','10-20分钟','20-30分钟','大于30分钟']},
                                'series': [
                                    {
                                        'name':'深度专注人数分布',
                                        'type': 'pie',
                                        'radius': '70%',
                                        'data': [
                                            {'value': 8, 'name': '小于10分钟', 'itemStyle': {'color': '#9fa8da'}},
                                            {'value': 10, 'name': '10-20分钟', 'itemStyle': {'color': '#7986cb'}},
                                            {'value': 15, 'name': '20-30分钟', 'itemStyle': {'color': '#5c6bc0'}},
                                            {'value': 12, 'name': '大于30分钟', 'itemStyle': {'color': '#3f51b5'}},
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
                            }).classes('w-full h-100')
                with ui.card().classes('w-full').props('flat bordered'):
                    with ui.column().classes('w-full item-start'):
                        ui.label('学习专注度排名').classes('w-full font-bold text-sm text-black')
                        table_rows = [
                            {'sn': 1, 'name': '陈佳佳', 'gender': '0', 'deep_concentration': '40%', 'mid_concentration': '35%', 'low_concentration': '25%', 'operation': ''},
                            {'sn': 2, 'name': '王思思', 'gender': '0', 'deep_concentration': '39%', 'mid_concentration': '32%', 'low_concentration': '28%', 'operation': ''},
                            {'sn': 3, 'name': '李明明', 'gender': '1', 'deep_concentration': '35%', 'mid_concentration': '38%', 'low_concentration': '27%', 'operation': ''},
                            {'sn': 4, 'name': '张雨晨', 'gender': '0', 'deep_concentration': '33%', 'mid_concentration': '37%', 'low_concentration': '30%', 'operation': ''},
                            {'sn': 5, 'name': '刘子豪', 'gender': '1', 'deep_concentration': '32%', 'mid_concentration': '39%', 'low_concentration': '32%', 'operation': ''},
                        ]
                        tables.show_report_table(table_rows, show_person_report)
    dialog.open()
    return dialog

# 显示个人报告窗口
def person_report_dialog() -> ui.dialog:
    with ui.dialog(value=True).props('persistent brightness(40%)') as dialog, \
        ui.card().style('background-color: #f5f5f5; width: 50%; max-width: 50%; height: 90%;') as card:
        with ui.row().classes('w-full items-center place-content-end'):
            ui.button(icon='close', on_click=dialog.close).props('flat round dense').classes('text-red').style('background-color: #f5f5f5;')
        with ui.row().classes('w-full h-2/3 justify-center gap-0 place-content-between'):
            with ui.column().classes('w-1/2 h-full items-center gap-0'):
                with ui.row().classes('w-full place-self-center place-content-start'):
                    labels.bold_xl_black_label('张雨晨')
                with ui.row().classes('w-full mt-2 place-self-center place-content-start'):
                    labels.normal_sm_gray_label('班级')
                    labels.normal_sm_black_label('五年级3班').classes('ml-2')
                with ui.row().classes('w-full place-self-center place-content-start'):
                    labels.normal_sm_gray_label('科目')
                    labels.normal_sm_black_label('数学').classes('ml-2')
                with ui.row().classes('w-full place-self-center place-content-start'):
                    labels.normal_sm_gray_label('任课老师')
                    labels.normal_sm_black_label('张明华老师').classes('ml-2')
                ui.echart({
                    'legend': {'data': ['浅度专注','中度专注','深度专注']},
                    'series': [
                        {
                            'name':'专注时间分布',
                            'type': 'pie',
                            'radius': '40%',
                            'label': {
                                'fontSize': 12,
                                'formatter': '{b}: {c}分钟',
                            },
                            'data': [
                                {'value': 23, 'name': '浅度专注', 'itemStyle': {'color': '#fca5a5'}},
                                {'value': 52, 'name': '中度专注', 'itemStyle': {'color': '#6366f1'}},
                                {'value': 45, 'name': '深度专注', 'itemStyle': {'color': '#25d867'}},
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
                }).classes('w-full h-full mt-10 place-self-start')
            with ui.column().classes('w-1/2 h-full items-center gap-2'):
                with ui.row().classes('w-full item-center place-content-start'):
                    ui.label('09:06:12-09:30:59').classes('place-self-center text-xl font-blod text-black')
                    ui.echart(options={
                        'series': [
                            {
                                'type': 'gauge',
                                'radius': '100%',
                                'startAngle': 90,
                                'endAngle': -270,
                                'pointer':{
                                    'show': 0,
                                },
                                'progress': {
                                    'show': 1,
                                    'overlap': 0,
                                    'roundCap': 1,
                                    'clip': 0,
                                    'itemStyle': {
                                        'borderWidth': 0,
                                        'borderColor': '#464646'
                                    }
                                },
                                'axisLine': {
                                    'lineStyle': {
                                        'width': 10
                                    }
                                },
                                'axisTick': {
                                    'show': 0
                                },
                                'axisLabel': {
                                    'show': 0,
                                    'distance': 10
                                },
                                'splitLine': {
                                    'show': 0,
                                    'distance': 0,
                                    'length': 10
                                },
                                'title': {
                                    'fontSize': 12
                                },
                                'detail': {
                                    'valueAnimation': 1,
                                    'formatter': '{value}分',
                                    'fontSize': 10,
                                },
                                'data': [
                                    {
                                        'value': 42,
                                        'title': {
                                            'offsetCenter': ['0%', '0%']
                                        },
                                        'detail': {
                                            'valueAnimation': 1,
                                            'offsetCenter': ['0%', '0%']
                                        }
                                    }
                                ]
                            }
                        ]
                    }).style('width: 50px; height: 50px;')
                progress.show_concentration_progress(19)
                progress.show_position_progress(85)
                progress.show_study_progress(59)
                # ui.label('学习状态详情').classes('w-full mt-5 place-self-start text-xl font-blod text-black')
                ui.echart({
                    'title': {
                        'text': '学习状态详情',
                        'fontSize': 12,
                    },
                    'xAxis': {
                        'type': 'category',
                        'data': ['09:06:12', '09:07:07', '09:08:02', '09:08:57', '09:09:52']
                    },
                    'yAxis': {
                        'type': 'value'
                    },
                    'series': [
                        {
                            'type': 'line',
                            'smooth': 1,
                            'min': 0,
                            'max': 100,
                            'data': [10, 15, 23, 30, 62],
                        },
                    ]
                }).classes('mt-5 place-self-start').style('width: 100%; height: 50%;')
        with ui.row().classes('w-full justify-center gap-0 place-content-between'):
            with ui.column().classes('w-1/3 items-center gap-1 place-content-start'):
                ui.label('深度专注最长时间').classes('w-full place-self-center text-sm text-black')
                ui.label('45分钟').classes('w-full place-self-center text-1g text-black font-bold')
            with ui.column().classes('w-1/3 items-center gap-1 place-content-start'):
                ui.label('专注度最高分').classes('w-full place-self-center text-sm text-black')
                ui.label('98分').classes('w-full place-self-center text-1g text-black font-bold')
            with ui.column().classes('w-1/3 items-center gap-1 place-content-start'):
                ui.label('坐姿不端正时间').classes('w-full place-self-center text-sm text-black')
                ui.label('18分钟').classes('w-full place-self-center text-1g text-black font-bold')
    dialog.open()
    return dialog


# 显示课程监控窗口
def show_course_monitor_dialog(import_students, add_students) -> ui.dialog:
    with ui.dialog(value=True).props('persistent ') as dialog, \
        ui.card().classes('p-10').style('background-color: #f5f5f5; width: 75%; max-width: 75%; height: 100%;'):
        with ui.row().classes('w-full items-center place-content-between'):
            labels.bold_1g_black_label('XX中学智能学习教室')
            with ui.row().classes('items-center place-content-center'):
                labels.bold_1g_black_label('代课老师: 王老师')
                ui.button(icon='close', on_click=dialog.close).props('flat round dense').classes('bg-red-500 text-white')
        with ui.row().classes('w-full item-center place-content-between'):
            labels.bold_sm_black_label('体验班')
            with ui.row().classes('items-center place-content-end'):
                ui.button('批量导入', icon='upload', on_click=import_students).classes('text-black')
                ui.button('添加学生', icon='add', on_click=add_students).classes('text-black')
        for x in('A', 'B', 'C', 'D', 'E', 'F'):
            with ui.row().classes('w-full gap-3 mt-2 item-center place-content-start'):
                ui.label(f'{x}排').classes('text-black font-bold text-sm place-self-center')
                for i in range(8):
                    with ui.card().classes('p-2 gap-2').props('flat bordered').style('width: 120px; height: 90px;'):
                        with ui.row().classes('w-full gap-0 place-content-between'):
                            labels.normal_sm_black_label(f'{x}-{i+1}')
                            ui.icon('circle').classes('text-green-500 w-4 h-4')
                        with ui.row().classes('w-full gap-0 place-content-center'):
                            labels.normal_sm_black_label('刘婷婷')
                        with ui.row().classes('w-full gap-0 place-content-end'):
                            ui.icon('computer').classes('text-gray-300 w-4 h-4')
        with ui.row().classes('w-full gap-1 mt-2 item-center place-content-start'):
            ui.icon('square').classes('text-green-500 w-4 h-4')
            labels.normal_sm_black_label('深度专注')
            ui.icon('square').classes('text-yellow-500 ml-5 w-4 h-4')
            labels.normal_sm_black_label('中度专注')
            ui.icon('square').classes('text-red-500 ml-5 w-4 h-4')
            labels.normal_sm_black_label('浅度专注')
            ui.icon('computer').classes('text-green-500 ml-5 w-4 h-4')
            labels.normal_sm_black_label('设备在线')
            ui.icon('computer').classes('text-gray-500 ml-5 w-4 h-4')
            labels.normal_sm_black_label('设备离线')
        with ui.card().classes('w-full p-5').props('flat'):
            with ui.row().classes('w-full place-content-start'):
                labels.bold_sm_black_label('学习状况:')
            with ui.column().classes('w-full mt-3 place-content-start gap-1'):
                with ui.row().classes('w-full'):
                    labels.normal_sm_gray_label('10:46:05')
                    labels.normal_sm_black_label('刘婷婷同学专注度下降到中度专注')
                    
        
    dialog.open()
    return dialog
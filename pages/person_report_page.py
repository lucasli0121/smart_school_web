from nicegui import ui
from components import tables, cards, inputs


def show_person_report_page(course_id: int, id: int) -> None:
    with ui.column().classes('w-full gap-0 mt-0 p-[15px] items-center place-content-start') \
        .style('background-color: #FFFFFF !important; border-radius: 10px;'):
        with ui.row().classes('w-full gap-0 items-center place-content-between'):
            with ui.row().classes('items-center place-content-start gap-0'):
                ui.icon('square').classes('text-[#65B6FF] w-[6px] h-[20px]')
                ui.label('赵雨晨').classes('ml-2 font-bold text-[#333333] text-[18px]')
                ui.label('>').classes('ml-2 text-[#888888] text-[18px]')
                inputs.input_search_w40('搜索学生', on_enterkey=lambda e: ui.notify(e))
            with ui.row().classes('items-center place-content-end'):
                ui.button('打印', icon='img:/static/images/printer@2x.png', on_click=print_person_report) \
                    .classes('w-25 rounded-md text-white') \
                    .style('background-color: #27CACA !important; border-radius: 6px;')
                ui.button('下载', icon='img:/static/images/download@2x.png', on_click=download_person_report) \
                    .classes('w-25 rounded-md text-white') \
                    .style('background-color: #65B6FF !important; border-radius: 6px;')
        with ui.row().classes('w-full mt-2 items-center place-content-start'):
            ui.icon('img:/static/images/group_student@2x.png').classes('w-[40px] h-[40px]')
            ui.label('一(4)班').classes('ml-2 text-[#333333] text-[14px]')
        with ui.row().classes('w-full mt-2 gap-0 items-center place-content-start'):
            ui.icon('img:/static/images/subject@2x.png').classes('w-[40px] h-[40px]')
            ui.label('科目').classes('ml-2 text-[#888888] text-[14px]')
            ui.label('数学').classes('ml-2 text-[#008DFF] text-[14px]')
            ui.icon('img:/static/images/teacher@2x.png').classes('ml-5 w-[40px] h-[40px]')
            ui.label('任课老师').classes('ml-2 text-[#888888] text-[14px]')
            ui.label('张明华').classes('ml-2 text-[#008DFF] text-[14px]')
            ui.icon('img:/static/images/student@2x.png').classes('ml-5 w-[40px] h-[40px]')
            ui.label('学生人数').classes('ml-2 text-[#888888] text-[14px]')
            ui.label('46人').classes('ml-2 text-[#008DFF] text-[14px]')
            ui.icon('img:/static/images/calendar_2@2x.png').classes('ml-5 w-[40px] h-[40px]')
            ui.label('开始时间').classes('ml-2 text-[#888888] text-[14px]')
            ui.label('2024-01-08 08:00').classes('ml-2 text-[#008DFF] text-[14px]')
            ui.icon('img:/static/images/course_time_long@2x.png').classes('ml-5 w-[40px] h-[40px]')
            ui.label('课程时长').classes('ml-2 text-[#888888] text-[14px]')
            ui.label('45分钟').classes('ml-2 text-[#008DFF] text-[14px]')
    with ui.row().classes('w-full h-[150px] gap-0 mt-3 items-center justify-between'):
        with ui.card().classes('h-full p-2 items-center gap-0') \
            .props('flat no-shadow') \
            .style('background-color: #FFFFFF !important; border-radius: 10px; width: 29% !important;'):
            with ui.row().classes('size-full gap-0 items-center place-content-around') \
                .style('background-color: #E2F2FF !important; border-radius: 4px;'):
                with ui.column().classes('h-full gap-0 items-center place-content-center'):
                    ui.label('深度专注总时长').classes('text-[#333333] text-[18px]')
                    ui.label('30分钟').classes('text-[#333333] text-[30px]')
                ui.icon('img:/static/images/total_time_long@2x.png').classes('w-[70px] h-[70px]')
        with ui.card().classes('w-1/4 h-full p-2 items-center gap-0') \
            .props('flat no-shadow') \
            .style('background-color: #FFFFFF !important; border-radius: 10px; width: 29% !important;'):
            with ui.row().classes('size-full gap-0 items-center place-content-around') \
                .style('background-color: #F1F2FF !important; border-radius: 4px;'):
                with ui.column().classes('h-full gap-0 items-center place-content-center'):
                    ui.label('深度专注最长时间').classes('text-[#333333] text-[18px]')
                    ui.label('10分钟').classes('text-[#333333] text-[30px]')
                ui.icon('img:/static/images/max_time_long@2x.png').classes('w-[70px] h-[70px]')
        with ui.card().classes('w-1/4 h-full p-2 items-center gap-0') \
            .props('flat no-shadow') \
            .style('background-color: #FFFFFF !important; border-radius: 10px; width: 29% !important;'):
            with ui.row().classes('size-full gap-0 items-center place-content-around') \
                .style('background-color: #E8F9EA !important; border-radius: 4px;'):
                with ui.column().classes('h-full gap-0 items-center place-content-center'):
                    ui.label('坐姿不端正时间').classes('text-[#333333] text-[18px]')
                    ui.label('5分钟').classes('text-[#333333] text-[30px]')
                ui.icon('img:/static/images/inposture_time_long@2x.png').classes('w-[70px] h-[70px]')
    with ui.row().classes('w-full h-[400px] gap-0 mt-3 items-center justify-between'):
        with ui.column().classes('gap-0 p-[15px] items-center') \
            .style('background-color: #FFFFFF !important; border-radius: 10px; width: 30% !important; height: 100% !important;'):
            ui.label('专注度分布').classes('w-full font-bold text-[16px] text-[#333333]')
            with ui.row().classes('w-full mt-2 items-center place-content-start'):
                ui.icon('square').classes('text-[#65B6FF] w-4 h-4')
                ui.label('深度专注').classes('ml-1 text-[#333333] text-[12px]')
                ui.icon('square').classes('text-[#4D82FB] w-4 h-4 ml-5')
                ui.label('中专注度').classes('ml-1 text-[#333333] text-[12px]')
                ui.icon('square').classes('text-[#FFA137] w-4 h-4 ml-5')
                ui.label('浅专注度').classes('ml-1 text-[#333333] text-[12px]')
            with ui.card().classes('w-full mt-2 flex-1').props('flat no-shadow'):
                ui.echart({
                    'series': [
                        {
                            'type': 'pie',
                            'radius': ['30%', '60%'],
                            'label': {
                                'fontSize': 12,
                                'formatter': '{b}: {c}分钟',
                            },
                            'data': [
                                {'value': 23, 'name': '浅度专注', 'itemStyle': {'color': '#FFA137'}},
                                {'value': 52, 'name': '中度专注', 'itemStyle': {'color': '#4D82FB'}},
                                {'value': 45, 'name': '深度专注', 'itemStyle': {'color': '#65B6FF'}},
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
            .style('background-color: #FFFFFF !important; border-radius: 10px; width: 30% !important; height: 100% !important;'):
            with ui.row().classes('w-full h-[55px] items-center place-content-between'):
                ui.label('学习记录').classes('font-bold text-[16px] text-[#333333] self-center')
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
                                    'borderColor': '#71B4FF'
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
                }).classes('w-[50px] h-[50px] self-center')
            with ui.card().classes('w-full mt-2 flex-1').props('flat no-shadow'):
                ui.echart({
                    'tooltip': {
                        'trigger': 'axis',
                        'axisPointer': {
                            'type': 'shadow'
                        }
                    },
                    'grid': {
                        'left': '3%',
                        'right': '4%',
                        'top': '3%',
                        'bottom': '3%',
                        'containLabel': 1
                    },
                    'xAxis': {
                        'data': ['学习专注度', '坐姿管理', '学习连续性'],
                        'axisLabel': {
                            'inside': 0,
                            'color': '#333333',
                            'fontSize': 14,
                        },
                        'axisTick': {
                            'show': 0
                        },
                        'axisLine': {
                            'show': 0,
                            'color': '#65B6FF'
                        },
                    },
                    'yAxis': {
                        'axisLabel': {
                            'inside': 0,
                            'color': '#333333',
                            'fontSize': 14,
                        },
                        'axisTick': {
                            'show': 0
                        },
                        'axisLine': {
                            'show': 0,
                        },
                        'type': 'value'
                    },
                    
                    'series': [
                        {
                            'type': 'bar',
                            'max': 100,
                            'barWidth': '30%',
                            'showBackground': 1,
                            'itemStyle': {
                                'color': {
                                    'type': 'linear',
                                    'x': 0,
                                    'y': 0,
                                    'x2': 0,
                                    'y2': 1,
                                    'colorStops': [
                                        { 'offset': 0, 'color': '#D9EDFF' },
                                        { 'offset': 1, 'color': '#65B6FF' }
                                    ],
                                }
                            },
                            'data': [25,82,59]
                        }
                    ]
                }).classes('w-full h-full p-0 gap-0')
        with ui.column().classes('gap-0 p-[15px] items-center') \
            .style('background-color: #FFFFFF !important; border-radius: 10px; width: 30% !important; height: 100% !important;'):
                ui.label('学习状态详情').classes('font-bold text-[16px] text-[#333333] place-self-start')
                with ui.card().classes('w-full mt-2 flex-1').props('flat no-shadow'):
                    ui.echart({
                        'tooltip': {
                            'trigger': 'axis',
                            'axisPointer': {
                                'type': 'shadow'
                            }
                        },
                        'grid': {
                            'left': '3%',
                            'right': '4%',
                            'top': '3%',
                            'bottom': '3%',
                            'containLabel': 1
                        },
                        'xAxis': {
                            'axisTick': {
                                'show': 0
                            },
                            'type': 'category',
                            'data': ['09:06:12', '09:07:07', '09:08:02', '09:08:57', '09:09:52']
                        },
                        'yAxis': {
                            'type': 'value'
                        },
                        'series': [
                            {
                                'type': 'line',
                                'stack': 'Total',
                                'areaStyle': {},
                                'smooth': 1,
                                'min': 0,
                                'max': 100,
                                'data': [10, 15, 23, 30, 62],
                            },
                        ]
                    }).classes('w-full h-full')
        



def print_person_report() ->None:
    ui.notify('打印个人报告')

def download_person_report() ->None:
    ui.notify('下载个人报告')    
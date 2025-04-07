
from nicegui import ui
from components import tables, cards


def show_course_detail_page(course_id: int) -> None:
    with ui.row().classes('w-full h-[80px] px-[20px] mt-0 items-center place-content-between') \
        .style('background-color: #FFFFFF !important; border-radius: 10px;'):
        with ui.row().classes('h-full items-center gap-0'):
            ui.label('XX中学智能学习教室').classes('text-[20px] text-[#333333]')
            ui.label('代课老师: 王老师').classes('ml-10 text-[20px] text-[#888888]')
        with ui.row().classes('h-full items-center'):
            ui.button('批量导入', icon='img:/static/images/import@2x.png', on_click=import_students) \
                .classes('w-25 rounded-md text-white') \
                .style('background-color: #27CACA !important; border-radius: 6px;')
            ui.button('添加学生', icon='img:/static/images/add@2x.png', on_click=add_students) \
                .classes('w-25 rounded-md text-white') \
                .style('background-color: #65B6FF !important; border-radius: 6px;')
            
    row_number = ['A', 'B', 'C', 'D', 'E', 'F']
    with ui.card().classes('w-full mt-2 no-shadow') \
        .props('borderless') \
        .style('padding: 15px; background-color: #FFFFFF !important; border-radius: 10px;'):
        for i in row_number:
            with ui.row().classes('w-full items-center place-content-evenly'):
                ui.label(f'{i}排').classes('text-[14px] font-bold text-[#333333]')
                for j in range(1, 8):
                    seat_number = f'{i}-{j}'
                    students = {'seat_number': seat_number, 'name': '刘婷婷', 'status': 1}
                    cards.student_in_seat_card(students)
        
        with ui.row().classes('w-full gap-0 mt-5 item-center place-content-start'):
            ui.icon('square').classes('text-[#27CACA] w-4 h-4').style('border-radius: 2px;')
            ui.label('深度专注').classes('text-[14px] font-bold text-[#333333]')
            ui.icon('square').classes('text-[#FFC100] ml-2 w-4 h-4').style('border-radius: 2px;')
            ui.label('中度专注').classes('text-[14px] font-bold text-[#333333]')
            ui.icon('square').classes('text-[#EF4444] ml-2 w-4 h-4').style('border-radius: 2px;')
            ui.label('浅度专注').classes('text-[14px] font-bold text-[#333333]')
            ui.icon('img:/static/images/on_line.png').classes('ml-5 w-4 h-4')
            ui.label('设备在线').classes('text-[14px] font-bold text-[#333333]')
            ui.icon('img:/static/images/off_line.png').classes('ml-2 w-4 h-4')
            ui.label('设备离线').classes('text-[14px] font-bold text-[#333333]')
        with ui.card().classes('w-full p-5 mt-2 no-shadow') \
            .props('borderless') \
            .style('padding: 15px; background-color: #EFF3FC !important; border-radius: 10px;'):
                with ui.row().classes('w-full place-content-start'):
                    ui.label('学习状况:').classes('text-[16px] text-[#333333]')
                with ui.column().classes('w-full mt-3 place-content-start gap-1'):
                    with ui.row().classes('w-full'):
                        ui.label('10:46:05').classes('text-[14px] text-[#333333]')
                        ui.label('刘婷婷同学专注度下降到中度专注').classes('text-[14px] text-[#333333]')

# 导入学生
def import_students():
    ui.notify('import students')
#添加学生
def add_students():
    ui.notify('add students')

#
# @description: 显示课程报告页面
# @param {int} course_id 课程ID
# @return {*}
#
def show_course_report_page(course_id: int, show_person_report) -> None:
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
                ui.button('下载', icon='img:/static/images/download@2x.png', on_click=download_course_report) \
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
                        'data': ['8:00', '8:10', '8:20', '8:30', '8:40', '8:50', '9:00', '9:10', '9:20', '9:30']
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
                            'data': [5, 8, 13, 21, 34, 55]
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
                            'data': [3, 10, 12, 19, 23, 30]
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
                            'data': [8, 9, 18, 25, 27, 45]
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
                                    {'value': 8, 'name': '小于10分钟', 'itemStyle': {'color': '#674CF5'}},
                                    {'value': 10, 'name': '10-20分钟', 'itemStyle': {'color': '#29B479'}},
                                    {'value': 15, 'name': '20-30分钟', 'itemStyle': {'color': '#FBB80F'}},
                                    {'value': 12, 'name': '大于30分钟', 'itemStyle': {'color': '#F96B3E'}},
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
    with ui.column().classes('w-full mt-2 gap-0 p-[15px] items-center place-content-start') \
        .style('background-color: #FFFFFF !important; border-radius: 10px;'):
        ui.label('学习专注度排名').classes('w-full font-bold text-[16px] text-[#333333]')
        table_rows = [
            {'course_id': course_id, 'id': 1, 'sn': 1, 'name': '陈佳佳', 'gender': '0', 'deep_concentration': '40%', 'mid_concentration': '35%', 'low_concentration': '25%', 'operation': ''},
            {'course_id': course_id, 'id': 2, 'sn': 2, 'name': '王思思', 'gender': '0', 'deep_concentration': '39%', 'mid_concentration': '32%', 'low_concentration': '28%', 'operation': ''},
            {'course_id': course_id, 'id': 3, 'sn': 3, 'name': '李明明', 'gender': '1', 'deep_concentration': '35%', 'mid_concentration': '38%', 'low_concentration': '27%', 'operation': ''},
            {'course_id': course_id, 'id': 4, 'sn': 4, 'name': '张雨晨', 'gender': '0', 'deep_concentration': '33%', 'mid_concentration': '37%', 'low_concentration': '30%', 'operation': ''},
            {'course_id': course_id, 'id': 5, 'sn': 5, 'name': '刘子豪', 'gender': '1', 'deep_concentration': '32%', 'mid_concentration': '39%', 'low_concentration': '32%', 'operation': ''},
        ]
        tables.show_report_table(table_rows, show_person_report)

def print_course_report():
    ui.notify('print course report')

def download_course_report():
    ui.notify('download course report')


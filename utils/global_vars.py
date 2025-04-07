from nicegui import ui
from navigation import navigation_switcher, HOME_NAVIGATION
from typing import Optional

# Define global variables
header_title: Optional[ui.row] = None
course_container: Optional[ui.tab_panel] = None
tab_panels: Optional[ui.tab_panels] = None

def show_main_page_title() -> None:
    if header_title is not None:
        header_title.clear()
        with header_title:
            title = ui.label(navigation_switcher.get(HOME_NAVIGATION, '')).classes('place-self-center').style('font-size: 24px; color:#65B6FF')
            title.bind_text_from(tab_panels, 'value', lambda value: value.props["label"] if not isinstance(value, str) else value)

def show_course_detail_title(onback) -> None:
    if header_title is not None:
        header_title.clear()
        with header_title:
            ui.icon('img:/static/images/back@2x.png') \
                .classes('w-[24px] h-[24px]') \
                .on('click', onback)
            ui.label('课程管理 / ').classes('ml-2 text-[20px] text-[#333333]')
            ui.label('课程详情').classes('text-[20px] text-[#65B6FF]')

def show_report_title(onback) -> None:
    if header_title is not None:
        header_title.clear()
        with header_title:
            ui.icon('img:/static/images/back@2x.png') \
                .classes('w-[24px] h-[24px]') \
                .on('click', onback)
            ui.label('课程管理 / ').classes('ml-2 text-[20px] text-[#333333]')
            ui.label('学习专注度报告').classes('text-[20px] text-[#65B6FF]')

def show_person_report_title(onback) -> None:
    if header_title is not None:
        header_title.clear()
        with header_title:
            ui.icon('img:/static/images/back@2x.png') \
                .classes('w-[24px] h-[24px]') \
                .on('click', onback)
            ui.label('课程管理 / 学习专注度报告 / ').classes('ml-2 text-[20px] text-[#333333]')
            ui.label('个人报告').classes('text-[20px] text-[#65B6FF]')            

# General
APP_NAME = "乎感智慧学校"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Li guo qiang"
ALARM_RECORDS = "告警记录"
LOG_CONTENT = "日志内容"
DEVICE_MAC = "设备MAC"
DEVICE_NAME = "设备名称"
LOG_STATUS = "状态"
LOG_DATETIME = "时间"
OPERATION = "操作"

HOME_PAGE = "首页"
COURSE_PAGE = "课程管理"
DEVICE_PAGE = "设备管理"
LOGIN_PAGE = "登录"

string_resources = {
    'app_name': APP_NAME,
    'app_version': APP_VERSION,
    'app_author': APP_AUTHOR,
    'alarm_records': ALARM_RECORDS,
    'log_content': LOG_CONTENT,
    'device_mac': DEVICE_MAC,
    'device_name': DEVICE_NAME,
    'log_status': LOG_STATUS,
    'log_datetime': LOG_DATETIME,
    'operation': OPERATION,
    'home_page': HOME_PAGE,
    'course_page': COURSE_PAGE,
    'device_page': DEVICE_PAGE,
    'login_page': LOGIN_PAGE,
    'course_management': '课程管理',
    'device_management': '设备管理',
}

def get(key: str) -> str:
    """
    获取字符串资源
    :param key: 字符串资源的键
    :return: 对应的字符串资源
    """
    if key in string_resources:
        return string_resources[key]
    else:
        # 如果键不存在，返回默认值或抛出异常
        # raise KeyError(f"String resource '{key}' not found.")
        # 或者返回键本身作为默认值
        return ""  # 返回空字符串作为默认值
from dataclasses import dataclass
from datetime import datetime
import json
from typing import Any

import pytz
from api import api_manager


course_page_no: int = 1
course_page_size: int = 10
course_total_page: int = 1

@dataclass
class CourseDao:
    id: int
    classes: str
    subject: str
    teacher: str
    begin_time: str|None
    end_time: str|None
    duration: float
    status: int
    name_list: int
    student_num: int
    create_time: str
    
    def __init__(self, id=0, classes="", subject="", teacher="", begin_time=None, end_time=None, duration=0, status=-1, name_list=0, student_num = 0, create_time=""):
        self.id = id
        self.classes = classes
        self.subject = subject
        self.teacher = teacher
        self.begin_time = begin_time
        self.end_time = end_time
        self.duration = duration
        self.status = status
        self.name_list = name_list
        self.student_num = student_num
        if create_time == "":
            self.create_time = datetime.now(pytz.timezone('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S")
        else:
            self.create_time = create_time
    def from_json(self, json_data):
        self.id = json_data.get('id', 0)
        self.classes = json_data.get('classes', "")
        self.subject = json_data.get('subject', "")
        self.teacher = json_data.get('teacher', "")
        self.begin_time = json_data.get('begin_time', None)
        self.end_time = json_data.get('end_time', None)
        duration = json_data.get('duration', 0)
        self.duration = round(duration, 1) if isinstance(duration, float) else duration
        self.status = json_data.get('status', 0)
        self.name_list = json_data.get('name_list', 0)
        self.student_num = json_data.get('student_num', 0)
        self.create_time = json_data.get('create_time', "")
        

    def to_json(self):
        return json.dumps(self.__dict__, default=str)

    """
    function:
    description: 从服务器查询课程列表
    param {*} course
    return {*}
    """
    def get_course_by_id(self) -> tuple[int, str]:
        url = f"{api_manager.server_url}/course/queryCourseById"
        fields=[ \
            ("id", str(self.id)), \
        ]
        result = api_manager.api_https.request("GET", url=url, fields=fields)
        if result.status == 200:
            jobj = json.loads(result.data)
            if jobj["code"] == 200:
                self.from_json(jobj["data"])
                return 200, '查询课程成功'
            else:
                return jobj["code"], jobj["message"]
        else:
            return result.status, str(result.data)
    """
    function:
    description: 向服务器添加课程
    param {*} self
    return {*}
    """
    def add_course(self) -> tuple[bool, Any|str|None]:
        url = f"{api_manager.server_url}/course/addCourse"
        payload = self.to_json()
        status, ret = api_manager.post_to_svr(url, payload)
        if status:
            self.from_json(ret)
            return True, '添加课程成功'
        else:
            return status, ret

    """
    function:
    description: 向服务器更新课程
    param {*} self
    return {*}
    """
    def update_course(self) -> tuple[bool, Any|str|None]:
        # Logic to update an existing course in the database
        url = f"{api_manager.server_url}/course/editCourse"
        payload = self.to_json()
        status, ret = api_manager.post_to_svr(url, payload)
        if status:
            self.from_json(ret)
            return True, '更新课程成功'
        else:
            return status, ret

    def delete_course(self, ids: list[int]) -> tuple[bool, Any|str|None]:
        url = f"{api_manager.server_url}/course/delCourse"
        payload = json.dumps({"ids": ids})
        status, ret = api_manager.post_to_svr(url, payload)
        if status:
            return True, '删除课程成功'
        else:
            return status, ret

"""
function:
description: 从服务器查询课程列表
param {*} course
return {*}
"""
def get_all_courses(classes, subject, teacher, begin_time, status) -> tuple[int, str|list[CourseDao]]:
    url = f"{api_manager.server_url}/course/queryCourseList"
    fields=[ \
        ("pageNo", "1"), \
        ("pageSize", "10"),\
        ("classes", classes), \
        ("subject", subject), \
        ("teacher", teacher), \
        ("begin_time", begin_time), \
        ("status", status), \
    ]
    result = api_manager.api_https.request("GET", url=url, fields=fields)
    if result.status == 200:
        jobj = json.loads(result.data)
        if jobj["code"] == 200:
            global course_page_no
            global course_page_size
            global course_total_page
            course_page_no = jobj.get('pageNo', 1)
            course_page_size = jobj.get('pageSize', 10)
            course_total_page = jobj.get('totalPage', 1)
            datas = jobj.get('data', [])
            course_list = []
            for item in datas:
                course = CourseDao()
                course.from_json(item)
                course_list.append(course)
            return 200, course_list
        else:
            return jobj["code"], jobj["message"]
    else:
        return result.status, str(result.data)
#
# @dataclass
# class CourseStudentsDao:
# 定义课程学生数据访问对象
# 该类用于处理与课程学生相关的数据库操作

@dataclass
class CourseStudentsDao:
    id: int
    class_room_id: int
    seat_id: int
    course_id: int
    name: str
    gender: int # 性别 0:男 1:女
    create_time: str

    def __init__(self, id=0, class_room_id=0, seat_id=0, course_id=0, name="", gender=0, create_time=""):
        self.id = id
        self.class_room_id = class_room_id
        self.seat_id = seat_id
        self.course_id = course_id
        self.name = name
        self.gender = gender
        if create_time == "":
            self.create_time = datetime.now(pytz.timezone('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S")
        else:
            self.create_time = create_time

    def from_json(self, json_data):
        self.id = json_data.get('id', 0)
        self.class_room_id = json_data.get('class_room_id', "")
        self.seat_id = json_data.get('seat_id', "")
        self.course_id = json_data.get('course_id', "")
        self.name = json_data.get('name', "")
        self.gender = json_data.get('gender', "")
        self.create_time = json_data.get('create_time', "")
        

    def to_json(self):
        return json.dumps(self.__dict__, default=str)
    
    """
    function:
    description: 向服务器添加学生信息
    param {*} self
    return {*}
    """
    def add_students(self) -> tuple[bool, Any|str|None]:
        url = f"{api_manager.server_url}/course/addStudents"
        payload = self.to_json()
        status, ret = api_manager.post_to_svr(url, payload)
        if status:
            self.from_json(ret)
            return True, '添加成功'
        else:
            return status, ret
        
#
# @dataclass
# class StudentInSeatsDao
# 定义学生和座位的关系

@dataclass
class StudentInSeatsDao:
    class_room_id: int
    seat_id: int
    seat_no: str
    mac: str
    is_installed: int
    is_online: int
    student_id: int
    course_id: int
    name: str
    gender: int # 性别 0:男 1:女

    def __init__(
            self,
            class_room_id=0,
            seat_id=0, 
            seat_no="", 
            mac="", 
            is_installed=0, 
            is_online=0, 
            student_id=0, 
            course_id=0, 
            name = "", 
            gender=0
        ):
        self.class_room_id = class_room_id
        self.seat_id = seat_id
        self.seat_no = seat_no
        self.mac = mac
        self.is_installed = is_installed
        self.is_online = is_online
        self.student_id = student_id
        self.course_id = course_id
        self.name = name
        self.gender = gender

    def from_json(self, json_data):
        self.class_room_id = json_data.get('class_room_id', "")
        self.seat_id = json_data.get('seat_id', "")
        self.seat_no = json_data.get('seat_no', "")
        self.mac = json_data.get('mac', "")
        self.is_installed = json_data.get('is_installed', 0)
        self.is_online = json_data.get('is_online', 0)
        self.student_id = json_data.get('student_id', None)
        self.course_id = json_data.get('course_id', None)
        self.name = json_data.get('name', None)
        self.gender = json_data.get('gender', None)

def query_student_in_seat(class_room_id: int, course_id: int) -> tuple[int, str|list[StudentInSeatsDao]]:
    url = f"{api_manager.server_url}/course/queryStudentsInSeat"
    fields=[ \
        ("class_room_id", str(class_room_id)), \
        ("course_id", str(course_id)), \
    ]
    student_seats_list = list[StudentInSeatsDao]()
    result = api_manager.api_https.request("GET", url=url, fields=fields)
    if result.status == 200:
        jobj = json.loads(result.data)
        if jobj["code"] == 200:
            objs = jobj.get("data", [])
            for item in objs:
                student = StudentInSeatsDao()
                student.from_json(item)
                student_seats_list.append(student)
            return 200, student_seats_list
        else:
            return jobj["code"], jobj["message"]
    else:
        return result.status, str(result.data)
    

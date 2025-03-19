'''
Author: liguoqiang
Date: 2025-03-15 09:47:54
LastEditors: liguoqiang
LastEditTime: 2025-03-15 23:10:29
Description: 
'''
from nicegui import ui

# 添加自定义 表格CSS
ui.add_css('''
.table-header {
    background-color: #EBECF0; /* 设置表头背景颜色 */
    color: black; /* 设置表头文字颜色 */
    align-items: center; /* 设置表头文字居中 */
}
''')

def show_course_table(datas, show_monitor, show_report, show_delete) -> ui.table:
    table_columns = [
        {'name': 'id', 'label': '序号', 'field': 'id'},
        {'name': 'class', 'label': '班级', 'field': 'class'},
        {'name': 'subject', 'label': '科目', 'field': 'subject'},
        {'name': 'teacher', 'label': '教师', 'field': 'teacher'},
        {'name': 'start_time', 'label': '开始时间', 'field': 'start_time'},
        {'name': 'end_time', 'label': '结束时间', 'field': 'end_time'},
        {'name': 'status', 'label': '状态', 'field': 'status'},
        {'name': 'student_roster', 'label': '学生名单', 'field': 'student_roster'},
        {'name': 'operation', 'label': '操作', 'field': 'operation'}
    ]
    with ui.table(
        columns=table_columns,
        rows=datas,
        row_key='name',
        pagination={'rowsPerPage': 10, 'sortBy': 'id', 'page': 1}).classes('w-full') as table:
        table.add_slot('header', r'''
            <q-tr :props="props" class="table-header">
                <q-th v-for="col in props.cols" :key="col.name" :props="props">
                    {{ col.label }}
                </q-th>
            </q-tr>
        ''')
        table.add_slot('body-cell-status', r'''
            <q-td auto-width key="status" :props="props">
                <template v-if="props.row.status == 0">
                    未开始
                </template>
                <template v-else-if="props.row.status == 1">
                    进行中
                </template>
                <template v-else-if="props.row.status == 2">
                    已结束
                </template>
            </q-td>
        ''')
        table.add_slot('body-cell-operation', r'''
            <q-td auto-width key="operation" :props="props" class="item-left">
                <template v-if="props.row.status == 0">
                    <q-btn size="sm" color="yellow" round dense icon="visibility"
                        @click="() => $parent.$emit('show_monitor', props.row)"
                    />
                    <span style="display: inline-block; width: 5px;"></span>
                    <q-btn size="sm" color="warning" round dense icon="delete"
                        @click="() => $parent.$emit('show_delete', props.row)"
                    />
                </template>
                <template v-else-if="props.row.status == 1">
                    <q-btn size="sm" round dense icon="visibility"
                        @click="() => $parent.$emit('show_monitor', props.row)"
                    />
                </template>
                <template v-else-if="props.row.status == 2">
                    <q-btn size="sm" color="green" round dense icon="report"
                        @click="() => $parent.$emit('show_report', props.row)"
                    />
                </template>
            </q-td>
        ''')
        table.on('show_monitor', show_monitor)
        table.on('show_delete', show_delete)
        table.on('show_report', show_report)
    return table

def show_report_table(datas, show_person_report) -> ui.table:
    table_columns = [
        {'name': 'sn', 'label': '排名', 'field': 'sn', 'width': '10%'},
        {'name': 'name', 'label': '姓名', 'field': 'name', 'width': '10%'},
        {'name': 'gender', 'label': '性别', 'field': 'gender', 'width': '10%'},
        {'name': 'deep_concentration', 'label': '深度专注', 'field': 'deep_concentration', 'width': '15%'},
        {'name': 'mid_concentration', 'label': '中度专注', 'field': 'mid_concentration', 'width': '15%'},
        {'name': 'low_concentration', 'label': '浅度专注', 'field': 'low_concentration', 'width': '15%'},
        {'name': 'operation', 'label': '操作', 'field': 'operation', 'width': '20%'}
    ]
    with ui.table(
        columns=table_columns,
        rows=datas,
        row_key='name',
        pagination={'rowsPerPage': 10, 'sortBy': 'sn', 'page': 1}).classes('w-full') as table:
        table.add_slot('header', r'''
            <q-tr :props="props" class="table-header">
                <q-th v-for="col in props.cols" :key="col.name" :props="props" :style="`width: ${col.width};`">
                    {{ col.label }}
                </q-th>
            </q-tr>
        ''')
        table.add_slot('body-cell-sn', r'''
            <q-td auto-width key="sn" :props="props">  
                <template v-if="props.row.sn < 4">
                    <q-icon name="thumb_up" color="primary" />
                </template>
                <template v-else>
                    {{ props.row.sn }}
                </template>
            </q-td>
        ''')
        table.add_slot('body-cell-operation', r'''
            <q-td auto-width key="operation" :props="props">
                <q-btn size="sm" round dense icon="details"
                    @click="() => $parent.$emit('show_person_report', props.row)"
                />
            </q-td>
        ''')
        table.on('show_person_report', show_person_report)
    return table

def show_devices_table(datas, on_device_edit, on_device_delete) -> ui.table:
    columns = [
        {'name': 'sn', 'label': '序号', 'field': 'sn', 'width': '10%'},
        {'name': 'seat_number', 'label': '座位号', 'field': 'seat_number', 'width': '10%'},
        {'name': 'mac', 'label': '设备码', 'field': 'mac', 'width': '30%'},
        {'name': 'status', 'label': '状态', 'field': 'status', 'width': '10%'},
        {'name': 'online', 'label': '在线', 'field': 'online', 'width': '10%'},
        {'name': 'operation', 'label': '操作', 'field': 'operation', 'width': '20%'}
    ]
    with ui.table(
        columns=columns,
        rows=datas,
        row_key='name',
        selection='multiple',
        pagination={'rowsPerPage': 10, 'sortBy': 'sn', 'page': 1}).classes('w-full') as table:
        table.add_slot('header', r'''
            <q-tr :props="props" class="table-header">
                <q-th :style="`width: 10%;`" />
                <q-th v-for="col in props.cols" :key="col.name" :props="props" :style="`width: ${col.width};`">
                    {{ col.label }}
                </q-th>
            </q-tr>
        ''')
        table.add_slot('body-cell-status', r'''
            <q-td auto-width key="status" :props="props">
                <template v-if="props.row.status == 0">
                    未安装
                </template>
                <template v-else>
                    已安装
                </template>
            </q-td>
        ''')
        table.add_slot('body-cell-online', r'''
            <q-td auto-width key="online" :props="props">
                <template v-if="props.row.online == 0">
                    离线
                </template>
                <template v-else>
                    在线
                </template>
            </q-td>
        ''')
        table.add_slot('body-cell-operation', r'''
            <q-td auto-width key="operation" :props="props">
                <q-btn size="sm" round dense icon="edit"
                    @click="() => $parent.$emit('on_device_edit', props.row)"
                />
                <span style="display: inline-block; width: 5px;"></span>
                <q-btn size="sm" color="warning" round dense icon="delete"
                    @click="() => $parent.$emit('on_device_delete', props.row)"
                />
            </q-td>
        ''')
        table.on('on_device_edit', on_device_edit)
        table.on('on_device_delete', on_device_delete)
    return table
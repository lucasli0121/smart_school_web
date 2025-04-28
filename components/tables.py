'''
Author: liguoqiang
Date: 2025-03-15 09:47:54
LastEditors: liguoqiang
LastEditTime: 2025-03-15 23:10:29
Description: 
'''
from nicegui import ui

# 添加自定义 表格CSS
# ui.add_css('''
# .table-header {
#     background-color: rgba(101,182,255,0.39); /* 设置表头背景颜色 */
#     color: black; /* 设置表头文字颜色 */
# }
# ''')

def show_course_table(datas, show_monitor, show_report, show_delete) -> ui.table:
    table_columns = [
        {'name': 'id', 'label': '序号', 'field': 'id', 'width': '5%', 'align': 'center'},
        {'name': 'classes', 'label': '班级', 'field': 'classes', 'width': '10%', 'align': 'center'},
        {'name': 'subject', 'label': '科目', 'field': 'subject', 'width': '10%', 'align': 'center'},
        {'name': 'teacher', 'label': '教师', 'field': 'teacher', 'width': '10%', 'align': 'center'},
        {'name': 'begin_time', 'label': '开始时间', 'field': 'begin_time', 'width': '15%', 'align': 'center'},
        {'name': 'end_time', 'label': '结束时间', 'field': 'end_time', 'width': '15%', 'align': 'center'},
        {'name': 'status', 'label': '状态', 'field': 'status', 'width': '10%', 'align': 'center'},
        {'name': 'name_list', 'label': '学生名单', 'field': 'name_list', 'width': '10%', 'align': 'center'},
        {'name': 'operation', 'label': '操作', 'field': 'operation', 'width': '10%', 'align': 'center'}
    ]
    with ui.table(
        columns=table_columns,
        rows=datas,
        row_key='id',
        selection='multiple',
        pagination={'rowsPerPage': 10, 'sortBy': 'id', 'page': 1}) \
            .props('table-header-style="color: white; font-size: 16px; background-color: #65B6FF;"') \
            .classes('w-full mt-2 gap-0') \
            .style('border: 1px solid #ECECEC; border-radius: 10px 10px 0px 0px;') as table:
        # table.add_slot('header', r'''
        #     <q-tr :props="props" class="table-header">
        #         <q-th v-for="col in props.cols" :key="col.name" :props="props">
        #             {{ col.label }}
        #         </q-th>
        #     </q-tr>
        # ''')
        table.props('v-model:selected="selected"')
        
        table.add_slot('body-cell-status', r'''
            <q-td auto-width key="status" :props="props" style="">
                <template v-if="props.row.status == 0">
                    <div style="text-align: center; width: 50px; height: 30px; line-height: 30px; background-color: #C5C5C5; border-radius: 17px;">
                       <font style="font-size: 12px; color: white;">未开始</font>
                    </div>
                </template>
                <template v-else-if="props.row.status == 1">
                    <div style="text-align: center; width: 50px; height: 30px; line-height: 30px; background-color: #65B6FF; border-radius: 17px;">
                       <font style="font-size: 12px; color: white;">进行中</font>
                    </div>
                </template>
                <template v-else-if="props.row.status == 2">
                    <div style="text-align: center; width: 50px; height: 30px; line-height: 30px; background-color: #27CACA; border-radius: 17px;">
                       <font style="font-size: 12px; color: white;">已结束</font>
                    </div>
                </template>
            </q-td>
        ''')
        table.add_slot('body-cell-name_list', r'''
            <q-td auto-width key="name_list" :props="props" style="">
                <template v-if="props.row.name_list == 0">
                    <font style="font-size: 12px; color: #FF4D4D;">未添加</font>
                </template>
                <template v-else-if="props.row.name_list == 1">
                    <font style="font-size: 12px; color: #333333;">已添加</font>
                </template>
            </q-td>
        ''')
        table.add_slot('body-cell-operation', r'''
            <q-td auto-width key="operation" :props="props" class="item-left">
                <template v-if="props.row.status == 0">
                    <q-btn size="sm" flat round dense icon="img:/static/images/visible.png"
                        @click="() => $parent.$emit('show_monitor', props.row)"
                    />
                    <span style="display: inline-block; width: 5px;"></span>
                    <q-btn size="sm" flat round dense icon="img:/static/images/delete_mini.png"
                        @click="() => $parent.$emit('show_delete', props.row)"
                    />
                </template>
                <template v-else-if="props.row.status == 1">
                    <q-btn size="sm" flat round dense icon="img:/static/images/visible.png"
                        @click="() => $parent.$emit('show_monitor', props.row)"
                    />
                </template>
                <template v-else-if="props.row.status == 2">
                    <q-btn size="sm" flat round dense icon="img:/static/images/report_mini.png"
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
        {'name': 'sn', 'label': '排名', 'field': 'sn', 'width': '10%', 'align': 'center'},
        {'name': 'name', 'label': '姓名', 'field': 'name', 'width': '10%', 'align': 'center'},
        {'name': 'gender', 'label': '性别', 'field': 'gender', 'width': '10%', 'align': 'center'},
        {'name': 'deep_concentration', 'label': '深度专注', 'field': 'deep_concentration', 'width': '15%', 'align': 'center'},
        {'name': 'mid_concentration', 'label': '中度专注', 'field': 'mid_concentration', 'width': '15%', 'align': 'center'},
        {'name': 'low_concentration', 'label': '浅度专注', 'field': 'low_concentration', 'width': '15%', 'align': 'center'},
        {'name': 'operation', 'label': '操作', 'field': 'operation', 'width': '20%', 'align': 'center'}
    ]
    with ui.table(
        columns=table_columns,
        rows=datas,
        row_key='name',
        pagination={'rowsPerPage': 10, 'sortBy': 'sn', 'page': 1}) \
            .props('table-header-style="color: white; font-size: 16px; background-color: #65B6FF;" flat no-shadow') \
            .classes('w-full mt-2 gap-0') \
            .style('border: 1px solid #ECECEC; border-radius: 10px 10px 0px 0px;') as table:
        
        table.props('visible-columns="[\'sn\', \'name\', \'gender\', \'deep_concentration\', \'mid_concentration\', \'low_concentration\', \'operation\']"')

        table.add_slot('body-cell-sn', r'''
            <q-td auto-width key="sn" :props="props">  
                <template v-if="props.row.sn == 1">
                    <q-icon name="img:/static/images/sort_1@2x.png" />
                </template>
                <template v-if="props.row.sn == 2">
                    <q-icon name="img:/static/images/sort_2@2x.png" />
                </template>
                <template v-if="props.row.sn == 3">
                    <q-icon name="img:/static/images/sort_3@2x.png" />
                </template>
                <template v-if="props.row.sn > 3">
                    {{ props.row.sn }}
                </template>
            </q-td>
        ''')
        table.add_slot('body-cell-operation', r'''
            <q-td auto-width key="operation" :props="props">
                <q-btn size="sm" flat round dense icon="img:/static/images/visible@2x.png"
                    @click="() => $parent.$emit('show_person_report', props.row)"
                />
            </q-td>
        ''')
        table.on('show_person_report', show_person_report)
    return table

def show_devices_table(datas, on_device_edit, on_device_delete) -> ui.table:
    columns = [
        {'name': 'sn', 'label': '序号', 'field': 'sn', 'width': '5%', 'align': 'center'},
        {'name': 'seat_no', 'label': '座位号', 'field': 'seat_no', 'width': '5%', 'align': 'center'},
        {'name': 'mac', 'label': '设备码', 'field': 'mac', 'width': '10%', 'align': 'center'},
        {'name': 'is_installed', 'label': '状态', 'field': 'is_installed', 'width': '10%', 'align': 'center'},
        {'name': 'is_online', 'label': '在线', 'field': 'is_online', 'width': '10%', 'align': 'center'},
        {'name': 'operation', 'label': '操作', 'field': 'operation', 'width': '20%', 'align': 'center'}
    ]
    with ui.table(
        columns=columns,
        rows=datas,
        row_key='seat_no',
        selection='multiple',
        pagination={'rowsPerPage': 10, 'sortBy': 'sn', 'page': 1}) \
            .props('table-header-style="color: white; font-size: 16px; background-color: #65B6FF;"') \
            .classes('w-full mt-2 gap-0 no-shadow') \
            .style('border: 1px solid #ECECEC; border-radius: 10px 10px 0px 0px;') as table:
        table.props('v-model:selected="selected"')
        # table.add_slot('header', r'''
        #     <q-tr :props="props" class="table-header">
        #         <q-th :style="`width: 10%;`" />
        #         <q-th v-for="col in props.cols" :key="col.name" :props="props" :style="`width: ${col.width};`">
        #             {{ col.label }}
        #         </q-th>
        #     </q-tr>
        # ''')
        table.add_slot('body-cell-is_installed', r'''
            <q-td auto-width key="is_installed" :props="props">
                <template v-if="props.row.is_installed == 0">
                    <div style="text-align: center; width: 50px; height: 30px; line-height: 30px; background-color: #FF8787; border-radius: 17px;">
                       <font style="font-size: 12px; color: white;">未安装</font>
                    </div>
                </template>
                <template v-else>
                    <div style="text-align: center; width: 50px; height: 30px; line-height: 30px; background-color: #27CACA; border-radius: 17px;">
                       <font style="font-size: 12px; color: white;">已安装</font>
                    </div>
                </template>
            </q-td>
        ''')
        table.add_slot('body-cell-is_online', r'''
            <q-td auto-width key="is_online" :props="props">
                <template v-if="props.row.is_online == -1">
                    <div style="text-align: center; width: 50px; height: 30px; line-height: 30px; background-color: #FF8787; border-radius: 17px;">
                       <font style="font-size: 12px; color: white;">未绑定</font>
                    </div>
                </template>
                <template v-if="props.row.is_online == 0">
                    <div style="text-align: center; width: 50px; height: 30px; line-height: 30px; background-color: #C5C5C5; border-radius: 17px;">
                       <font style="font-size: 12px; color: white;">离线</font>
                    </div>
                </template>
                <template v-else>
                    <div style="text-align: center; width: 50px; height: 30px; line-height: 30px; background-color: #27CACA; border-radius: 17px;">
                       <font style="font-size: 12px; color: white;">在线</font>
                    </div>
                </template>
            </q-td>
        ''')
        table.add_slot('body-cell-operation', r'''
            <q-td auto-width key="operation" :props="props">
                <!--
                <q-btn size="sm" round dense icon="edit"
                    @click="() => $parent.$emit('on_device_edit', props.row)"
                />
                <span style="display: inline-block; width: 5px;"></span>
                -->
                <q-btn size="sm" flat round dense icon="img:/static/images/delete_mini.png"
                    @click="() => $parent.$emit('on_device_delete', props.row)"
                />
            </q-td>
        ''')
        table.on('on_device_edit', on_device_edit)
        table.on('on_device_delete', on_device_delete)
    return table
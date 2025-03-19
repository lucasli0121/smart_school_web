'''
Author: liguoqiang
Date: 2025-03-04 23:11:35
LastEditors: liguoqiang
LastEditTime: 2025-03-04 23:39:40
Description: 
'''
import pytest
from nicegui import ui
import dialogs
from dialogs.alarm_records import alarm_records

@pytest.mark.usefixtures("dialogs")
def test_alarm_records():
    alarm_records()
    ui.run()
    assert True
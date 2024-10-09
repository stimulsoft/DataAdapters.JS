"""
Stimulsoft.Reports.JS
Version: 2024.4.1
Build date: 2024.10.08
License: https://www.stimulsoft.com/en/licensing/reports
"""

from enum import Enum


class StiBaseEventType(Enum):

    NONE = None
    BEGIN_PROCESS_DATA = 'BeginProcessData'
    END_PROCESS_DATA = 'EndProcessData'


### Helpers

    @staticmethod
    def getValues(none = False):
        return [enum.value for enum in StiBaseEventType if none or enum.value != None]

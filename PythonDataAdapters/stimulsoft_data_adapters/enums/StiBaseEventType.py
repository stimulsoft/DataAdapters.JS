"""
Stimulsoft.Reports.JS
Version: 2025.2.1
Build date: 2025.03.20
License: https://www.stimulsoft.com/en/licensing/reports
"""

from enum import Enum


class StiBaseEventType(Enum):

    NONE = None
    DATABASE_CONNECT = 'DatabaseConnect'
    BEGIN_PROCESS_DATA = 'BeginProcessData'
    END_PROCESS_DATA = 'EndProcessData'


### Helpers

    @staticmethod
    def getValues(none = False):
        return [enum.value for enum in StiBaseEventType if none or enum.value != None]

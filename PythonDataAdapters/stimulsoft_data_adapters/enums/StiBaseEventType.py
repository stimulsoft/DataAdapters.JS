"""
Stimulsoft.Reports.JS
Version: 2025.1.6
Build date: 2025.02.28
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

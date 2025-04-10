"""
Stimulsoft.Reports.JS
Version: 2025.2.2
Build date: 2025.04.08
License: https://www.stimulsoft.com/en/licensing/reports
"""

from enum import Enum


class StiDataType(Enum):

    NONE: None
    JAVASCRIPT = 'text/javascript'
    JSON = 'application/json'
    XML = 'application/xml'
    HTML = 'text/html'
    CSV = "text/csv"
    TEXT = "text/plain"


### Helpers

    @staticmethod
    def getValues():
        return [enum.value for enum in StiDataType if enum.value != None]
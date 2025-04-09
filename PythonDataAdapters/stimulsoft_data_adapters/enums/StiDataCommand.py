"""
Stimulsoft.Reports.JS
Version: 2025.2.2
Build date: 2025.04.08
License: https://www.stimulsoft.com/en/licensing/reports
"""

from enum import Enum


class StiDataCommand(Enum):

    NONE = None
    GET_SUPPORTED_ADAPTERS = 'GetSupportedAdapters'
    GET_SCHEMA = 'GetSchema'
    GET_DATA = 'GetData'
    TEST_CONNECTION = 'TestConnection'
    RETRIEVE_SCHEMA = 'RetrieveSchema'
    EXECUTE = 'Execute'
    EXECUTE_QUERY = 'ExecuteQuery'


### Helpers

    @staticmethod
    def getValues():
        return [enum.value for enum in StiDataCommand if enum.value != None]
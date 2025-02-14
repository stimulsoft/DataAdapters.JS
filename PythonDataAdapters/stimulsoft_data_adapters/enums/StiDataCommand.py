"""
Stimulsoft.Reports.JS
Version: 2025.1.5
Build date: 2025.02.11
License: https://www.stimulsoft.com/en/licensing/reports
"""

from enum import Enum


class StiDataCommand(Enum):

    NONE = None
    GET_SUPPORTED_ADAPTERS = 'GetSupportedAdapters'
    TEST_CONNECTION = 'TestConnection'
    RETRIEVE_SCHEMA = 'RetrieveSchema'
    EXECUTE = 'Execute'
    EXECUTE_QUERY = 'ExecuteQuery'


### Helpers

    @staticmethod
    def getValues():
        return [enum.value for enum in StiDataCommand if enum.value != None]
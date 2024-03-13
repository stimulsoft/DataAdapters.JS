"""
Stimulsoft.Reports.JS
Version: 2024.2.2
Build date: 2024.03.11
License: https://www.stimulsoft.com/en/licensing/reports
"""

from typing import Final


class StiDataCommand:
    GET_SUPPORTED_ADAPTERS: Final = 'GetSupportedAdapters'
    TEST_CONNECTION: Final = 'TestConnection'
    RETRIEVE_SCHEMA: Final = 'RetrieveSchema'
    EXECUTE: Final = 'Execute'
    EXECUTE_QUERY: Final = 'ExecuteQuery'

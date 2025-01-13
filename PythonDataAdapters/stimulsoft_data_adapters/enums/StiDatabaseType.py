"""
Stimulsoft.Reports.JS
Version: 2025.1.3
Build date: 2025.01.09
License: https://www.stimulsoft.com/en/licensing/reports
"""

from enum import Enum


class StiDatabaseType(Enum):

    NONE = None
    MYSQL = 'MySQL'
    MSSQL = 'MS SQL'
    POSTGRESQL = 'PostgreSQL'
    FIREBIRD = 'Firebird'
    ORACLE = 'Oracle'
    ODBC = 'ODBC'
    MONGODB = 'MongoDB'


### Helpers

    @staticmethod
    def getValues():
        return [enum.value for enum in StiDatabaseType if enum.value != None]
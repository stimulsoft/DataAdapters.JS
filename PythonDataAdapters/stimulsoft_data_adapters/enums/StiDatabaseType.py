"""
Stimulsoft.Reports.JS
Version: 2024.4.2
Build date: 2024.10.16
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
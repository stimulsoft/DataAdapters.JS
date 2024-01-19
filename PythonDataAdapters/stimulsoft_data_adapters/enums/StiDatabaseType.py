"""
Stimulsoft.Reports.JS
Version: 2024.1.3
Build date: 2024.01.18
License: https://www.stimulsoft.com/en/licensing/reports
"""

from typing import Final


class StiDatabaseType:
    MYSQL: Final = 'MySQL'
    MSSQL: Final = 'MS SQL'
    POSTGRESQL: Final = 'PostgreSQL'
    FIREBIRD: Final = 'Firebird'
    ORACLE: Final = 'Oracle'
    ODBC: Final = 'ODBC'
    MONGODB: Final = 'MongoDB'

    def getTypes():
        return [getattr(StiDatabaseType, field) for field in dir(StiDatabaseType) if not callable(getattr(StiDatabaseType, field)) and not field.startswith('__')]
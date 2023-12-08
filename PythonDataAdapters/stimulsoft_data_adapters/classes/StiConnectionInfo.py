"""
Stimulsoft.Reports.JS
Version: 2024.1.1
Build date: 2023.12.08
License: https://www.stimulsoft.com/en/licensing/reports
"""

class StiConnectionInfo:
    """All database connection information taken from the connection string."""

    driver: str = ''
    host: str = ''
    port: int = 0
    database: str = ''
    userId: str = ''
    password: str = ''
    charset: str = ''
    privilege: str = ''
    dataPath: str = ''
    schemaPath: str = ''
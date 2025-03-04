"""
Stimulsoft.Reports.JS
Version: 2025.1.6
Build date: 2025.02.28
License: https://www.stimulsoft.com/en/licensing/reports
"""

from ..classes.StiConnectionInfo import StiConnectionInfo
from ..enums import StiDatabaseType
from .StiEventArgs import StiEventArgs


class StiConnectionEventArgs(StiEventArgs):

    database = StiDatabaseType.NONE
    """[enum] The type of the current database connection."""

    driver: str = None
    """Driver used for connection."""

    info: StiConnectionInfo = None
    """Information about the current connection."""

    link: object = None
    """Database connection identifier."""


### Constructor

    def __init__(self, database: StiDatabaseType, driver: str, info: StiConnectionInfo):
        super().__init__()

        self.database = database
        self.driver = driver
        self.info = info


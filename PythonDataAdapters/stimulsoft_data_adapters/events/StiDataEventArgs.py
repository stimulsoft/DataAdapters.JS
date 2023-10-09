"""
Stimulsoft.Reports.JS
Version: 2023.4.1
Build date: 2023.10.06
License: https://www.stimulsoft.com/en/licensing/reports
"""

from .StiEventArgs import StiEventArgs
from ..classes.StiDataResult import StiDataResult

class StiDataEventArgs(StiEventArgs):

    command: str = None
    """The current command for the data adapter. The supported commands are in the 'StiDataCommand' enum."""

    database: str = None
    """The database type for which the command will be executed. The supported database types are in the 'StiDatabaseType' enum."""

    connection: str = None
    """The name of the current database connection."""

    dataSource: str = None
    """The name of the current data source."""

    connectionString: str = None
    """The connection string for the current data source."""

    queryString: str = None
    """The SQL query that will be executed to get the data array of the current data source."""

    parameters: list = None
    """A set of parameters for the current SQL query."""

    result: StiDataResult = None
    """The result of executing an event handler request."""
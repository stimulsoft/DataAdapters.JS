"""
Stimulsoft.Reports.JS
Version: 2024.1.3
Build date: 2024.01.18
License: https://www.stimulsoft.com/en/licensing/reports
"""

from ..classes.StiDataResult import StiDataResult
from ..classes.StiParameter import StiParameter
from .StiEventArgs import StiEventArgs


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

    parameters: dict[str, StiParameter] = None
    """A set of parameters for the current SQL query."""

    result: StiDataResult = None
    """The result of executing an event handler request."""
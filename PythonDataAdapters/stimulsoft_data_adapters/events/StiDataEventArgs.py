"""
Stimulsoft.Reports.JS
Version: 2025.1.2
Build date: 2024.12.19
License: https://www.stimulsoft.com/en/licensing/reports
"""

from ..classes.StiDataResult import StiDataResult
from ..classes.StiParameter import StiParameter
from ..enums import StiDatabaseType, StiDataCommand
from .StiEventArgs import StiEventArgs


class StiDataEventArgs(StiEventArgs):

    command = StiDataCommand.NONE
    """[enum] The current command for the data adapter."""

    database = StiDatabaseType.NONE
    """[enum] The database type for which the command will be executed."""

    connection: str = None
    """The name of the current database connection."""

    dataSource: str = None
    """The name of the current data source."""

    connectionString: str = None
    """The connection string for the current data source."""

    queryString: str = None
    """The SQL query that will be executed to get the data array of the current data source."""

    maxDataRows: int = None
    """The maximum number of data rows. The value is taken from the designer's options for the dashboard in design mode."""

    parameters: dict[str, StiParameter] = None
    """A set of parameters for the current SQL query."""

    result: StiDataResult = None
    """The result of executing an event handler request."""
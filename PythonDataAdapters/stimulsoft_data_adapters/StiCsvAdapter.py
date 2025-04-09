"""
Stimulsoft.Reports.JS
Version: 2025.2.2
Build date: 2025.04.08
License: https://www.stimulsoft.com/en/licensing/reports
"""

from .enums.StiDatabaseType import StiDatabaseType
from .enums.StiDataType import StiDataType
from .StiFileAdapter import StiFileAdapter


class StiCsvAdapter(StiFileAdapter):
    
### Properties

    version = '2025.2.1'
    """Current version of the data adapter."""

    checkVersion = True
    """Sets the version matching check on the server and client sides."""

    type = StiDatabaseType.CSV
    dataType = StiDataType.CSV

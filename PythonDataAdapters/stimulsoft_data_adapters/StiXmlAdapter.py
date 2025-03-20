"""
Stimulsoft.Reports.JS
Version: 2025.2.1
Build date: 2025.03.20
License: https://www.stimulsoft.com/en/licensing/reports
"""

from .enums.StiDatabaseType import StiDatabaseType
from .enums.StiDataType import StiDataType
from .StiFileAdapter import StiFileAdapter


class StiXmlAdapter(StiFileAdapter):
    
### Properties

    version = '2025.1.6'
    """Current version of the data adapter."""

    checkVersion = True
    """Sets the version matching check on the server and client sides."""

    type = StiDatabaseType.XML
    dataType = StiDataType.XML

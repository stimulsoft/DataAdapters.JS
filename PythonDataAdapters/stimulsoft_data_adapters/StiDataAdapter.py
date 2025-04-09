"""
Stimulsoft.Reports.JS
Version: 2025.2.2
Build date: 2025.04.08
License: https://www.stimulsoft.com/en/licensing/reports
"""

from __future__ import annotations

import typing

from pyodbc import Connection

from .classes.StiDataResult import StiDataResult
from .classes.StiFunctions import StiFunctions
from .enums.StiDatabaseType import StiDatabaseType

if typing.TYPE_CHECKING:
    from .classes.StiBaseHandler import StiBaseHandler


class StiDataAdapter:

### Properties

    version = '2025.2.1'
    """Current version of the data adapter."""

    checkVersion = False
    """Sets the version matching check on the server and client sides."""

    handler: StiBaseHandler = None
    
    type = StiDatabaseType.NONE
    """The type of database processed by the data adapter."""

    driverName: str = None
    """The name of the current Python data driver."""

    connectionString: str = None
    """The connection string or URL for the current data source."""

    connectionLink: Connection = None
    """Link to the database connection driver."""


### Methods

    def connect(self):
        return StiDataResult.getSuccess().getDataAdapterResult(self)
    
    def disconnect(self):
        if self.connectionLink != None:
            self.connectionLink.close()
        self.connectionLink = None

    def test(self):
        result = self.connect()
        if result.success:
            self.disconnect()
        return result
    
    def process(self):
        return False

    def getDataResult(self, queryString: str, maxDataRows: int = -1) -> StiDataResult:
        return StiDataResult.getSuccess().getDataAdapterResult(self)
    

### Helpers

    @staticmethod
    def getDataAdapter(database: StiDatabaseType, connectionString: str):
        if database == StiDatabaseType.MYSQL:
            from .StiMySqlAdapter import StiMySqlAdapter
            return StiMySqlAdapter(connectionString)
        
        elif database == StiDatabaseType.MSSQL:
            from .StiMsSqlAdapter import StiMsSqlAdapter
            return StiMsSqlAdapter(connectionString)
        
        elif database == StiDatabaseType.FIREBIRD:
            from .StiFirebirdAdapter import StiFirebirdAdapter
            return StiFirebirdAdapter(connectionString)
        
        elif database == StiDatabaseType.POSTGRESQL:
            from .StiPostgreSqlAdapter import StiPostgreSqlAdapter
            return StiPostgreSqlAdapter(connectionString)
        
        elif database == StiDatabaseType.ORACLE:
            from .StiOracleAdapter import StiOracleAdapter
            return StiOracleAdapter(connectionString)
        
        elif database == StiDatabaseType.ODBC:
            from .StiOdbcAdapter import StiOdbcAdapter
            return StiOdbcAdapter(connectionString)
        
        elif database == StiDatabaseType.MONGODB:
            from .StiMongoDbAdapter import StiMongoDbAdapter
            return StiMongoDbAdapter(connectionString)
        
        elif database == StiDatabaseType.XML:
            from .StiXmlAdapter import StiXmlAdapter
            return StiXmlAdapter(connectionString)
        
        elif database == StiDatabaseType.JSON:
            from .StiJsonAdapter import StiJsonAdapter
            return StiJsonAdapter(connectionString)
        
        elif database == StiDatabaseType.CSV:
            from .StiCsvAdapter import StiCsvAdapter
            return StiCsvAdapter(connectionString)
        
        return None
    

### Constructor
    
    def __init__(self, connectionString: str):
        self.connectionString = connectionString.strip() if not StiFunctions.isNullOrEmpty(connectionString) else None
        self.process()
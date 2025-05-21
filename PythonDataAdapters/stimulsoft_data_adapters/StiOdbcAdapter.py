"""
Stimulsoft.Reports.JS
Version: 2025.2.4
Build date: 2025.05.19
License: https://www.stimulsoft.com/en/licensing/reports
"""

import pyodbc
from pyodbc import Connection

from .classes.StiDataResult import StiDataResult
from .enums import StiDatabaseType
from .events.StiConnectionEventArgs import StiConnectionEventArgs
from .StiSqlAdapter import StiSqlAdapter


class StiOdbcAdapter(StiSqlAdapter):

### Properties

    version = '2025.2.3'
    """Current version of the data adapter."""

    checkVersion = True
    """Sets the version matching check on the server and client sides."""
    
    connectionLink: Connection
    type = StiDatabaseType.ODBC
    driverName = 'pyodbc'


### Methods

    def connect(self):
        try:
            args = StiConnectionEventArgs(self.handler.request, self.type, self.driverName, self.connectionInfo)
            self.handler.onDatabaseConnect(args)

            if args.link != None:
                self.connectionLink = args.link
            else:    
                self.connectionLink = pyodbc.connect(self.connectionString)
                if self.connectionInfo.charset:
                    self.connectionLink.setdecoding(pyodbc.SQL_CHAR, self.connectionInfo.charset)
                    self.connectionLink.setdecoding(pyodbc.SQL_WCHAR, self.connectionInfo.charset)
        except Exception as e:
            return StiDataResult.getError(str(e)).getDataAdapterResult(self)
        
        return StiDataResult.getSuccess().getDataAdapterResult(self)
    
    def process(self):
        if super().process():
            return True

        parameterNames = {
            'driver': ['driver'],
            'userId': ['uid', 'user', 'username', 'userid', 'user id'],
            'password': ['pwd', 'password']
        }

        return self.processParameters(parameterNames)
    
    
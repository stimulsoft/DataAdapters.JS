"""
Stimulsoft.Reports.JS
Version: 2025.1.5
Build date: 2025.02.11
License: https://www.stimulsoft.com/en/licensing/reports
"""

import pyodbc
from pyodbc import Connection

from .classes.StiDataResult import StiDataResult
from .enums import StiDatabaseType
from .events.StiConnectionEventArgs import StiConnectionEventArgs
from .StiDataAdapter import StiDataAdapter


class StiOdbcAdapter(StiDataAdapter):

### Properties

    version = '2025.1.4'
    checkVersion = True
    connectionLink: Connection
    type = StiDatabaseType.ODBC
    driverName = 'pyodbc'


### Methods

    def connect(self):
        try:
            args = StiConnectionEventArgs(self.type, self.driverName, self.connectionInfo)
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
    
    
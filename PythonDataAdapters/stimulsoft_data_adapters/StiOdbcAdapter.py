"""
Stimulsoft.Reports.JS
Version: 2024.3.1
Build date: 2024.06.13
License: https://www.stimulsoft.com/en/licensing/reports
"""

import pyodbc
from pyodbc import Connection

from .classes.StiDataResult import StiDataResult
from .StiDataAdapter import StiDataAdapter


class StiOdbcAdapter(StiDataAdapter):

### Properties

    version = '2024.3.1'
    checkVersion = True
    connectionLink: Connection


### Methods

    def connect(self):
        try:
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
    
    
"""
Stimulsoft.Reports.JS
Version: 2023.4.2
Build date: 2023.10.18
License: https://www.stimulsoft.com/en/licensing/reports
"""

from .StiDataAdapter import StiDataAdapter
from .classes.StiDataResult import StiDataResult
import pyodbc
from pyodbc import Connection

class StiOdbcAdapter(StiDataAdapter):
    version: str = '2023.4.2'
    checkVersion: bool = True
    connectionLink: Connection

    def connect(self):
        try:
            self.connectionLink = pyodbc.connect(self.connectionString)
            if (self.connectionInfo.charset):
                self.connectionLink.setdecoding(pyodbc.SQL_CHAR, self.connectionInfo.charset)
                self.connectionLink.setdecoding(pyodbc.SQL_WCHAR, self.connectionInfo.charset)
        except Exception as e:
            message = str(e)
            return StiDataResult.getError(self, message)
        
        return StiDataResult.getSuccess(self)
    
    def process(self):
        if (not super().process()):
            return False

        parameterNames = {
            'driver': ['driver'],
            'userId': ['uid', 'user', 'username', 'userid', 'user id'],
            'password': ['pwd', 'password']
        }

        return self.parseParameters(parameterNames)
    
    
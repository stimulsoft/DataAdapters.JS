"""
Stimulsoft.Reports.JS
Version: 2024.1.1
Build date: 2023.12.08
License: https://www.stimulsoft.com/en/licensing/reports
"""

import pyodbc
from pyodbc import Connection

from .classes.StiDataResult import StiDataResult
from .StiDataAdapter import StiDataAdapter


class StiOdbcAdapter(StiDataAdapter):
    version: str = '2024.1.1'
    checkVersion: bool = True
    connectionLink: Connection

    def connect(self):
        try:
            self.connectionLink = pyodbc.connect(self.connectionString)
            if self.connectionInfo.charset:
                self.connectionLink.setdecoding(pyodbc.SQL_CHAR, self.connectionInfo.charset)
                self.connectionLink.setdecoding(pyodbc.SQL_WCHAR, self.connectionInfo.charset)
        except Exception as e:
            return StiDataResult.getError(self, str(e))
        
        return StiDataResult.getSuccess(self)
    
    def process(self):
        if not super().process():
            return False

        parameterNames = {
            'driver': ['driver'],
            'userId': ['uid', 'user', 'username', 'userid', 'user id'],
            'password': ['pwd', 'password']
        }

        return self.parseParameters(parameterNames)
    
    
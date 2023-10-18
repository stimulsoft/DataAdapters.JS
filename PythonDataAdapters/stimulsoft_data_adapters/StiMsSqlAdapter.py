"""
Stimulsoft.Reports.JS
Version: 2023.4.2
Build date: 2023.10.18
License: https://www.stimulsoft.com/en/licensing/reports
"""

from .StiDataAdapter import StiDataAdapter
from .classes.StiDataResult import StiDataResult
import pymssql
from datetime import datetime
from datetime import date
from datetime import time
from uuid import UUID

class StiMsSqlAdapter(StiDataAdapter):
    version: str = '2023.4.2'
    checkVersion: bool = True
    trustServerCertificate: str = None
    integratedSecurity: str = None

    def getOdbcConnectionString(self):
        connectionString: str = \
            f'Driver={self.connectionInfo.driver};' \
            f'Server={self.connectionInfo.host};' \
            f'Database={self.connectionInfo.database};' \
            f'Uid={self.connectionInfo.userId};' \
            f'Pwd={self.connectionInfo.password};'
        
        if (self.trustServerCertificate):
            connectionString += f'TrustServerCertificate={self.trustServerCertificate};'

        if (self.integratedSecurity):
            connectionString += f'Integrated Security={self.integratedSecurity};'
        
        return connectionString

    def connect(self):
        if (self.connectionInfo.driver):
            return self.connectOdbc()
        
        if (not self.connectionInfo.charset):
            self.connectionInfo.charset = 'utf8'

        try:
            self.connectionLink = pymssql.connect(
                server = self.connectionInfo.host,
                user = self.connectionInfo.userId,
                password = self.connectionInfo.password,
                database = self.connectionInfo.database,
                charset = self.connectionInfo.charset,
                host = self.connectionInfo.host,
                port = self.connectionInfo.port)
        except Exception as e:
            message = str(e)
            return StiDataResult.getError(self, message)
        
        return StiDataResult.getSuccess(self)
    
    def process(self):
        if (not super().process()):
            return False
        
        self.connectionInfo.port = 1433

        parameterNames = {
            'driver': ['driver'],
            'host': ['server', 'data source'],
            'database': ['database', 'initial catalog', 'dbname'],
            'userId': ['uid', 'user', 'user id'],
            'password': ['pwd', 'password'],
            'charset': ['charset']
        }

        return self.parseParameters(parameterNames)
    
    def parseUnknownParameter(self, parameter: str, name: str, value: str):
        super().parseUnknownParameter(parameter, name, value)
        
        if (name.lower() == 'trustservercertificate'):
            self.trustServerCertificate = value
        if (name.lower() == 'integrated security'):
            self.integratedSecurity = value
    
    def makeQuery(self, procedure: str, parameters: list):
        paramsString = super().makeQuery(procedure, parameters)
        return f'EXEC {procedure} {paramsString}'

    def parseType(self, meta: tuple):
        if (self.connectionInfo.driver):
            return super().parseType(meta)

        types = {
            'int': [pymssql.NUMBER],
            'number': [pymssql.DECIMAL],
            'datetime': [pymssql.DATETIME],
            'array': [pymssql.BINARY],
            'string': [pymssql.STRING]
        }

        for key, array in types.items():
            if (meta[1] in array):
                return key

        return 'string'
    
    def getValueType(self, value: object, index: int, types: list):
        if (types[index] == 'array' and (type(value) == datetime or type(value) == date or type(value) == time)):
            types[index] = 'datetime'

        if (types[index] == 'array' and type(value) == UUID):
            types[index] = 'string'
        
        return super().getValueType(value, index, types)
    
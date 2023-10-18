"""
Stimulsoft.Reports.JS
Version: 2023.4.2
Build date: 2023.10.18
License: https://www.stimulsoft.com/en/licensing/reports
"""

from .StiDataAdapter import StiDataAdapter
from .classes.StiDataResult import StiDataResult
from mysql.connector.connection import MySQLConnection
from mysql.connector import Error
from mysql.connector import FieldType
from mysql.connector import FieldFlag

class StiMySqlAdapter(StiDataAdapter):
    version: str = '2023.4.2'
    checkVersion: bool = True
    connectionLink: MySQLConnection
    
    def connect(self):
        if (self.connectionInfo.driver):
            return self.connectOdbc()
        
        if (not self.connectionInfo.charset):
            self.connectionInfo.charset = 'utf8'
        
        try:
            self.connectionLink = MySQLConnection(
                user = self.connectionInfo.userId,
                password = self.connectionInfo.password,
                host = self.connectionInfo.host,
                database = self.connectionInfo.database,
                port = self.connectionInfo.port,
                charset = self.connectionInfo.charset)
        except Error as error:
            return StiDataResult.getError(self, f'[{error.errno}] {error.msg}')
        
        return StiDataResult.getSuccess(self)
    
    def process(self):
        if (not super().process()):
            return False

        self.connectionInfo.port = 3306

        parameterNames = {
            'driver': ['driver'],
            'host': ['server', 'host', 'location'],
            'port': ['port'],
            'database': ['database', 'data source', 'dbname'],
            'userId': ['uid', 'user', 'username', 'userid', 'user id'],
            'password': ['pwd', 'password'],
            'charset': ['charset']
        }

        return self.parseParameters(parameterNames)

    def parseType(self, meta: tuple):
        if (self.connectionInfo.driver):
            return super().parseType(meta)

        types = {
            'tiny': [FieldType.TINY],
            'int': [FieldType.BIT, FieldType.SHORT, FieldType.LONG, FieldType.LONGLONG, FieldType.INT24, FieldType.YEAR],
            'number': [FieldType.DECIMAL, FieldType.FLOAT, FieldType.DOUBLE, FieldType.NEWDECIMAL],
            'time': [FieldType.TIME],
            'datetime': [FieldType.TIMESTAMP, FieldType.DATE, FieldType.DATETIME, FieldType.NEWDATE],
            'array': [FieldType.TINY_BLOB, FieldType.MEDIUM_BLOB, FieldType.LONG_BLOB, FieldType.GEOMETRY, FieldType.NULL],
            'blob': [FieldType.BLOB],
            'string': [FieldType.STRING, FieldType.VARCHAR, FieldType.VAR_STRING, FieldType.SET, FieldType.ENUM, FieldType.JSON]
        }

        for key, array in types.items():
            if (meta[1] in array):
                if (key == 'tiny'):
                    return 'int'  # boolean?
                if (key == 'blob'):
                    return 'array' if meta[7] & FieldFlag.BINARY else 'string'
                return key

        return 'string'
    
    def makeQuery(self, procedure: str, parameters: list):
        paramsString = super().makeQuery(procedure, parameters)
        return f'CALL {procedure} ({paramsString})'
    
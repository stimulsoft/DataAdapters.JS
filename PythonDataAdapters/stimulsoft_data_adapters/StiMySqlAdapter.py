"""
Stimulsoft.Reports.JS
Version: 2024.4.2
Build date: 2024.10.16
License: https://www.stimulsoft.com/en/licensing/reports
"""

from .classes.StiDataResult import StiDataResult
from .enums import StiDatabaseType
from .events.StiConnectionEventArgs import StiConnectionEventArgs
from .StiDataAdapter import StiDataAdapter


class StiMySqlAdapter(StiDataAdapter):

### Properties

    version = '2024.4.1'
    checkVersion = True
    type = StiDatabaseType.MYSQL
    driverName = 'mysql-connector-python'
    

### Methods

    def connect(self):
        if self.connectionInfo.driver:
            return self.connectOdbc()
        
        if not self.connectionInfo.charset:
            self.connectionInfo.charset = 'utf8'
        
        try:
            args = StiConnectionEventArgs(self.type, self.driverName, self.connectionInfo)
            self.handler.onDatabaseConnect(args)

            if args.link != None:
                self.connectionLink = args.link
            else:
                from mysql.connector.connection import MySQLConnection
                self.connectionLink = MySQLConnection(
                    user = self.connectionInfo.userId,
                    password = self.connectionInfo.password,
                    host = self.connectionInfo.host,
                    database = self.connectionInfo.database,
                    port = self.connectionInfo.port,
                    charset = self.connectionInfo.charset)
        except Exception as e:
            return StiDataResult.getError(str(e)).getDataAdapterResult(self)
        
        return StiDataResult.getSuccess().getDataAdapterResult(self)
    
    def process(self):
        if super().process():
            return True

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

        return self.processParameters(parameterNames)

    def getType(self, meta: tuple):
        if self.connectionInfo.driver:
            return super().getType(meta)
        
        from mysql.connector import FieldFlag, FieldType

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
            if meta[1] in array:
                if key == 'tiny':
                    return 'int'  # boolean?
                if key == 'blob':
                    return 'array' if meta[7] & FieldFlag.BINARY else 'string'
                return key

        return 'string'
    
    def makeQuery(self, procedure: str, parameters: list):
        paramsString = super().makeQuery(procedure, parameters)
        return f'CALL {procedure} ({paramsString})'
    
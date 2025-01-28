"""
Stimulsoft.Reports.JS
Version: 2025.1.4
Build date: 2025.01.24
License: https://www.stimulsoft.com/en/licensing/reports
"""

from datetime import date, datetime, time
from uuid import UUID

from .classes.StiDataResult import StiDataResult
from .enums import StiDatabaseType
from .events.StiConnectionEventArgs import StiConnectionEventArgs
from .StiDataAdapter import StiDataAdapter


class StiMsSqlAdapter(StiDataAdapter):

### Properties

    version = '2025.1.3'
    checkVersion = True
    trustServerCertificate: str = None
    integratedSecurity: str = None
    type = StiDatabaseType.MSSQL
    driverName = 'pymssql'


### Methods

    def getOdbcConnectionString(self):
        connectionString: str = \
            f'Driver={self.connectionInfo.driver};' \
            f'Server={self.connectionInfo.host};' \
            f'Database={self.connectionInfo.database};' \
            f'Uid={self.connectionInfo.userId};' \
            f'Pwd={self.connectionInfo.password};'
        
        if self.trustServerCertificate:
            connectionString += f'TrustServerCertificate={self.trustServerCertificate};'

        if self.integratedSecurity:
            connectionString += f'Integrated Security={self.integratedSecurity};'
        
        return connectionString

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
                import pymssql
                self.connectionLink = pymssql.connect(
                    server = self.connectionInfo.host,
                    user = self.connectionInfo.userId,
                    password = self.connectionInfo.password,
                    database = self.connectionInfo.database,
                    charset = self.connectionInfo.charset,
                    host = self.connectionInfo.host,
                    port = self.connectionInfo.port)
        except Exception as e:
            return StiDataResult.getError(str(e)).getDataAdapterResult(self)
        
        return StiDataResult.getSuccess().getDataAdapterResult(self)
    
    def process(self):
        if super().process():
            return True
        
        self.connectionInfo.port = 1433

        parameterNames = {
            'driver': ['driver'],
            'host': ['server', 'data source'],
            'database': ['database', 'initial catalog', 'dbname'],
            'userId': ['uid', 'user', 'user id'],
            'password': ['pwd', 'password'],
            'charset': ['charset']
        }

        return self.processParameters(parameterNames)
    
    def processUnknownParameter(self, parameter: str, name: str, value: str):
        super().processUnknownParameter(parameter, name, value)
        
        if name.lower() == 'trustservercertificate':
            self.trustServerCertificate = value
        if name.lower() == 'integrated security':
            self.integratedSecurity = value
    
    def makeQuery(self, procedure: str, parameters: list):
        paramsString = super().makeQuery(procedure, parameters)
        return f'EXEC {procedure} {paramsString}'

    def getType(self, meta: tuple):
        import pymssql

        if self.connectionInfo.driver:
            return super().getType(meta)

        types = {
            'int': [pymssql.NUMBER],
            'number': [pymssql.DECIMAL],
            'datetime': [pymssql.DATETIME],
            'array': [pymssql.BINARY],
            'string': [pymssql.STRING]
        }

        for key, array in types.items():
            if meta[1] in array:
                return key

        return 'string'
    
    def getValueType(self, value: object, index: int, types: list):
        if types[index] == 'array' and (type(value) == datetime or type(value) == date or type(value) == time):
            types[index] = 'datetime'

        if types[index] == 'array' and type(value) == UUID:
            types[index] = 'string'
        
        return super().getValueType(value, index, types)
    
"""
Stimulsoft.Reports.JS
Version: 2024.4.3
Build date: 2024.10.23
License: https://www.stimulsoft.com/en/licensing/reports
"""

from __future__ import annotations

import codecs
import typing
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from uuid import UUID

from pyodbc import Connection

from .classes.StiConnectionInfo import StiConnectionInfo
from .classes.StiDataResult import StiDataResult
from .classes.StiParameter import StiParameter
from .enums.StiDatabaseType import StiDatabaseType

if typing.TYPE_CHECKING:
    from .classes.StiBaseHandler import StiBaseHandler


class StiDataAdapter:

### Properties

    version = ''
    checkVersion = False

    handler: StiBaseHandler = None
    type = StiDatabaseType.NONE
    driverName: str = None
    connectionString: str = None
    connectionInfo: StiConnectionInfo = None
    connectionLink: Connection = None


### Methods

    def getOdbcConnectionString(self):
        connectionString: str = \
            f'Driver={self.connectionInfo.driver};' \
            f'Server={self.connectionInfo.host};' \
            f'Database={self.connectionInfo.database};' \
            f'Uid={self.connectionInfo.userId};' \
            f'Pwd={self.connectionInfo.password};'
        
        return connectionString

    def connect(self):
        return StiDataResult.getSuccess().getDataAdapterResult(self)
    
    def connectOdbc(self):
        from .StiOdbcAdapter import StiOdbcAdapter
        adapter = StiOdbcAdapter()
        adapter.connectionString = self.getOdbcConnectionString()
        adapter.connectionInfo = self.connectionInfo

        result = adapter.connect()
        self.connectionLink = adapter.connectionLink
        return result

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
        self.connectionInfo = StiConnectionInfo()
        return False
    
    def processParameters(self, parameterNames: dict[str, list[str]]):
        parameters = self.connectionString.split(';')

        for parameter in parameters:
            name = ''
            value = parameter
            if parameter.find('=') >= 0:
                pos = parameter.find('=')
                name = parameter[0:pos].strip().lower()
                value = parameter[pos + 1:].strip()

            unknown = True
            if len(parameterNames) > 0:
                for key, names in parameterNames.items():
                    if name in names:
                        setattr(self.connectionInfo, key, value)
                        unknown = False
                        break

            if unknown:
                self.processUnknownParameter(parameter, name, value)

        return True
    
    def processUnknownParameter(self, parameter: str, name: str, value: str):
        pass

    def getType(self, meta: tuple):
        types = {
            'boolean': [bool],
            'int': [int],
            'number': [float, complex, Decimal],
            'time': [timedelta],
            'datetime': [time, date, datetime],
            'array': [bytes, bytearray],
            'string': [str]
        }

        for key, array in types.items():
            if meta[1] in array:
                return key

        return 'string'
    
    def getValueType(self, value: object, index: int, types: list):
        return types[index]

    def getValue(self, value: object, valueType: str):
        if value is None:
            return None

        if valueType == 'array':
            valueBytes = value.encode() if type(value) == str else value
            return codecs.encode(valueBytes, 'base64').decode()
        
        if valueType == 'datetime':
            valueDateTime: datetime = value
            return valueDateTime.strftime('%Y-%m-%dT%H:%M:%S.000')
        
        if valueType == 'time':
            valueDelta: timedelta = value
            hours = int(valueDelta.seconds / 3600) + valueDelta.days * 24
            minutes = int(valueDelta.seconds / 60) % 60
            seconds = int(valueDelta.seconds) % 60
            return '{:02d}:'.format(hours) + '{:02d}:'.format(minutes) + '{:02d}.000'.format(seconds)
        
        if type(value) == Decimal:
            return float(value)
        
        if type(value) == UUID:
            return str(value)
        
        return value
    
    def makeQuery(self, procedure: str, parameters: list):
        paramsString: str = ''
        for name in parameters:
            if len(paramsString) > 0:
                paramsString += ', '
            paramsString += '@' + name

        return paramsString
    
    def executeQuery(self, queryString: str, maxDataRows: int):
        result = self.connect()
        if result.success:
            result.types = []
            result.columns = []
            result.rows = []

            if maxDataRows != 0:
                result = self.executeNative(queryString, maxDataRows, result)
            
            self.disconnect()

        return result
    
    def executeNative(self, queryString: str, maxDataRows: int, result: StiDataResult):
        cursor = self.connectionLink.cursor()

        try:
            cursor.execute(queryString)
        except Exception as e:
            message = str(e)
            cursor.close()
            return StiDataResult.getError(message).getDataAdapterResult(self)
        
        for meta in cursor.description:
            result.columns.append(meta[0])
            columnType = self.getType(meta)
            result.types.append(columnType)

        try:
            for rowItem in cursor:
                row = []
                for rowValue in rowItem:
                    valueType = self.getValueType(rowValue, len(row), result.types)
                    value = self.getValue(rowValue, valueType)
                    row.append(value)
                result.rows.append(row)
            
                if len(result.rows) == maxDataRows:
                    cursor.fetchall()

        except Exception as e:
            message = str(e)
            return StiDataResult.getError(message).getDataAdapterResult(self)
        finally:
            cursor.close()

        result.count = len(result.rows)
        return result
    

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
        
        return None
    
    @staticmethod
    def applyQueryParameters(query: str, parameters: dict[str, StiParameter], escape: bool) -> str:
        result: str = ''

        while query.find('@') >= 0:
            result += query[0:query.find('@')]
            query = query[query.find('@') + 1:]

            parameterName = ''
            while len(query) > 0:
                char = query[0]
                if not char.isalnum() and char != '_':
                    break

                parameterName += char
                query = query[1:]

            replaced: bool = False
            for key, item in parameters.items():
                if key.lower() == parameterName.lower():
                    stringValue = str(item.value)
                    if item.typeGroup == 'number':
                        result += stringValue
                    elif item.typeGroup == 'datetime':
                        result += "'" + stringValue + "'"
                    elif escape:
                        result += "'" + stringValue.translate(str.maketrans({'\\':  r'\\', "'": r"\'", '"': r'\"'})) + "'"
                    else:
                        result += "'" + stringValue + "'"
                    
                    replaced = True

            if (replaced == False):
                result += '@' + parameterName

        return result + query
    

### Constructor
    
    def __init__(self, connectionString: str):
        self.connectionString = connectionString.strip()
        self.process()
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


class StiOracleAdapter(StiDataAdapter):

### Properties

    version = '2024.4.1'
    checkVersion = True
    type = StiDatabaseType.ORACLE
    driverName = 'oracledb'


### Methods

    def getOdbcConnectionString(self):
        connectionString: str = \
            f'Driver={self.connectionInfo.driver};' \
            f'Dbq={self.connectionInfo.database};' \
            f'Uid={self.connectionInfo.userId};' \
            f'Pwd={self.connectionInfo.password};'
        
        return connectionString

    def connect(self):
        if self.connectionInfo.driver:
            return self.connectOdbc()
        
        try:
            args = StiConnectionEventArgs(self.type, self.driverName, self.connectionInfo)
            self.handler.onDatabaseConnect(args)
            
            if args.link != None:
                self.connectionLink = args.link
            else:
                import oracledb
                oracledb.init_oracle_client()
                self.connectionLink = oracledb.connect(
                    user = self.connectionInfo.userId,
                    password = self.connectionInfo.password,
                    dsn = self.connectionInfo.database,
                    encoding = self.connectionInfo.charset,
                    mode = self.connectionInfo.privilege)
        except Exception as e:
            return StiDataResult.getError(str(e)).getDataAdapterResult(self)
        
        return StiDataResult.getSuccess().getDataAdapterResult(self)
    
    def process(self):
        if super().process():
            return True
        
        import oracledb
        
        self.connectionInfo.port = 3306
        self.connectionInfo.privilege = oracledb.AUTH_MODE_DEFAULT

        parameterNames = {
            'driver': ['driver'],
            'database': ['database', 'data source', 'dbname'],
            'userId': ['uid', 'user', 'user id'],
            'password': ['pwd', 'password'],
            'charset': ['charset']
        }

        return self.processParameters(parameterNames)
    
    def processUnknownParameter(self, parameter: str, name: str, value: str):
        import oracledb
        
        super().processUnknownParameter(parameter, name, value)

        if name.lower() == 'dba privilege' or name.lower() == 'privilege':
            value = value.lower()
            if value == 'sysoper' or value == 'oci_sysoper':
                self.connectionInfo.privilege = oracledb.AUTH_MODE_SYSOPER
            if value == 'sysdba' or value == 'oci_sysdba':
                self.connectionInfo.privilege = oracledb.AUTH_MODE_SYSDBA

    def getType(self, meta: tuple):
        if self.connectionInfo.driver:
            return super().getType(meta)
        
        import oracledb
        info: oracledb.FetchInfo = meta
        
        types = {
            'int': [oracledb.DB_TYPE_NUMBER],
            'number': [oracledb.DB_TYPE_BINARY_DOUBLE, oracledb.DB_TYPE_BINARY_FLOAT],
            'time': [oracledb.DB_TYPE_INTERVAL_DS],
            'datetime': [oracledb.DB_TYPE_DATE, oracledb.DB_TYPE_TIMESTAMP, oracledb.DB_TYPE_TIMESTAMP_LTZ, oracledb.DB_TYPE_TIMESTAMP_TZ],
            'blob': [oracledb.DB_TYPE_BFILE, oracledb.DB_TYPE_BLOB, oracledb.DB_TYPE_CLOB, oracledb.DB_TYPE_CURSOR, oracledb.DB_TYPE_NCLOB],
            'array': [oracledb.DB_TYPE_LONG_RAW, oracledb.DB_TYPE_OBJECT, oracledb.DB_TYPE_RAW],
            'string': [oracledb.DB_TYPE_CHAR, oracledb.DB_TYPE_JSON, oracledb.DB_TYPE_LONG, oracledb.DB_TYPE_NCHAR, oracledb.DB_TYPE_NVARCHAR,
                       oracledb.DB_TYPE_ROWID, oracledb.DB_TYPE_ROWID, oracledb.DB_TYPE_UROWID, oracledb.DB_TYPE_VARCHAR]
        }

        for key, array in types.items():
            if info.type in array:
                if key == 'int':
                    return 'number' if info.scale > 0 else 'int'
                if key == 'blob':
                    return 'array'
                return key

        return 'string'
    
    def getValue(self, value: object, valueType: str):
        import oracledb
        
        if value is None:
            return None
        
        if valueType == 'array':
            if type(value) == oracledb.LOB:
                value = value.read()

        return super().getValue(value, valueType)

    def makeQuery(self, procedure: str, parameters: list):
        paramsString = super().makeQuery(procedure, parameters)
        return f"SQLEXEC 'CALL {procedure} {paramsString}'"
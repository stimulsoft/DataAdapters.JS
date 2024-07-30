"""
Stimulsoft.Reports.JS
Version: 2024.3.3
Build date: 2024.07.25
License: https://www.stimulsoft.com/en/licensing/reports
"""

from .classes.StiDataResult import StiDataResult
from .StiDataAdapter import StiDataAdapter


class StiFirebirdAdapter(StiDataAdapter):

### Properties

    version = '2024.3.2'
    checkVersion = True


### Methods

    def getOdbcConnectionString(self):
        connectionString: str = \
            f'Driver={self.connectionInfo.driver};' \
            f'Dbname={self.connectionInfo.host}/{self.connectionInfo.port}:{self.connectionInfo.database};' \
            f'Uid={self.connectionInfo.userId};' \
            f'Pwd={self.connectionInfo.password};'
        
        return connectionString

    def connect(self) -> StiDataResult:
        if self.connectionInfo.driver:
            return self.connectOdbc()
        
        if not self.connectionInfo.charset:
            self.connectionInfo.charset = 'utf8'
        
        try:
            from firebird.driver import connect
            dsn = f'{self.connectionInfo.host}/{self.connectionInfo.port}:{self.connectionInfo.database}'
            self.connectionLink = connect(
                user = self.connectionInfo.userId,
                password = self.connectionInfo.password,
                database = dsn,
                charset = self.connectionInfo.charset)
        except Exception as e:
            return StiDataResult.getError(str(e)).getDataAdapterResult(self)
        
        return StiDataResult.getSuccess().getDataAdapterResult(self)
    
    def process(self):
        if super().process():
            return True

        self.connectionInfo.port = 3050

        parameterNames = {
            'driver': ['driver'],
            'host': ['server', 'host', 'location', 'datasource', 'data source'],
            'port': ['port'],
            'database': ['database', 'dbname'],
            'userId': ['uid', 'user', 'username', 'userid', 'user id'],
            'password': ['pwd', 'password'],
            'charset': ['charset']
        }

        return self.processParameters(parameterNames)
    
    def makeQuery(self, procedure: str, parameters: list):
        paramsString = super().makeQuery(procedure, parameters)
        return f'EXECUTE PROCEDURE {procedure} {paramsString}'
    
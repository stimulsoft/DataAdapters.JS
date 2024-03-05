"""
Stimulsoft.Reports.JS
Version: 2024.2.1
Build date: 2024.03.04
License: https://www.stimulsoft.com/en/licensing/reports
"""

from .classes.StiDataResult import StiDataResult
from .StiDataAdapter import StiDataAdapter


class StiFirebirdAdapter(StiDataAdapter):
    version: str = '2024.2.1'
    checkVersion: bool = True

    def getOdbcConnectionString(self):
        connectionString: str = \
            f'Driver={self.connectionInfo.driver};' \
            f'Dbname={self.connectionInfo.host}/{self.connectionInfo.port}:{self.connectionInfo.database};' \
            f'Uid={self.connectionInfo.userId};' \
            f'Pwd={self.connectionInfo.password};'
        
        return connectionString

    def connect(self):
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
            return StiDataResult.getError(self, str(e))
        
        return StiDataResult.getSuccess(self)
    
    def process(self):
        if not super().process():
            return False

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

        return self.parseParameters(parameterNames)
    
    def makeQuery(self, procedure: str, parameters: list):
        paramsString = super().makeQuery(procedure, parameters)
        return f'EXECUTE PROCEDURE {procedure} {paramsString}'
    
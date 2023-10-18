"""
Stimulsoft.Reports.JS
Version: 2023.4.2
Build date: 2023.10.18
License: https://www.stimulsoft.com/en/licensing/reports
"""

from .StiDataAdapter import StiDataAdapter
from .classes.StiDataResult import StiDataResult
from firebird.driver import connect

class StiFirebirdAdapter(StiDataAdapter):
    version: str = '2023.4.2'
    checkVersion: bool = True

    def getOdbcConnectionString(self):
        connectionString: str = \
            f'Driver={self.connectionInfo.driver};' \
            f'Dbname={self.connectionInfo.host}/{self.connectionInfo.port}:{self.connectionInfo.database};' \
            f'Uid={self.connectionInfo.userId};' \
            f'Pwd={self.connectionInfo.password};'
        
        return connectionString

    def connect(self):
        if (self.connectionInfo.driver):
            return self.connectOdbc()
        
        if (not self.connectionInfo.charset):
            self.connectionInfo.charset = 'utf8'
        
        try:
            dsn = f'{self.connectionInfo.host}/{self.connectionInfo.port}:{self.connectionInfo.database}'
            self.connectionLink = connect(
                user = self.connectionInfo.userId,
                password = self.connectionInfo.password,
                database = dsn,
                charset = self.connectionInfo.charset)
        except Exception as e:
            message = str(e)
            return StiDataResult.getError(self, message)
        
        return StiDataResult.getSuccess(self)
    
    def process(self):
        if (not super().process()):
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
    
"""
Stimulsoft.Reports.JS
Version: 2025.2.4
Build date: 2025.05.19
License: https://www.stimulsoft.com/en/licensing/reports
"""

from urllib import response
import requests

from .classes.StiDataResult import StiDataResult
from .classes.StiPath import StiPath
from .enums.StiDataType import StiDataType
from .StiDataAdapter import StiDataAdapter


class StiFileAdapter(StiDataAdapter):
    
### Properties

    dataType = StiDataType.TEXT
    """The data type loaded by the data adapter."""

    connectionLink: StiPath = None
    """Link to the created database connection driver."""

### Methods

    def connect(self) -> StiDataResult:
        path = StiPath(self.connectionString)
        if path.filePath == None:
            return StiDataResult.getError(f"Data file '{self.connectionString}' not found.").getDataAdapterResult(self)

        self.connectionLink = path

        return StiDataResult.getSuccess().getDataAdapterResult(self)
    
    def getDataResult(self, filePath: str, maxDataRows: int = -1) -> StiDataResult:
        self.connectionString = filePath
        self.process()

        result = self.connect()
        if result.success:
            try:
                if self.connectionLink.fileUrl != None:
                    response = requests.get(self.connectionLink.fileUrl)
                    if response.status_code == 200:
                        result.data = response.content.decode()
                else:
                    with open(self.connectionLink.filePath, mode='r', encoding='utf-8') as file:
                        result.data = file.read()

                result.dataType = self.dataType.value
                
            except Exception as e:
                message = str(e)
                result = StiDataResult.getError(message).getDataAdapterResult(self)

        return result
    
"""
Stimulsoft.Reports.JS
Version: 2024.1.4
Build date: 2024.02.14
License: https://www.stimulsoft.com/en/licensing/reports
"""

import codecs
import json

from .StiBaseResult import StiBaseResult


class StiBaseRequest:
    """Contains all set request parameters passed to the event handler."""

    event: str = None
    command: str = None
    encryptData: bool = False
    connectionString: str = None
    queryString: str = None
    parameters: dict[str, object] = None
    database: str = None
    dataSource: str = None
    connection: str = None
    timeout: int = 0
    escapeQueryParameters: bool = False
    error: str = None


### Private

    def __populateVars(self, obj: object, prefix: bool = False):
        fields = dir(self)
        for prop in obj:
            field = prop[4:] if prefix and prop[0:4] == 'sti_' else prop
            if field in fields:
                self._setField(field, obj[prop])


### Protected

    def _setField(self, name, value):
        setattr(self, name, value)


### Public

    def process(self, query: dict, body: str) -> bool:
        if len(query) > 0:
            self.__populateVars(query, True)

        if len(body) > 0:
            if body[0] != '{':
                try:
                    body = codecs.decode(body, 'rot_13')
                    body = codecs.decode(body.encode(), 'base64').decode()
                except Exception as e:
                    self.error = 'Base64: ' + str(e)
                    return False
                
                self.encryptData = True

            try:
                obj = json.loads(body)
            except Exception as e:
                self.error = 'JSON: ' + str(e)
                return False

            self.__populateVars(obj)

        return True

    def getResult(self):
        """
        The result of executing an event handler request. 
        The result contains a collection of data, message about the result of the command execution, and other technical information.
        """

        if self.error != None:
            return StiBaseResult.getError(self.error)

        StiBaseResult.getSuccess()
    
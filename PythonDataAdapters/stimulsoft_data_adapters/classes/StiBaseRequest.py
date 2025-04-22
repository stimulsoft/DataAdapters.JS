"""
Stimulsoft.Reports.JS
Version: 2025.2.3
Build date: 2025.04.18
License: https://www.stimulsoft.com/en/licensing/reports
"""

import codecs
import json
from enum import Enum, Flag

from ..enums import StiBaseEventType, StiDatabaseType, StiDataCommand
from .StiBaseResult import StiBaseResult


class StiBaseRequest:
    """Contains all set request parameters passed to the event handler."""


### Properties

    event = StiBaseEventType.NONE
    command = StiDataCommand.NONE
    encryptData = False
    connectionString: str = None
    queryString: str = None
    parameters: dict[str, object] = None
    database = StiDatabaseType.NONE
    dataSource: str = None
    connection: str = None
    timeout = 0
    maxDataRows: int = None
    pathData: str = None
    pathSchema: str = None
    escapeQueryParameters = False
    error: str = None


### Helpers

    def __getProperties(self) -> list:
        return [name for name in dir(self) if not name.startswith('_') and not callable(getattr(self, name))]

    def __setObject(self, object: dict, prefix = False):
        properties = self.__getProperties()
        for property in object:
            name = property[4:] if prefix and property[0:4] == 'sti_' else property
            if name in properties:
                self._setProperty(name, object.get(property))
    
    def _setProperty(self, name, value):
        selfvalue = getattr(self, name)
        if isinstance(selfvalue, Enum) or isinstance(value, Flag): setattr(self, name, selfvalue.__class__(value))
        else: setattr(self, name, value)


### Process

    def process(self, query: dict, body: str) -> bool:
        if len(query or '') > 0:
            self.__setObject(query, True)

        if len(body or '') > 0:
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

            self.__setObject(obj)

        return True

    def getResult(self):
        """
        The result of executing an event handler request. 
        The result contains a collection of data, message about the result of the command execution, and other technical information.
        """

        if self.error != None:
            return StiBaseResult.getError(self.error)

        StiBaseResult.getSuccess()

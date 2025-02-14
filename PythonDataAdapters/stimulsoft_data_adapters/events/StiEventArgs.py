"""
Stimulsoft.Reports.JS
Version: 2025.1.5
Build date: 2025.02.11
License: https://www.stimulsoft.com/en/licensing/reports
"""

from enum import Enum, Flag


class StiEventArgs:

### Properties

    event: str = None
    """Name of the current event."""
    
    sender: object = None
    """The component that sent the request."""


### Helpers

    def __getProperties(self) -> list:
        return [name for name in dir(self) if not name.startswith('_')  and name != 'sender' and not callable(getattr(self, name))]

    def __setObject(self, object: object):
        properties = self.__getProperties()
        for name in properties:
            if hasattr(object, name):
                value = getattr(object, name)
                self.__setProperty(name, value)

    def __setProperty(self, name, value):
        selfvalue = getattr(self, name)
        if isinstance(selfvalue, Enum) or isinstance(value, Flag):
            if value != None: setattr(self, name, selfvalue.__class__(value))
        else: setattr(self, name, value)


### Constructor

    def __init__(self, object = None):
        if (object != None):
            self.__setObject(object)
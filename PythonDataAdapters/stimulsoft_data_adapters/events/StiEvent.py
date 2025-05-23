"""
Stimulsoft.Reports.JS
Version: 2025.2.4
Build date: 2025.05.19
License: https://www.stimulsoft.com/en/licensing/reports
"""

from __future__ import annotations

import typing

from ..classes.StiBaseResult import StiBaseResult
from .StiEventArgs import StiEventArgs

if typing.TYPE_CHECKING:
    from ..classes.StiBaseHandler import StiBaseHandler


class StiEvent:

### Fields

    __name: str = None
    __callbacks: list = None
    __handler: StiBaseHandler = None


### Properties
    
    @property
    def name(self):
        return self.__name
    
    @property
    def callbacks(self):
        return self.__callbacks
    
    @property
    def handler(self):
        return self.__handler
    

### Helpers

    def getResult(self, args: StiEventArgs, resultClass = None) -> StiBaseResult:
        if resultClass == None:
            resultClass = StiBaseResult

        if len(self) > 0:
            result = self(args)

            if result == None or result == True:
                return resultClass.getSuccess()

            if result == False:
                return resultClass.getError(f"An error occurred while processing the '{self.name}' event.")

            if isinstance(result, StiBaseResult):
                return result

            return resultClass.getSuccess(str(result))

        return None

    def _setArgs(self, *args, **keywargs) -> StiEventArgs:
        eventArgs = args[0] if len(args) > 0 else keywargs.get('args')
        if isinstance(eventArgs, StiEventArgs):
            eventArgs.event = self.name[2:]
            eventArgs.sender = self.handler
            return eventArgs
        
        return None
    
    def append(self, callback) -> StiEvent:
        self.callbacks.append(callback)
        return self

    def remove(self, callback) -> StiEvent:
        self.callbacks.remove(callback)
        return self
    
    def hasServerCallbacks(self) -> bool:
        for callback in self.callbacks:
            if (callable(callback) or callback == True):
                return True
        
        return False
    
    def hasClientCallbacks(self) -> bool:
        for callback in self.callbacks:
            if (isinstance(callback, str)):
                return True
        
        return False

### Override

    def __len__(self) -> int:
        return len(self.callbacks or '')

    def __iadd__(self, callback) -> StiEvent:
        return self.append(callback)
    
    def __isub__(self, callback) -> StiEvent:
        return self.remove(callback)

    def __call__(self, *args, **keywargs) -> object:
        for callback in self.callbacks:
            if (callable(callback)):
                self._setArgs(*args, **keywargs)
                result = callback(*args, **keywargs)
                if result != None:
                    return result
        return None
    
    def __contains__(self, callback):
        return callback in self.callbacks
	

### Constructor

    def __init__(self, handler: StiBaseHandler, name: str):
        self.__callbacks = []
        self.__handler = handler
        self.__name = name
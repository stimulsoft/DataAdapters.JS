"""
Stimulsoft.Reports.JS
Version: 2024.4.1
Build date: 2024.10.08
License: https://www.stimulsoft.com/en/licensing/reports
"""

from __future__ import annotations

import typing

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
            if (callable(callback)):
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
	

### Constructor

    def __init__(self, handler: StiBaseHandler, name: str):
        self.__callbacks = []
        self.__handler = handler
        self.__name = name
"""
Stimulsoft.Reports.JS
Version: 2024.2.4
Build date: 2024.04.18
License: https://www.stimulsoft.com/en/licensing/reports
"""

from __future__ import annotations

import typing

from .StiEventArgs import StiEventArgs

if typing.TYPE_CHECKING:
    from ..classes.StiBaseHandler import StiBaseHandler


class StiEvent:

### Private

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
    

### Protected

    def _applyFields(self, *args, **keywargs) -> StiEventArgs:
        eventArgs = args[0] if len(args) > 0 else keywargs.get('args')
        if isinstance(eventArgs, StiEventArgs):
            eventArgs.event = self.name[2:]
            eventArgs.sender = self.handler
            return eventArgs
        
        return None

### Override

    def __len__(self) -> int:
        return len(self.callbacks or '')

    def __iadd__(self, callback) -> StiEvent:
        self.callbacks.append(callback)
        return self
    
    def __isub__(self, callback) -> StiEvent:
        self.callbacks.remove(callback)
        return self

    def __call__(self, *args, **keywargs) -> object:
        for callback in self.callbacks:
            if (callable(callback)):
                self._applyFields(*args, **keywargs)
                return callback(*args, **keywargs)
	

### Constructor

    def __init__(self, handler: StiBaseHandler, name: str):
        self.__callbacks = []
        self.__handler = handler
        self.__name = name
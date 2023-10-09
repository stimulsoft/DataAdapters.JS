"""
Stimulsoft.Reports.JS
Version: 2023.4.1
Build date: 2023.10.06
License: https://www.stimulsoft.com/en/licensing/reports
"""

class StiEvent:

    __handlers: list = None
    __name: str = None

    @property
    def count(self):
        return len(self.__handlers or '')
    
    @property
    def name(self):
        return self.__name
    
    @property
    def jsHandlers(self):
        return [handler for handler in self.__handlers if type(handler) == str or handler is True]
    
    def __iadd__(self, handler):
        self.__handlers.append(handler)
        return self
    
    def __isub__(self, handler):
        self.__handlers.remove(handler)
        return self

    def __call__(self, *args, **keywargs):
        for handler in self.__handlers:
            if (callable(handler)):
                handler(*args, **keywargs)

    def __init__(self, name: str):
        self.__handlers = []
        self.__name = name
	
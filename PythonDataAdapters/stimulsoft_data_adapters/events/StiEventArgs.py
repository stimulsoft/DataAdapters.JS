"""
Stimulsoft.Reports.JS
Version: 2023.4.2
Build date: 2023.10.18
License: https://www.stimulsoft.com/en/licensing/reports
"""

class StiEventArgs:
    
    sender: str = None
    """The component that sent the request."""


### Private

    def __populateVars(self, obj: object):
        attributes = [attr for attr in dir(self) if not attr.startswith('_') and attr != 'sender']
        for attr in attributes:
            if hasattr(obj, attr):
                setattr(self, attr, getattr(obj, attr))


### Constructor

    def __init__(self, sender: object, obj: object = None):
        self.sender = sender
        if (obj != None):
            self.__populateVars(obj)
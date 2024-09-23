"""
Stimulsoft.Reports.JS
Version: 2024.3.6
Build date: 2024.09.19
License: https://www.stimulsoft.com/en/licensing/reports
"""

from __future__ import annotations


class StiBaseResult:
    """
    The result of executing an event handler request. 
    The result contains a collection of data, message about the result of the command execution, and other technical information.
    """

### Properties
    
    handlerVersion: str = None
    checkVersion = True
    success = True
    notice: str = None


### Abstract

    types: list


### JSON

    @staticmethod
    def getProperties(object: object):
        return { name: getattr(object, name) for name in dir(object) if not name.startswith('_') and not callable(getattr(object, name)) }


### Result

    @staticmethod
    def getSuccess(notice: str = None) -> StiBaseResult:
        """Creates a successful result."""

        result = StiBaseResult()
        result.success = True
        result.notice = notice
        return result
    
    @staticmethod
    def getError(notice: str) -> StiBaseResult:
        """Creates an error result."""

        result = StiBaseResult()
        result.success = False
        result.notice = notice
        return result
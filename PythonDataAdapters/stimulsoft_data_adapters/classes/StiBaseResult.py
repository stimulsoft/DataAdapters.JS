"""
Stimulsoft.Reports.JS
Version: 2023.4.3
Build date: 2023.11.02
License: https://www.stimulsoft.com/en/licensing/reports
"""

from __future__ import annotations


class StiBaseResult:
    """
    The result of executing an event handler request. 
    The result contains a collection of data, message about the result of the command execution, and other technical information.
    """
    
    handlerVersion: str = None
    checkVersion: bool = True
    success: bool = True
    notice: str = None
    
### Abstract

    types: list


### Public

    def getSuccess(notice: str = None) -> StiBaseResult:
        """Creates a successful result."""

        result = StiBaseResult()
        result.success = True
        result.notice = notice
        return result
    
    def getError(notice: str) -> StiBaseResult:
        """Creates an error result."""

        result = StiBaseResult()
        result.success = False
        result.notice = notice
        return result
"""
Stimulsoft.Reports.JS
Version: 2024.4.3
Build date: 2024.10.23
License: https://www.stimulsoft.com/en/licensing/reports
"""

from __future__ import annotations

import typing

from .StiBaseResult import StiBaseResult

if typing.TYPE_CHECKING:
    from ..StiDataAdapter import StiDataAdapter


class StiDataResult(StiBaseResult):
    """
    The result of executing an event handler request. 
    The result contains a collection of data, message about the result of the command execution, and other technical information.
    """

### Properties

    adapterVersion: str = None
    types: list = None
    columns: list = None
    rows: list = None
    count = 0


### Result

    def getDataAdapterResult(self, adapter: StiDataAdapter) -> StiDataResult:
        self.adapterVersion = adapter.version
        self.checkVersion = adapter.checkVersion
        return self

    @staticmethod
    def getSuccess(notice: str = None) -> StiDataResult:
        """Creates a successful result."""
        
        result: StiDataResult = StiBaseResult.getSuccess(notice)
        result.__class__ = StiDataResult
        result.types = []
        result.columns = []
        result.rows = []

        return result
    
    @staticmethod
    def getError(notice: str) -> StiDataResult:
        """Creates an error result."""

        result: StiDataResult = StiBaseResult.getError(notice)
        result.__class__ = StiDataResult
        return result
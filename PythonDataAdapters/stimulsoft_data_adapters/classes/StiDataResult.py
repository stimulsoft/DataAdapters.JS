"""
Stimulsoft.Reports.JS
Version: 2024.1.3
Build date: 2024.01.18
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

    adapterVersion: str = None
    types: list = None
    columns: list = None
    rows: list = None
    count: int = 0


### Public

    def getSuccess(adapter: StiDataAdapter, notice: str = None) -> StiDataResult:
        """Creates a successful result."""
        
        result: StiDataResult = StiBaseResult.getSuccess(notice)
        result.__class__ = StiDataResult
        result.adapterVersion = adapter.version
        result.checkVersion = adapter.checkVersion
        result.types = []
        result.columns = []
        result.rows = []

        return result
    
    def getError(adapter: StiDataAdapter, notice: str) -> StiBaseResult:
        """Creates an error result."""

        result: StiDataResult = StiBaseResult.getError(notice)
        result.__class__ = StiDataResult
        result.adapterVersion = adapter.version
        result.checkVersion = adapter.checkVersion
        return result
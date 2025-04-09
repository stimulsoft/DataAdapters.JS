"""
Stimulsoft.Reports.JS
Version: 2025.2.2
Build date: 2025.04.08
License: https://www.stimulsoft.com/en/licensing/reports
"""

from __future__ import annotations

import typing

from .StiBaseResult import StiBaseResult

if typing.TYPE_CHECKING:
    from ..StiDataAdapter import StiDataAdapter
    from ..StiSqlAdapter import StiSqlAdapter


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
    data: str = None
    dataType: str = None
    count = 0

    @property
    def type(self) -> str:
        if self.success:
            if hasattr(self, 'columns') and isinstance(self.columns, list):
                return 'SQL'

            if self.dataType != None:
                return 'File'

        return super().type


### Result

    def getDataAdapterResult(self, adapter: StiDataAdapter) -> StiDataResult:
        self.adapterVersion = adapter.version
        self.checkVersion = adapter.checkVersion

        from ..StiSqlAdapter import StiSqlAdapter
        if isinstance(adapter, StiSqlAdapter):
            self.types = []
            self.columns = []
            self.rows = []

        return self

    @staticmethod
    def getSuccess(notice: str = None) -> StiDataResult:
        """Creates a successful result."""
        
        result: StiDataResult = StiBaseResult.getSuccess(notice)
        result.__class__ = StiDataResult
        
        return result
    
    @staticmethod
    def getError(notice: str) -> StiDataResult:
        """Creates an error result."""

        result: StiDataResult = StiBaseResult.getError(notice)
        result.__class__ = StiDataResult
        
        return result
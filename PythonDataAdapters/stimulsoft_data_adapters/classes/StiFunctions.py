"""
Stimulsoft.Reports.JS
Version: 2025.2.3
Build date: 2025.04.18
License: https://www.stimulsoft.com/en/licensing/reports
"""

import re
import uuid
from enum import Enum


class StiFunctions:

### String

    def getJavaScriptValue(value) -> str:
        if value == None: return 'null'
        if isinstance(value, Enum): return 'null' if value.value == None else value.value
        if type(value) == list: return str(value)
        if type(value) == str: return f"'{value}'"
        return str(value).lower()

    def isNullOrEmpty(value) -> bool:
        return len(value or '') == 0
    
    def newGuid(length = 16) -> str:
        return uuid.uuid4().hex[:length]

    def isJavaScriptFunctionName(value) -> bool:
        return re.search("^[a-zA-Z_\x7f-\xff][a-zA-Z0-9_\x7f-\xff]*$", value)
    
    def isDashboardsProduct() -> bool:
        try:
            from stimulsoft_dashboards.report.StiDashboard import StiDashboard
        except Exception as e:
            return False
        
        return True

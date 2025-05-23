"""
Stimulsoft.Reports.JS
Version: 2025.2.4
Build date: 2025.05.19
License: https://www.stimulsoft.com/en/licensing/reports
"""

from __future__ import annotations

import codecs
import json
import typing

from ..classes.StiDataResult import StiDataResult
from ..enums.StiDataType import StiDataType
from ..enums.StiFrameworkType import StiFrameworkType
from .StiBaseResult import StiBaseResult

if typing.TYPE_CHECKING:
    from .StiBaseHandler import StiBaseHandler


class StiBaseResponse:
    """
    The result of executing an event handler request. 
    You can get the data, its type and other parameters necessary to create a web server response.
    """

### Properties

    handler: StiBaseHandler = None
    result: StiBaseResult = None

    @property
    def origin(self) -> str:
        """Returns the detected origin url for the handler response. Can be used for the 'Access-Control-Allow-Origin' header of the response."""

        return self.handler.origin

    @property
    def mimeType(self) -> str:
        """Returns the MIME type for the handler response."""

        if isinstance(self.result, StiDataResult) and self.result.dataType != None:
            return self.result.dataType

        return StiDataType.JSON.value
    
    @property
    def contentType(self) -> str:
        """Returns the content type for the handler response. Can be used for the 'Content-Type' header of the response."""

        return self.mimeType + '; charset=utf-8'
    
    @property
    def data(self) -> bytes:
        """Returns the handler response as a byte array. When using encryption, the response will be encrypted and encoded into a Base64 string."""

        if isinstance(self.result, StiDataResult) and self.result.type == 'File':
            return (self.result.data or '').encode()

        data = json.dumps(self.result, default = StiBaseResult.getProperties)
        encryptSqlData = self.handler.encryptSqlData or self.result.type != 'SQL'
        if self.handler.request.encryptData and encryptSqlData:
            data = codecs.encode(codecs.encode(data.encode(), 'base64').decode(), 'rot13')
            
        return data.encode()


### Response

    def getFrameworkResponse(self, handler = None):
        """Returns a response intended for one of the supported frameworks."""
        
        if self.handler.framework == StiFrameworkType.DJANGO:
            try:
                from django.http import HttpResponse
                contentType = self.contentType
                response = HttpResponse(self.data, content_type = contentType)
                response.headers['Access-Control-Allow-Origin'] = self.origin
                response.headers['X-Stimulsoft-Result'] = self.result.type
                return response
            except:
                return self

        if self.handler.framework == StiFrameworkType.FLASK:
            try:
                from flask import make_response
                response = make_response(self.data)
                response.headers.set('Content-Type', self.contentType)
                response.headers.set('Access-Control-Allow-Origin', self.origin)
                response.headers.set('X-Stimulsoft-Result', self.result.type)
                return response
            except:
                return self
            
        if self.handler.framework == StiFrameworkType.TORNADO:
            try:
                from tornado.web import RequestHandler as TornadoRequestHandler
                if isinstance(handler, TornadoRequestHandler):
                    handler.set_header('Content-Type', self.contentType)
                    handler.set_header('Access-Control-Allow-Origin', self.origin)
                    handler.set_header('X-Stimulsoft-Result', self.result.type)
                    handler.write(self.data)
                    return None

                return self
            except:
                return self

        return self
    

### Constructor

    def __init__(self, handler: StiBaseHandler, result: StiBaseResult = None):
        self.handler = handler
        self.result = result if result != None else self.handler.getResult()

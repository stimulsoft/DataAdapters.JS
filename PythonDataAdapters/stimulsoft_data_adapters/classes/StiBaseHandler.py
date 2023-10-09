"""
Stimulsoft.Reports.JS
Version: 2023.4.1
Build date: 2023.10.06
License: https://www.stimulsoft.com/en/licensing/reports
"""

from .StiBaseResult import StiBaseResult
from .StiBaseRequest import StiBaseRequest
from .StiBaseResponse import StiBaseResponse
from ..enums.StiDataCommand import StiDataCommand
from ..enums.StiDatabaseType import StiDatabaseType
from ..enums.StiFrameworkType import StiFrameworkType
from ..StiDataAdapter import StiDataAdapter
from ..events.StiEvent import StiEvent
from ..events.StiDataEventArgs import StiDataEventArgs
import codecs
import urllib.parse

class StiBaseHandler:
    """
    Event handler for all requests from the report generator. 
    The incoming request is processed, a data adapter is created and all necessary actions are performed.
    """

    version: str = '2023.4.1'
    checkDataAdaptersVersion: bool = True
    framework: str = StiFrameworkType.DEFAULT
    origin: str = None
    query: dict = None
    body: str = None
    error: str = None
    request: StiBaseRequest = None
    dataAdapter: StiDataAdapter = None


### Private

    __url: str = None


### Properties
    
    @property
    def url(self):
        return '' if self.__url == None else self.__url

### Events

    onBeginProcessData: StiEvent = None
    """The event is invoked before data request, which needed to render a report."""

    onEndProcessData: StiEvent = None
    """The event is invoked after loading data before rendering a report."""


### Private

    def __setQuery(self, query: dict | str) -> None:
        if query != None:
            self.query = query if isinstance(query, dict) else dict(urllib.parse.parse_qsl(query))

    def __setBody(self, body: bytes | str) -> None:
        if body != None:
            self.body = body if type(body) == str else codecs.decode(body)

    def __processFrameworkRequest(self, request: object) -> bool:
        try:
            from django.http import HttpRequest as DjangoRequest
            if isinstance(request, DjangoRequest):
                self.__setQuery(request.GET)
                self.__setBody(request.body)
                self.origin = '{0}://{1}'.format(request.scheme, request.get_host())
                self.framework = StiFrameworkType.DJANGO
                return True
        except Exception as e:
            self.error = 'Request: ' + str(e)
            return False

        try:
            from flask import Request as FlaskRequest
            if isinstance(request, FlaskRequest):
                self.__setQuery(request.args.to_dict())
                self.__setBody(request.get_data(False))
                self.origin = request.origin
                self.framework = StiFrameworkType.FLASK
                return True
        except Exception as e:
            self.error = 'Request: ' + str(e)
            return False

        try:
            from tornado.httputil import HTTPServerRequest as TornadoRequest
            if isinstance(request, TornadoRequest):
                self.__setQuery(request.query)
                self.__setBody(request.body)
                self.origin = '{0}://{1}'.format(request.protocol, request.host)
                self.framework = StiFrameworkType.TORNADO
                return True
        except Exception as e:
            self.error = 'Request: ' + str(e)
            return False
        
        return True

    def __getSupportedDataAdaptersResult(self) -> StiBaseResult:
        result = StiBaseResult.getSuccess()
        result.types = StiDatabaseType.getTypes()
        result.handlerVersion = self.version
        return result
    
    def __processParameters(self):
        parameters = []
        if self.request.queryString != None and self.request.parameters != None and len(self.request.parameters) > 0:
            for item in self.request.parameters:
                name = item.name.find('@') == 0 or item.name.find(':') == 0 if item.name[1] else item.name
                parameters[name] = item
                del item.name

        self.request.parameters = parameters
    
    def __getDataAdapterResult(self):
        args = StiDataEventArgs(self, self.request)
        self.onBeginProcessData(args)

        self.dataAdapter = StiDataAdapter.getDataAdapter(args.database, args.connectionString)
        if self.dataAdapter == None:
            return StiBaseResult.getError(f'Unknown database type: {args.database}')

        if self.request.command == StiDataCommand.RETRIEVE_SCHEMA:
            args.result = self.dataAdapter.executeQuery(args.dataSource)
            self.onEndProcessData(args)
            return args.result

        if self.request.command == StiDataCommand.EXECUTE or self.request.command == StiDataCommand.EXECUTE_QUERY:
            try:
                from ..StiMongoDbAdapter import StiMongoDbAdapter
                if (isinstance(self.dataAdapter, StiMongoDbAdapter)):
                    args.queryString = args.dataSource
            except:
                pass

            if self.request.command == StiDataCommand.EXECUTE:
                args.queryString = self.dataAdapter.makeQuery(args.queryString, args.parameters)

            if len(args.parameters) > 0:
                args.queryString = StiDataAdapter.applyQueryParameters(args.queryString, args.parameters, self.request.escapeQueryParameters)

            args.result = self.dataAdapter.executeQuery(args.queryString)
            self.onEndProcessData(args)
            return args.result
        
        return self.dataAdapter.test()
    

### Protected

    def _createRequest(self):
        return StiBaseRequest()
    
    def _checkCommand(self):
        commands = [getattr(StiDataCommand, field) for field in dir(StiDataCommand) if not callable(getattr(StiDataCommand, field)) and not field.startswith('_')]
        if self.request.command in commands:
            return True
        
        return False

### Public

    def processRequest(self, request: object = None, query: dict | str = None, body: bytes | str = None) -> bool:
        """The request process, reading all passed parameters, retrieving data from the database, and other necessary actions of the event handler."""

        self.error = None

        if request != None:
            self.__processFrameworkRequest(request)
            if (self.error != None):
                return False
        
        if self.framework == StiFrameworkType.DEFAULT:
            try:
                self.__setQuery(query)
                self.__setBody(body)
            except Exception as e:
                self.error = 'Request: ' + str(e)
                return False
        
        self.request = self._createRequest()
        self.request.process(self.query, self.body)
        if len(self.request.error or '') > 0:
            self.error = self.request.error
            return False
        
        if not self._checkCommand():
            self.error = f'Unknown command: {self.request.command}'
            return False
        
        return True

    def getFrameworkResponse(self) -> object:
        """
        Returns a response intended for one of the supported frameworks specified in the arguments. 
        The supported frameworks are in the 'StiFrameworkType' enum. 
        If the framework is not specified, it will be determined based on the request.
        """

        return self.getResponse().getFrameworkResponse()

    def getResponse(self) -> StiBaseResponse:
        """
        The result of executing an event handler request.
        You can get the data, its type and other parameters necessary to create a web server response.
        """
        
        return StiBaseResponse(self)

    def getResult(self):
        """
        The result of executing an event handler request. 
        The result contains a collection of data, message about the result of the command execution, and other technical information.
        """

        if len(self.error or '') > 0:
            result = StiBaseResult.getError(self.error)
            result.handlerVersion = self.version
            return result
        
        if self.request.command == StiDataCommand.GET_SUPPORTED_ADAPTERS:
            return self.__getSupportedDataAdaptersResult()

        self.__processParameters()
        result = self.__getDataAdapterResult()
        result.handlerVersion = self.version
        return result
    

### Constructor

    def __init__(self, url: str = None):
        self.onBeginProcessData = StiEvent('onBeginProcessData')
        self.onEndProcessData = StiEvent('onEndProcessData')
        self.__url = url
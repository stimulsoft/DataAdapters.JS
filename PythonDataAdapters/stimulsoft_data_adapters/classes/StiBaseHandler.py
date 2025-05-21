"""
Stimulsoft.Reports.JS
Version: 2025.2.4
Build date: 2025.05.19
License: https://www.stimulsoft.com/en/licensing/reports
"""

import codecs
import urllib.parse

from ..classes.StiDataResult import StiDataResult
from ..classes.StiFunctions import StiFunctions
from ..classes.StiParameter import StiParameter
from ..enums.StiBaseEventType import StiBaseEventType
from ..enums.StiDatabaseType import StiDatabaseType
from ..enums.StiDataCommand import StiDataCommand
from ..enums.StiFrameworkType import StiFrameworkType
from ..events.StiDataEventArgs import StiDataEventArgs
from ..events.StiEvent import StiEvent
from ..StiDataAdapter import StiDataAdapter
from .StiBaseRequest import StiBaseRequest
from .StiBaseResponse import StiBaseResponse
from .StiBaseResult import StiBaseResult


class StiBaseHandler:
    """
    Event handler for all requests from the report generator. Processes the incoming request, communicates with data adapters, 
    prepares parameters and triggers events, and performs all necessary actions. After this, the event handler prepares a 
    response for the web server.
    """

### Fields

    __events: dict = None
    __url: str = None
    __requestCookies = None


### Properties

    version = '2025.2.3'
    """Current version of the event handler."""
    
    checkDataAdaptersVersion = True
    """Enables checking for client-side and server-side data adapter versions to match."""

    framework = StiFrameworkType.DEFAULT
    origin: str = None
    query: dict = None
    body: str = None
    error: str = None
    request: StiBaseRequest = None
    frameworkRequest: object = None
    dataAdapter: StiDataAdapter = None

    passQueryParameters = False
    """Enables automatic passing of GET parameters from the current URL to event handler requests."""

    encryptSqlData = True
    """
    Enables encryption of SQL data transmitted from the server to the report generator.
    This improves security but slows down the processing of large data.
    """
    
    @property
    def url(self):
        #return self.__url or ''
        
        url = self.__url or ''
        if self.passQueryParameters:
            pass
            """
            foreach ($_GET as $key => $value)
                if (strpos($url, $key) === false) {
                    $url .= strpos($url, '?') === false ? '?' : '&';
                    $url .= "$key=" . rawurlencode($value);
                }
            """

        return url
    
    @url.setter
    def url(self, value):
        self.__url = value


### Events

    @property
    def onDatabaseConnect(self) -> StiEvent:
        """The event is invoked before connecting to the database after all parameters have been received. Only Python functions are supported."""
        return self._getEvent('onDatabaseConnect')

    @onDatabaseConnect.setter
    def onDatabaseConnect(self, value):
        self._setEvent('onDatabaseConnect', value)


    @property
    def onBeginProcessData(self) -> StiEvent:
        """The event is invoked before data request, which needed to render a report. Python and JavaScript functions are supported."""
        return self._getEvent('onBeginProcessData')

    @onBeginProcessData.setter
    def onBeginProcessData(self, value):
        self._setEvent('onBeginProcessData', value)


    @property
    def onEndProcessData(self) -> StiEvent:
        """The event is invoked after loading data before rendering a report. Python and JavaScript functions are supported."""
        return self._getEvent('onEndProcessData')

    @onEndProcessData.setter
    def onEndProcessData(self, value):
        self._setEvent('onEndProcessData', value)


### Helpers

    def __setQuery(self, query: dict | str) -> None:
        if query != None:
            self.query = query if isinstance(query, dict) else dict(urllib.parse.parse_qsl(query))

    def __setBody(self, body: bytes | str) -> None:
        if body != None:
            self.body = body if type(body) == str else codecs.decode(body)

    def __removeResourceParameters(self, url: str) -> str:
        query = urllib.parse.urlparse(url).query
        if StiFunctions.isNullOrEmpty(query):
            return url
        
        params = []
        remove = ['sti_event', 'sti_data']
        for param, values in urllib.parse.parse_qs(query).items():
            if param not in remove:
                for value in values:
                    params.append((param, value))

        baseUrl = url[:url.find('?')]
        return baseUrl if len(params) == 0 else baseUrl + '?' + urllib.parse.urlencode(params)
    
    def _createRequest(self):
        return StiBaseRequest()
    
    def _checkEvent(self):
        return self.request.event.value in StiBaseEventType.getValues(True)
    
    def _checkCommand(self):
        return self.request.command.value in StiDataCommand.getValues()

    def _getEvent(self, name) -> StiEvent:
        event = self.__events.get(name)
        if event == None:
            event = StiEvent(self, name)
            self.__events[name] = event

        return event
    
    def _setEvent(self, name, value):
        if isinstance(value, StiEvent):
            self.__events[name] = value
        elif callable(value) or isinstance(value, (bool, str)):
            self._getEvent(name).append(value)

    def _setEvents(self, events: dict):
        self.__events = events


### Process

    def __processFrameworkRequest(self, request: object) -> bool:
        try:
            from django.http import HttpRequest as DjangoRequest
            if isinstance(request, DjangoRequest):
                # This code is needed to update CSRF token in cookies
                from django.middleware.csrf import get_token
                get_token(request)

                self.__setQuery(request.GET)
                self.__setBody(request.body)
                self.__requestCookies = request.COOKIES
                self.url = self.url or self.__removeResourceParameters(request.build_absolute_uri())
                self.origin = '{0}://{1}'.format(request.scheme, request.get_host())
                self.framework = StiFrameworkType.DJANGO
                self.frameworkRequest = request
                return True
        except Exception as e:
            if not isinstance(e, ModuleNotFoundError):
                self.error = 'Request: ' + str(e)
                return False

        try:
            from flask import Request as FlaskRequest
            if isinstance(request, FlaskRequest):
                self.__setQuery(request.args.to_dict())
                self.__setBody(request.get_data(False))
                self.__requestCookies = request.cookies
                self.url = self.url or self.__removeResourceParameters(request.base_url)
                self.origin = request.origin
                self.framework = StiFrameworkType.FLASK
                self.frameworkRequest = request
                return True
        except Exception as e:
            if not isinstance(e, ModuleNotFoundError):
                self.error = 'Request: ' + str(e)
                return False

        try:
            from tornado.httputil import HTTPServerRequest as TornadoRequest
            if isinstance(request, TornadoRequest):
                self.__setQuery(request.query)
                self.__setBody(request.body)
                self.__requestCookies = request.cookies
                self.url = self.url or self.__removeResourceParameters(request.full_url())
                self.origin = '{0}://{1}'.format(request.protocol, request.host)
                self.framework = StiFrameworkType.TORNADO
                self.frameworkRequest = request
                return True
        except Exception as e:
            if not isinstance(e, ModuleNotFoundError):
                self.error = 'Request: ' + str(e)
                return False
        
        self.error = 'Unsupported request: ' + str(request.__class__)
        return False
    
    def __processParameters(self):
        parameters = dict()
        if len(self.request.parameters or '') > 0 and len(self.request.queryString or '') > 0:
            for item in self.request.parameters:
                name = item['name'][1:] if item['name'][0] == '@' or item['name'][0] == ':' else item['name']
                parameters[name] = StiParameter(name, item['type'], item['typeName'], item['typeGroup'], item['size'], item['value'])

        self.request.parameters = parameters

    def processRequest(self, request: object = None, query: dict | str = None, body: bytes | str = None) -> bool:
        """
        Processing an HTTP request from the client side of the component. If successful, it is necessary to return a response 
        with the processing result, which can be obtained using the 'getResponse()' or 'getFrameworkResponse()' functions.
        
        request:
            A request object for one of the supported frameworks.

        query:
            The GET query string if no framework request is specified.
        
        body:
            The POST form data if no framework request is specified.

        return:
            True if the request was processed successfully.
        """

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
        
        if not self._checkEvent():
            self.error = f'Unknown event: {self.request.event.value}'
            return False
        
        if not self._checkCommand():
            self.error = f'Unknown command: {self.request.command.value}'
            return False
        
        return True
    

### Results

    def __getSupportedDataAdaptersResult(self) -> StiBaseResult:
        result: StiBaseResult = StiBaseResult.getSuccess()
        result.types = StiDatabaseType.getValues()
        result.handlerVersion = self.version
        return result
    
    def __getDataResult(self, result: StiBaseResult, notice: str, args: StiDataEventArgs) -> StiBaseResult:

        # The event did not return any result, the result of the data adapter is used
        if result == None:
            result = args.result

        # Copying message from event if data adapter message is empty
        if StiFunctions.isNullOrEmpty(args.result.notice):
            args.result.notice = result.notice if not StiFunctions.isNullOrEmpty(result.notice) else notice

        # If the result from the event is successful, use the result of the data adapter
        if result.success:
            return args.result

        # Passing data adapter parameters
        if isinstance(result, StiDataResult):
            result = result.getDataAdapterResult(self.dataAdapter)

        return result
    
    def __getDataAdapterResult(self):
        args = StiDataEventArgs(self.request)
        result = self.onBeginProcessData.getResult(args)
        if result != None and not result.success:
            return result
        
        # Saving a message to return in the results of the next events
        notice = result.notice if result != None else None

        # Prepare the connection string or the URL of the data file
        connectionString = args.connectionString
        if self.request.command == StiDataCommand.GET_DATA or self.request.command == StiDataCommand.GET_SCHEMA:
            connectionString = args.pathData if self.request.command == StiDataCommand.GET_DATA else args.pathSchema

        # Get the necessary data adapter
        self.dataAdapter: StiDataAdapter = StiDataAdapter.getDataAdapter(args.database, connectionString)
        if self.dataAdapter == None:
            return StiBaseResult.getError(f'Unknown database type: {args.database}')
        
        self.dataAdapter.handler = self

        # Get the data source schema
        if self.request.command == StiDataCommand.RETRIEVE_SCHEMA:
            args.result = self.dataAdapter.getDataResult(args.dataSource, args.maxDataRows)
            result = self.onEndProcessData.getResult(args, StiDataResult)
            return self.__getDataResult(result, notice, args)

        # Process SQL data
        if self.request.command == StiDataCommand.EXECUTE or self.request.command == StiDataCommand.EXECUTE_QUERY:

            # The MongoDB data source does not contain a connection string
            # Using the data source name to find a match from the MongoDB data object
            try:
                from ..StiMongoDbAdapter import StiMongoDbAdapter
                if isinstance(self.dataAdapter, StiMongoDbAdapter):
                    args.queryString = args.dataSource
            except:
                pass

            if self.request.command == StiDataCommand.EXECUTE:
                args.queryString = self.dataAdapter.makeQuery(args.queryString, args.parameters)

            if len(args.parameters) > 0:
                from ..StiSqlAdapter import StiSqlAdapter
                args.queryString = StiSqlAdapter.applyQueryParameters(args.queryString, args.parameters, self.request.escapeQueryParameters)

            args.result = self.dataAdapter.getDataResult(args.queryString, args.maxDataRows)
            result = self.onEndProcessData.getResult(args, StiDataResult)
            return self.__getDataResult(result, notice, args)

        # Process file data
        if self.request.command == StiDataCommand.GET_DATA or self.request.command == StiDataCommand.GET_SCHEMA:
            args.result = self.dataAdapter.getDataResult(connectionString)
            result = self.onEndProcessData.getResult(args, StiDataResult)

            # If the server side event is not set, the result is always successful
            # Required for loading file data on the JavaScript client-side
            if not self.onEndProcessData.hasServerCallbacks():
                args.result.success = True

            return self.__getDataResult(result, notice, args)
        
        return self.dataAdapter.test()

    def getFrameworkResponse(self, handler = None) -> object:
        """Returns the result of processing a request from the client side intended for one of the supported frameworks."""

        return self.getResponse().getFrameworkResponse(handler)

    def getResponse(self) -> StiBaseResponse:
        """
        Returns the result of processing a request from the client side. The response object will contain the data for the response, 
        as well as their MIME type, Content-Type, and other useful information to create a web server response.
        """
        
        return StiBaseResponse(self)

    def getResult(self):
        """
        Returns the result of processing a request from the client side. The result object will contain a collection of data, 
        message about the result of the command execution, and other technical information.
        """

        if len(self.error or '') > 0:
            result: StiBaseResult = StiBaseResult.getError(self.error)
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
        self.__events = dict()
        self.__url = url

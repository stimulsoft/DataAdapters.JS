# Stimulsoft data adapters for Python.

This project is a simple Web server written in Python using a Flask framework. You can use any web server and framework, the code examples below show how to use Flask, Django, and Tornado.


## Prepare to Start

To install the **Stimulsoft data adapters for Python**, you can use the specified command:
```
python -m pip install stimulsoft-data-adapters
```
All supported data adapters will be installed, as well as the universal **pyodbc** data driver, which supports most databases. If necessary, you can install any additional native data driver from the list below.

To install **Stimulsoft data adapters for Python** with all the necessary data drivers, you can use the following command:
```
python -m pip install stimulsoft-data-adapters[ext]
```

Before start this project, you also need to install the Flask framework, this can be done using the specified command:
```
python -m pip install Flask
```


## Start the project

To start the web server, it is enough to execute the specified command:
```
python app.py
```
After launching, open this URL in the browser:
```
http://127.0.0.1:8040
```
The data adapter event handler runs on the following address, which must be configured in the JS application:
```
http://127.0.0.1:8040/handler
```


## Working with data adapters

To start working with data adapters, it is enough to define the **StiBaseHandler** class, call **processRequest()** function which accepts HTTP request data as input, and generates a response that needs to be passed to the report generator.

The **StiBaseHandler** class supports simplified work with the Flask, Django, and Tornado frameworks. To process the request, it is enough to pass the request object to the handler, and return a response generated specifically for the framework.

### Flask

```
from flask import Flask, request
from stimulsoft_data_adapters import StiBaseHandler

@app.route('/handler', methods = ['GET', 'POST'])
def handler():
    handler = StiBaseHandler()
    handler.processRequest(request)
    return handler.getFrameworkResponse()
```

### Django

```
from django.http import HttpRequest
from stimulsoft_data_adapters import StiBaseHandler

def handler(request: HttpRequest):
    handler = StiBaseHandler()
    handler.processRequest(request)
    return handler.getFrameworkResponse()
```

### Tornado

```
from tornado.web import Application, RequestHandler
from stimulsoft_data_adapters import StiBaseHandler

class Handler(RequestHandler):
    def post(self):
        handler = StiBaseHandler()
        handler.processRequest(self.request)
        return handler.getFrameworkResponse(self)
```

For all other cases, it is enough to pass query vars and the request body to the handler. After that, you can get a response from the handler, which will contain the data and the necessary information.

```
from stimulsoft_data_adapters import StiBaseHandler

def handler():
    handler = StiBaseHandler()
    handler.processRequest(None, query, body)
    response = handler.getResponse()
    data = response.data
    contentType = response.contentType
    mimetype = response.mimetype
```

## Data adapter events

The handler provides two events: **onBeginProcessData** and **onEndProcessData**, which occur before connecting to the database and after receiving data.

```
from stimulsoft_data_adapters import StiBaseHandler
from stimulsoft_data_adapters.events import StiDataEventArgs

@app.route('/handler', methods = ['GET', 'POST'])
def handler():
    handler = StiBaseHandler()
    handler.onBeginProcessData += beginProcessData
    handler.onEndProcessData += endProcessData
    handler.processRequest(request)
    return handler.getFrameworkResponse()
```

### onBeginProcessData

In the event args, you can get and change all connection parameters, such as connection string, SQL query, connection name, connection type, data source name and others.

```
def beginProcessData(args: StiDataEventArgs):
    args.command
    args.database
    args.connection
    args.connectionString = args.connectionString.replace('Pwd=;', 'Pwd=**********;')
    args.queryString
    args.dataSource
```

### onEndProcessData

The event args, in addition to all connection parameters, will contain the result of the data request. It is a set of three arrays - column names, column types and data rows. All values can be changed in the event.

```
def endProcessData(args: StiDataEventArgs):
    args.result.columns
    args.result.types
    args.result.rows
```


## Install database drivers

By default, without extras, only the data adapters will be installed. All required database drivers must be installed manually. This may be useful for some cases and certain operating systems, or for installing only the necessary drivers.

### MS SQL

To use the **MS SQL data adapter**, you need to install the specified package:
```
python -m pip install "pymssql[binary]"
```
Standard connection strings for MS SQL databases are supported.

You can also use the ODBC driver for MS SQL. For this, you need to install the [Microsoft ODBC Driver for SQL Server](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16) for your operation system. After this, you need to add the name of the ODBC driver to the connection string, for example:
```
Driver={ODBC Driver 18 for SQL Server}; Data Source=myServerAddress; 
Initial Catalog=myDataBase; User ID=myUsername; Password=myPassword;
```
Also, additional connection string parameters are supported:
```
TrustServerCertificate=Yes;
```

### MySQL

To use the **MySQL data adapter**, you need to install the specified package:
```
python -m pip install mysql-connector-python
```
Standard connection strings for MySQL databases are supported.

You can also use the ODBC driver for MySQL. For this, you need to install the [Connector/ODBC for MySQL](https://dev.mysql.com/downloads/connector/odbc/) for your operation system. After this, you need to add the name of the ODBC driver to the connection string, for example:

```
Driver={MySQL ODBC 8.1 UNICODE Driver}; Server=myServerAddress; 
Database=myDataBase; UserId=myUsername; Pwd=myPassword;
```

### PostgreSQL

To use the **PostgreSQL data adapter**, you need to install the specified package:
```
python -m pip install "psycopg[binary]"
```
Standard connection strings for PostgreSQL databases are supported.

You can also use the ODBC driver for PostgreSQL. For this, you need to install the [PostgreSQL ODBC Driver](https://odbc.postgresql.org/) for your operation system. After this, you need to add the name of the ODBC driver to the connection string, for example:

```
Driver={PostgreSQL Unicode}; Server=myServerAddress; Port=5432; 
Database=myDataBase; User Id=myUsername; Password=myPassword;
```

### Firebird

To use the **Firebird data adapter**, you need to install the specified package:
```
python -m pip install firebird-driver
```
Standard connection strings for Firebird databases are supported.

You can also use the ODBC driver for Firebird. For this, you need to install the [Firebird ODBC Driver](https://firebirdsql.org/en/odbc-driver/) for your operation system. After this, you need to add the name of the ODBC driver to the connection string, for example:

```
Driver={Firebird/InterBase(r) driver}; User=SYSDBA; Password=masterkey; 
Database=SampleDatabase.fdb; DataSource=myServerAddress; Port=3050;
```

### Oracle

To use the **Oracle data adapter**, you need to install the specified package:
```
python -m pip install oracledb
```
To run the driver, you will also need to install [Oracle Instant Client](https://www.oracle.com/pl/database/technologies/instant-client/downloads.html) for your operating system, and if required, add the path to it to the environment variables. Standard connection strings for Oracle databases are supported.

You can also use the ODBC driver for Oracle. For this, you need to install the [Oracle Instant Client ODBC](https://www.oracle.com/pl/database/technologies/releasenote-odbc-ic.html) for your operation system. After this, you need to add the name of the ODBC driver to the connection string, for example:

```
Driver={Oracle in instantclient_19_20}; Data Source=TORCL; 
User Id=myUsername; Password=myPassword;
```

### MongoDB

To use the **MongoDB data adapter**, you need to install the specified package:
```
python -m pip install "pymongo[srv]"
```
Standard connection strings for MongoDB databases are supported.

### ODBC

To use the **ODBC data adapter**, you need to install the specified package (if for some reason it was not installed automatically with the data adapter package):
```
python -m pip install pyodbc
```
After that, you can create a native ODBC connection in the Report Designer using any supported driver specified on [this page](https://github.com/mkleehammer/pyodbc/wiki).

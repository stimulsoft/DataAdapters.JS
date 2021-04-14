

Since pure JavaScript does not have built-in methods for working with remote databases, this functionality is implemented using server-side code. Therefore, Stimulsoft Reports.JS product contains server data adapters implemented using PHP, Node.JS, ASP.NET, Java technologies.
 
The database adapter is a software layer between the DBMS and the client script. The adapter connects to the DBMS and retrieves the necessary data, converting it into JSON. The script running on the server (using the adapter) provides for the exchange of JSON data between the client-side JavaScript application and the server side.
 
To use this mechanism on the clint side, you should specify the URL address of the host adapter, which processes requests to a required adapter

Links to examples with ready data adapters, implemented for various platforms:  
* [Node.js](https://github.com/stimulsoft/Samples-JS/tree/master/Node.js/04.%20Start%20SQL%20Adapters%20from%20Http%20Server)
* [PHP](https://github.com/stimulsoft/Samples-JS/tree/master/PHP/02.%20Connect%20to%20databases)
* [.NET](https://github.com/stimulsoft/Samples-JS/tree/master/ASP.NET/02.%20Connect%20to%20databases)
* [Java](https://github.com/stimulsoft/Samples-JS/tree/master/Java/01.%20Data%20Adapter)

## How to use
It`s easy to use an adapter.  
You should run an adapter and specify the its address:
```js
StiOptions.WebServer.url = "http://localhost:9615";
```

## How it works
When requesting data from SQL data sources, the Stimulsoft.Report.Engine sends a POST request to the URL, specified in the option:  
```js
StiOptions.WebServer.url = "https://localhost/handler.php";
```

A JSON object with parameters is passed in the body of the request that use the following structure:
* `command`: two variants are possible - "*TestConnection*" и "*ExecuteQuery*"
* `connectionString`: database connection string
* `queryString`: query string
* `database`: database type
* `timeout`: the time of request waiting, specified in the data source
* `parameters`: an array of parameters as a JSON object {name, value}
* `escapeQueryParameters`: a flag of parameters shielding before requesting

In response, the Stimulsoft.Report.Engine expects a JSON object with data in the form of the following structure:
* `success`: a flag of successful command execution
* `notice`: if the flag of command execution has the false value, this parameter will contain an error description
* `rows`: strings array, each element is the array of values, the index is the column number
* `columns`: an array of column names, index is the column number
* `types`: an array of column types, the index is the column number. It can take the values "*string*", "*number*", "*int*", "*boolean*", "*array*", "*datetime*"

Request and responce sample:
```js
request = {
    command: "ExecuteQuery",
    connectionString: "Server=myServerAddress;Database=myDataBase;User Id=myUsername;Password=myPassword;",
    queryString: "select * from table1",
    database: "MS SQL"
}

response = {
    success: true,

    rows: [
        ["value1", 1, false],
        ["value2", 1, true]
        ["value3", 2, false]
    ],
    columns: [
        "Column1_name",
        "Column2_name",
        "Column3_name"
    ],
    types:[
        "string",
        "int",
        "boolean"
    ]
}
```
  


## CustomDataAdapter
Also, there is the ability to registrate own data adapter. To do it you should invoke the following option:
```js
Stimulsoft.Report.Dictionary.StiCustomDatabase.registerCustomDatabase(options);
```

The options are the set of properties and the `process()` function, which will be invoked when requesting data:
* `serviceName`: adapter name which will be displayed in the designer when creating a new connection
* `sampleConnectionString`: the sample of a connection string that is inserted in the form of setting up a new connection
* `process`: the function, which will be invoked to prepareband transmit data to the Stimulsoft.Report.Engine
            
Two arguments are transmitted to the input of the `process()` function: `command` and` callback`. 

The `command` argument is the JSON object, where the Stimulsoft.Report.Engine will transfer the following parameters:

* `command`: action, which is being invoked at the moment. Possible values:
    "*TestConnection*": test the database connection from the new connection creation form
    "*RetrieveSchema*": retrieving data schema is needed to optimize a request and not only to transfer necessary data set. It is invokes after connection creation
    "*RetrieveData*": data request
* `connectionString`: connection string
* `queryString`: query string
* `database`: database type
* `timeout`: the time of request waiting, specified in the data source

The `callback` argument is the function, which should be invoked to transmit prepared data to the Stimulsoft.Report.Engine. As the `callback` argument to the functions you must pass a JSON object with the following parameters:
* `success`: the flag of successful command execution
* `notice`: if the flag of command execution has the false value, this parameter should contain an error description
* `rows`: strings array, each element is the array from values, the index is the column number
* `columns`: columns name array, the index is the column number
* `types`: the object where field name is column name and the value is the type of the column {Column_Name : "string"}. The type can take the following values "*string*", "*number*", "*int*", "*boolean*", "*array*", "*datetime*". If the `columns` array will be transmitted, you will be able to transmit types array to the `types`, the index should be column number. It doesn`t work for the "*RetrieveSchema*"

If the command = "*RetrieveSchema*", then in addition types you should transmit table names to the `types`.

The sample of a request and response when receiving a schema:
```js
request = {
    command: "RetrieveSchema"
}

response = {
    success: true,
    
    types:{
        Table1: {
            Column1: "string",
            Column2: "number"
        },
        Table2: {
            Column1: "string"
        }
    }
}
```

The sample of a request and response when getting data:
```js
request = {
    command: "RetrieveData",
    queryString: "Table1"
}

response = {
    success: true,
    
    rows: [
        ["value1", 1],
        ["value2", 1]
        ["value3", 2]
    ],
    columns:[
        "Column1",
        "Column2"
    ],
    types:[
        "string",
        "number"
    ]
}
```

[The example of adapter registration](https://github.com/stimulsoft/Samples-JS/blob/master/JavaScript/Working%20with%20report%20designer/08.%20Custom%20DataAdapter.html)

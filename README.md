

Поскольку чистый JavaScript не имеет встроенных методов для работы с удаленными базами данных, эта функциональность реализуется с помощью серверного кода. Поэтому продукт Stimulsoft Reports.JS содержит серверные адаптеры данных, реализованные с использованием технологий PHP, Node.JS, ASP.NET, Java.
 
Адаптер базы данных - это программный уровень между СУБД и клиентским скриптом. Адаптер подключается к СУБД и извлекает необходимые данные, конвертируя их в JSON. Сценарий, запущенный на сервере (с использованием адаптера), обеспечивает обмен данными между клиентским приложением JavaScript и серверной частью.
 
Чтобы использовать этот механизм на стороне клиента, достаточно указать URL-адрес хоста адаптера, который обрабатывает запросы к необходимому адаптеру.

Ссылки на уже готовые адаптеры данных, реализованные для различных платформ:  
* [Node.js](https://github.com/stimulsoft/DataAdapters.JS/tree/main/NodejsDataAdapters) ([Пример](https://github.com/stimulsoft/Samples-JS/tree/master/Node.js/04.%20Start%20SQL%20Adapters%20from%20Http%20Server))
* [PHP](https://github.com/stimulsoft/DataAdapters.JS/tree/main/PHPDataAdapters) ([Пример](https://github.com/stimulsoft/Samples-JS/tree/master/PHP/02.%20Connect%20to%20databases))
* [.NET](https://github.com/stimulsoft/DataAdapters.JS/tree/master/NetDataAdapters) ([Пример](https://github.com/stimulsoft/Samples-JS/tree/master/ASP.NET/02.%20Connect%20to%20databases))
* [Java](https://github.com/stimulsoft/DataAdapters.JS/tree/master/JavaDataAdapters) ([Пример](https://github.com/stimulsoft/Samples-JS/tree/master/Java/01.%20Data%20Adapter))

## Как это работает
При запросе данных из SQL источников данных, JS report engine отправляет POST запрос на URL, указанный в опции:  
```js
StiOptions.WebServer.url = "https://localhost/handler.php";`
```

В теле запроса передается JSON объект с параметрами, которые используют указанную ниже структуру:
* `command`: возможны два варианта - "*TestConnection*" и "*ExecuteQuery*"
* `connectionString`: строка подключения к базе
* `queryString`: строка запроса
* `database`: тип базы данных
* `timeout`: время ожидания запроса, указанное в источнике данных
* `parameters`: масив параметров в виде JSON объекта {name, value}
* `escapeQueryParameters`: флаг экранирования параметров перед выполнением запроса

В ответ JS report engine одидает JSON объект с данными в виде следующей структуры:
* `success`: флаг успешного выполнения команды
* `notice`: если флаг выполенния команты имеет значение false, то данный параметр будет содержать описание ошибки
* `rows`: масив строк, каждый элемент - это масив из значений, индексом является номер колонки
* `columns`: масив имен колонок, индексом является номер колонки
* `types`: масив типов колонок, индексом является номер колонки. Может принимать значения "*string*", "*number*", "*int*", "*boolean*", "*array*", "*datetime*"

Пример запроса и ответа:
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
Также предусмотрена возможность зарегистрировать собственный адаптер данных. Для этого необходимо вызвать функцию:
```js
Stimulsoft.Report.Dictionary.StiCustomDatabase.registerCustomDatabase(options);
```

Опции представляют собой набор свойств и функцию `process()`, которая будет вызываться при запросе данных:
* `serviceName`: имя адаптера которое отобразится в дизанере при создании нового подключения
* `sampleConnectionString`: пример строки подключения который вставиться в форме настройки нового подключения
* `process`: функция которая вызовется для подготовки и передачи данных в Stimulsoft.Report.Engine
            
На вход функции `process()` передаются два аргумента: `command` и `callback`. 

Аргумент `command` представляет собой JSON объект, в который JS report engine передаст следующие параметры:

* `command`: действие, которое вызывается в данный момент. Возможные значения:
    "*TestConnection*": проверка соединения с базой данных из формы создания нового подключения
    "*RetrieveSchema*": извлечение схемы данных, нужно для оптимизации запроса и не передачи только необходимого набора данных. Вызывается после создания подключения
    "*RetrieveData*": запрос данных
* `connectionString`: строка подключения к базе
* `queryString`: строка SQL запроса
* `database`: тип базы данных
* `timeout`: время ожидания запроса, указанное в источнике данных

Аргумент `callback` является функцией, которую нужно вызвать для передачи подготовленных данных в JS report engine. В качестве аргумента`callback` функции необходимо передать JSON объект, имеющий указанные ниже параметры:
* `success`: флаг успешного выполнения команды
* `notice`: если флаг выполенния команты имеет значение false, то данный параметр должен содержать описание ошибки
* `rows`: масив строк, каждый элемент - это масив из значений, индексом является номер колонки
* `columns`: масив имен колонок, индексом является номер колонки
* `types`: объект где имя поля это имя колонки а значение тип колонки {Column_Name : "string"}. Тип может принимать значения "*string*", "*number*", "*int*", "*boolean*", "*array*", "*datetime*". Если будет передан масив `columns`, то в `types` можно передать масив типов, индексом должен являться номер колонки. Не работает для "*RetrieveSchema*"

Если command = "*RetrieveSchema*", то помимо типов, в `types` необходимо передать имена таблиц.

Пример запроса и ответа при получении схемы:
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

Пример запроса и ответа при получении данных:
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

[Пример регистрации адаптера](https://github.com/stimulsoft/Samples-JS/blob/master/JavaScript/Working%20with%20report%20designer/08.%20Custom%20DataAdapter.html)

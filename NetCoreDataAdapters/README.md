
### Installation and running
In order to start simply open the Visual Studio solution file in the IDE Visual Studio and run the required project. 
Then, in your code, you should specify the address to the DataAdaptersController.

index.html
```js
StiOptions.WebServer.url = "https://localhost:44355/DataAdapters";
```

In the DataAdaptersController.cs file, you can change all parameters passed from the JS client-side.

A [sample](https://github.com/stimulsoft/Samples-JS/tree/master/ASP.NET%20Core/Connecting%20to%20Databases) shows how to run an adapter.
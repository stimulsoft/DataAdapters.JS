
### Installation and running
In order to start simply open the Visual Studio solution file in the IDE Visual Studio and run the required project. Then, in your code, you should specify the address to the file Handler.ashx.

index.html
```js
StiOptions.WebServer.url = "https://localhost:44311/Handler.ashx";
```

In the Handler.ashx.cs file, you can change all parameters passed from the JS client-side.

A [sample](https://github.com/stimulsoft/Samples-JS/tree/master/ASP.NET/Connecting%20to%20Databases) shows how to run an adapter.

### Installation and running
All files from this folder are required to be copied on your PHP server (using ftp or http access interface - depending on your hosting provider). Then, in your code, you should specify the address to the file handler.php.

index.html
```js
StiOptions.WebServer.url = "http://example.com/handler.php";
```

If you use the PHP server installed on local developers computer:
index.html
```js
StiOptions.WebServer.url = "http://localhost/handler.php";
```

In the handler.php file, you can change all parameters passed from the JS client-side.

A [sample](https://github.com/stimulsoft/Samples-Dashboards.JS-for-Node.js/tree/master/Starting%20SQL%20adapters%20from%20the%20HTTP%20server) shows how to run an adapter.
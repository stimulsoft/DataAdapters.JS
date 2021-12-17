
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

A [sample](https://github.com/stimulsoft/Samples-JS/tree/master/PHP/02.%20Connect%20to%20databases) shows how to run an adapter.
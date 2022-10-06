/*
Stimulsoft.Reports.JS
Version: 2022.4.2
Build date: 2022.10.06
License: https://www.stimulsoft.com/en/licensing/reports
*/

function getCommand(data) {
    var encryptResult = false;
    if (typeof data === "string" && !data.startsWith("{")) {
        data = Buffer.from(data.replace(/[A-Za-z]/g, function (c) {
            return String.fromCharCode(c.charCodeAt(0) + (c.toUpperCase() <= "M" ? 13 : -13));
        }), "base64").toString("ascii");
        encryptResult = true;
    }

    var command = JSON.parse(data.toString());
    command.encryptResult = encryptResult;
    return command;
}

function process(command, onResult) {
    if (typeof command !== "object") command = getCommand(command);

    var onProcessHandler = onProcess.bind(null, onResult, command.encryptResult);

    if (command.command === "GetSupportedAdapters") {
        onProcessHandler({ success: true, types: ["MySQL", "MS SQL", "Firebird", "PostgreSQL"] });
    } else {
        command.queryString = applyQueryParameters(command.queryString, command.parameters, command.escapeQueryParameters);

        if (command.database == "MySQL") {
            var MySQLAdapter = require('./MySQLAdapter');
            MySQLAdapter.process(command, onProcessHandler);
        }
        else if (command.database == "Firebird") {
            var FirebirdAdapter = require('./FirebirdAdapter');
            FirebirdAdapter.process(command, onProcessHandler);
        }
        else if (command.database == "MS SQL") {
            var MSSQLAdapter = require('./MSSQLAdapter');
            MSSQLAdapter.process(command, onProcessHandler);
        }
        else if (command.database == "PostgreSQL") {
            var PostgreSQLAdapter = require('./PostgreSQLAdapter');
            PostgreSQLAdapter.process(command, onProcessHandler);
        }
        else onProcessHandler({ success: false, notice: "Database '" + command.database + "' not supported!" });
    }
}

function applyQueryParameters(baseSqlCommand, parameters, escapeQueryParameters) {
    if (baseSqlCommand == null || baseSqlCommand.indexOf("@") < 0) return baseSqlCommand;

    var result = "";
    while (baseSqlCommand.indexOf("@") >= 0 && parameters != null && parameters.length > 0) {
        result += baseSqlCommand.substring(0, baseSqlCommand.indexOf("@"));
        baseSqlCommand = baseSqlCommand.substring(baseSqlCommand.indexOf("@") + 1);

        var parameterName = "";

        while (baseSqlCommand.length > 0) {
            var char = baseSqlCommand.charAt(0);
            if (char.length === 1 && char.match(/[a-zA-Z0-9_-]/i)) {
                parameterName += char;
                baseSqlCommand = baseSqlCommand.substring(1);
            }
            else break;
        }

        var parameter = parameters.find(parameter => parameter.name.toLowerCase() == parameterName.toLowerCase());
        if (parameter) {
            if (parameter.typeGroup != "number") {
                if (escapeQueryParameters)
                    result += "'" + parameter.value.toString().replace(/\\/gi, "\\\\").replace(/\'/gi, "\\\'").replace(/\"/gi, "\\\"") + "'";
                else
                    result += "'" + parameter.value.toString() + "'";
            }
            else
                result += parameter.value.toString();
        }
        else
            result += "@" + parameterName;
    }

    return result + baseSqlCommand;
}

function getResponse(result) {
    let encryptData = result.encryptData;
    delete result.encryptData;

    result = JSON.stringify(result);
    if (encryptData) {
        result = Buffer.from(result).toString("base64").replace(/[A-Za-z]/g, function (c) {
            return String.fromCharCode(c.charCodeAt(0) + (c.toUpperCase() <= "M" ? 13 : -13));
        });
    }

    return result
}
function onProcess(onResult, encryptData, result) {
    result.handlerVersion = "2022.4.2";
    result.checkVersion = true;
    result.encryptData = encryptData;
    onResult(result);
}

module.exports = { getCommand, process, getResponse };

if (require.main === module) {
    var http = require('http');
    var accept = function (request, response) {
        response.setHeader("Access-Control-Allow-Origin", "*");
        response.setHeader("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
        response.setHeader("Access-Control-Allow-Methods", "POST, GET, OPTIONS, DELETE, PUT");
        response.setHeader("Cache-Control", "no-cache");

        var data = "";
        request.on('data', function (buffer) {
            data += buffer;
        });

        request.on('end', function () {
            var command = getCommand(data);
            process(command, function (result) {
                var responseData = getResponse(result);
                response.end(responseData);
            });
        });
    }

    console.log("The DataAdapter run on port 9615");
    console.log("To use, on the client side, you need to specify the URL of this host that handles requests:");
    console.log("StiOptions.WebServer.url = \"http://localhost:9615\"");
    http.createServer(accept).listen(9615);
}


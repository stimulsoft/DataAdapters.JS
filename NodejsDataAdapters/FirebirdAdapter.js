/*
Stimulsoft.Reports.JS
Version: 2024.3.6
Build date: 2024.09.19
License: https://www.stimulsoft.com/en/licensing/reports
*/
exports.process = function (command, onResult) {
    var end = function (result) {
        try {
            if (db) db.detach();
            result.adapterVersion = "2024.3.6";
            onResult(result);
        }
        catch (e) {
        }
    }

    var onError = function (message) {
        end({ success: false, notice: message });
    }

    try {
        var connect = function () {
            Firebird.attach(options, function (error, db1) {
                db = db1;
                if (error) onError(error.message);
                else onConnect();
            });
        }

        var query = function (queryString, maxDataRows) {
            db.query(queryString, undefined, function (error, recordset) {
                if (error) onError(error.message);
                else onQuery(recordset, maxDataRows);
                db.detach();
            });
        }

        var onConnect = function () {
            if (command.queryString) {
                var queryString = applyQueryParameters(command.queryString, command.parameters, command.escapeQueryParameters);
                query(queryString, command.maxDataRows);
            }
            else end({ success: true });
        }

        var onQuery = function (recordset, maxDataRows) {
            var columns = [];
            var rows = [];
            var types = [];
            var isColumnsFill = false;
            for (var recordIndex in recordset) {
                var row = [];
                for (var columnName in recordset[recordIndex]) {
                    if (!isColumnsFill) columns.push(columnName);
                    var columnIndex = columns.indexOf(columnName);
                    types[columnIndex] = typeof recordset[recordIndex][columnName];
                    if (recordset[recordIndex][columnName] instanceof Uint8Array ||
                        recordset[recordIndex][columnName] instanceof Buffer) {
                        recordset[recordIndex][columnName] = recordset[recordIndex][columnName].toString();
                        types[columnIndex] = "string";
                    }
                    if (recordset[recordIndex][columnName] != null && typeof recordset[recordIndex][columnName].toISOString === "function") {
                        var dateTime = new Date(recordset[recordIndex][columnName].getTime() - (recordset[recordIndex][columnName].getTimezoneOffset() * 60000)).toISOString();
                        recordset[recordIndex][columnName] = dateTime.replace("Z", "");
                        types[columnIndex] = "datetime";
                    }

                    row[columnIndex] = recordset[recordIndex][columnName];
                }
                isColumnsFill = true;
                if (maxDataRows != null && maxDataRows <= rows.length) break;
                rows.push(row);
            }

            end({ success: true, columns: columns, rows: rows, types: types });
        }

        var getConnectionStringInfo = function (connectionString) {
            var info = { host: "localhost", port: "3050" };
            var isCorrect = false;
            for (var propertyIndex in connectionString.split(";")) {
                var property = connectionString.split(";")[propertyIndex];
                if (property) {
                    var match = property.split("=");
                    if (match && match.length >= 2) {
                        match[0] = match[0].trim().toLowerCase();
                        match[1] = match[1].trim();

                        switch (match[0]) {
                            case "server":
                            case "host":
                            case "location":
                            case "datasource":
                            case "data source":
                                info["host"] = match[1];
                                break;

                            case "port":
                                info["port"] = match[1];
                                break;

                            case "database":
                                info["database"] = match[1];
                                isCorrect = true;
                                break;

                            case "uid":
                            case "user":
                            case "user id":
                                info["userId"] = match[1];
                                break;

                            case "pwd":
                            case "password":
                                info["password"] = match[1];
                                break;

                            case "charset":
                                info["charset"] = match[1];
                                break;
                        }
                    }
                }
            }
            if (!isCorrect) {
                onError("Connection String parse error");
                return null;
            }
            return info;
        };

        var applyQueryParameters = function (baseSqlCommand, parameters, escapeQueryParameters) {
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

        var Firebird = require('node-firebird');
        command.connectionStringInfo = getConnectionStringInfo(command.connectionString);
        if (command.connectionStringInfo) {
            var options = {
                host: command.connectionStringInfo.host,
                port: command.connectionStringInfo.port,
                database: command.connectionStringInfo.database,
                user: command.connectionStringInfo.userId,
                password: command.connectionStringInfo.password,
                charset: command.connectionStringInfo.charset,
            };

            connect();
            var db;
        }
    }
    catch (e) {
        onError(e.stack);
    }
}
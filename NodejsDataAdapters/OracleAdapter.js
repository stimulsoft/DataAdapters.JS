/*
Stimulsoft.Reports.JS
Version: 2023.3.3
Build date: 2023.08.23
License: https://www.stimulsoft.com/en/licensing/reports
*/
exports.process = function (command, onResult) {
    var end = function (result) {
        result.adapterVersion = "2023.3.3";
        onResult(result);
    }

    var onError = function (message) {
        end({ success: false, notice: message });
    }

    try {
        var connect = function (error, connection) {
            if (error) onError(error.message);
            else onConnect(connection);
        }

        var onConnect = function (connection) {
            if (command.queryString) {
                if (command.command == "Execute")
                    command.queryString = "BEGIN " + command.queryString + "(" + command.parameters.map(parameter => "@" + parameter.name).join(", ") + "); END;";

                var { queryString, parameters } = applyQueryParameters(command.queryString, command.parameters, command.escapeQueryParameters);
                query(connection, queryString, parameters, command.maxDataRows);
            }
            else end({ success: true });
        }

        var query = function (connection, queryString, parameters, maxDataRows) {
            var args = [queryString];
            if (parameters) args.push(parameters);

            connection.execute(...args, function (error, result) {
                if (error) onError(error.message);
                else {
                    onQuery(result, maxDataRows);
                }
            });
        }

        var onQuery = function (result, maxDataRows) {
            var columns = [];
            var rows = [];
            var types = [];

            for (var column of result.metaData) {
                columns.push(column.name);

                switch (column.dbTypeName) {
                    case "BFILE":
                    case "BLOB":
                    case "LONGRAW":
                    case "RAW":
                        types.push("array"); break;

                    case "DATE":
                    case "TIMESTAMP":
                    case "TIMESTAMPWITHLOCALTIMEZONE":
                    case "TIMESTAMPWITHTIMEZONE":
                        types.push("datetime"); break;

                    case "INTERVALDAYTOSECOND":
                        types.push("time"); break;

                    case "INTERVALYEARTOMONTH":
                        types.push("int"); break;

                    case "NUMBER":
                    case "BINARY_DOUBLE":
                    case "BINARY_FLOAT":
                    case "BINARY_INTEGER":
                        types.push("number"); break;

                    default:
                        types.push("string"); break;
                }
            }

            for (var record of result.rows) {
                var row = [];

                for (var columnIndex in record) {
                    var value = record[columnIndex];
                    if (value instanceof Uint8Array) value = Buffer.from(result.rows[recordIndex][columnIndex]).toString('base64');
                    if (value instanceof Date) value = new Date(value.getTime() - (value.getTimezoneOffset() * 60000)).toISOString();;

                    row.push(value);
                }

                if (maxDataRows != null && maxDataRows <= rows.length) break;
                rows.push(row);
            }

            end({ success: true, columns: columns, rows: rows, types: types });
        }

        var getConnectionStringInfo = function (connectionString) {
            var info = { database: "", userId: "", password: "", charset: "AL32UTF8", privilege: "" };


            for (var propertyIndex in connectionString.split(";")) {
                var property = connectionString.split(";")[propertyIndex];
                if (property) {
                    var match = property.split("=");
                    if (match && match.length >= 2) {
                        match[0] = match[0].trim().toLowerCase();
                        match[1] = match[1].trim();

                        switch (match[0]) {
                            case "database":
                            case "data source":
                                info["database"] = match.splice(1, match.length).join("=");
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

                            case "dba privilege":
                            case "privilege":
                                var value = match[1].toLowerCase();
                                info["privilege"] = "OCI_DEFAULT";
                                if (value == "sysoper" || value == "oci_sysoper") info["privilege"] = "OCI_SYSOPER";
                                if (value == "sysdba" || value == "oci_sysdba") info["privilege"] = "OCI_SYSDBA";
                                break;
                        }
                    }
                }
            }

            return info;
        };

        var applyQueryParameters = function (baseSqlCommand, baseParameters, escapeQueryParameters) {
            var parameters = null;
            var result = "";

            if (baseSqlCommand != null && baseSqlCommand.indexOf(":") > -1) {
                while (baseSqlCommand.indexOf(":") >= 0 && baseParameters != null && baseParameters.length > 0) {
                    result += baseSqlCommand.substring(0, baseSqlCommand.indexOf(":"));
                    baseSqlCommand = baseSqlCommand.substring(baseSqlCommand.indexOf(":") + 1);

                    var parameterName = "";

                    while (baseSqlCommand.length > 0) {
                        var char = baseSqlCommand.charAt(0);
                        if (char.length === 1 && char.match(/[a-zA-Z0-9_-]/i)) {
                            parameterName += char;
                            baseSqlCommand = baseSqlCommand.substring(1);
                        }
                        else break;
                    }

                    var parameter = baseParameters.find(parameter => parameter.name.toLowerCase() == parameterName.toLowerCase());
                    if (parameter) {
                        if (parameter.index == null) {
                            var parameterValue = parameter.value;
                            if (parameter.typeGroup == "number") parameterValue = +parameter.value;
                            else if (parameter.typeGroup == "datetime") parameterValue = new Date(parameter.value);
                            else if (parameter.typeGroup == "date") parameterValue = new Date(parameter.value);
                            else if (parameter.typeGroup == "time") parameterValue = new Date(parameter.value);
                            if (parameters == null) parameters = {};
                            parameters[parameter.name] = parameterValue;
                        }
                    }
                    result += ':' + parameter.name;
                }
            }

            return { queryString: result + baseSqlCommand, parameters };
        }

        command.connectionStringInfo = getConnectionStringInfo(command.connectionString);
        var oracledb = require('oracledb');
        try {
            oracledb.initOracleClient();
        }
        catch (e) {
            var utils = require("oracledb/lib/thin/util.js");
            utils.CLIENT_INFO.program = utils.CLIENT_INFO.program.split("(").join("_").split(")").join("_");
        }

        var connection;

        oracledb.getConnection({
            user: command.connectionStringInfo.userId,
            password: command.connectionStringInfo.password,
            connectString: command.connectionStringInfo.database
        }, connect);

    }
    catch (e) {
        onError(e.stack);
    }
}
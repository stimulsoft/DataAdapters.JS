/*
Stimulsoft.Reports.JS
Version: 2025.1.6
Build date: 2025.02.28
License: https://www.stimulsoft.com/en/licensing/reports
*/
exports.process = function (command, onResult) {
    var end = function (result) {
        try {
            if (client) client.end();
            result.adapterVersion = "2025.1.6";
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
            client.connect(function (error) {
                if (error) onError(error.message);
                else onConnect();
            });
        }

        var query = function (queryString, parameters, maxDataRows) {
            client.query(queryString, parameters, function (error, recordset) {
                if (error) onError(error.message);
                else {
                    onQuery(recordset, maxDataRows);
                }
            });
        }

        var onConnect = function () {
            if (command.queryString) {
                if (command.command == "Execute")
                    command.queryString = "CALL " + command.queryString + "(" + command.parameters.map(parameter => "@" + parameter.name).join(", ") + ")";

                var { queryString, parameters } = applyQueryParameters(command.queryString, command.parameters, command.escapeQueryParameters);
                query(queryString, parameters, command.maxDataRows);
            }
            else end({ success: true });
        }

        var onQuery = function (recordset, maxDataRows) {
            var columns = [];
            var rows = [];
            var types = [];

            if (Array.isArray(recordset)) {
                for (var resultIndex in recordset) {
                    if (recordset[resultIndex].command == "SELECT") {
                        recordset = recordset[resultIndex];
                        break;
                    }
                }
            }

            for (var columnIndex in recordset.fields) {
                var column = recordset.fields[columnIndex]
                columns.push(column.name);

                switch (column.dataTypeID) {
                    case 16: // BOOL
                        types[columnIndex] = "boolean"; break;

                    case 20: // INT8
                    case 21: // INT2
                    case 23: // INT4
                        types[columnIndex] = "int"; break;

                    case 700: // FLOAT4
                    case 701: // FLOAT8
                    case 1700: // NUMERIC
                        types[columnIndex] = "number"; break;

                    case 702: // ABSTIME
                    case 1082: // DATE
                    case 1114: // TIMESTAMP
                        types[columnIndex] = "datetime"; break;

                    case 1184: // TIMESTAMPTZ
                        types[columnIndex] = "datetimeZ"; break;

                    case 1083: // TIME
                        types[columnIndex] = "time"; break;

                    case 1266: // TIMETZ
                        types[columnIndex] = "timeZ"; break;

                    case 17: // BYTEA
                    case 18: // CHAR
                    case 19:
                    case 24: // REGPROC
                    case 25: // TEXT
                    case 26: // OID
                    case 27: // TID
                    case 28: // XID
                    case 29: // CID
                    case 114: // JSON
                    case 142: // XML
                    case 194: // PG_NODE_TREE
                    case 210: // SMGR
                    case 602: // PATH
                    case 604: // POLYGON
                    case 650: // CIDR
                    case 703: // RELTIME
                    case 704: // TINTERVAL
                    case 718: // CIRCLE
                    case 774: // MACADDR8
                    case 790: // MONEY
                    case 829: // MACADDR
                    case 869: // INET
                    case 1033: // ACLITEM
                    case 1042: // BPCHAR
                    case 1043: // VARCHAR
                    case 1186: // INTERVAL
                    case 1560: // BIT
                    case 1562: // VARBIT
                    case 1790: // REFCURSOR
                    case 2202: // REGPROCEDURE
                    case 2203: // REGOPER
                    case 2204: // REGOPERATOR
                    case 2205: // REGCLASS
                    case 2206: // REGTYPE
                    case 2950: // UUID
                    case 2970: // TXID_SNAPSHOT
                    case 3220: // PG_LSN
                    case 3361: // PG_NDISTINCT
                    case 3402: // PG_DEPENDENCIES
                    case 3614: // TSVECTOR
                    case 3615: // TSQUERY
                    case 3642: // GTSVECTOR
                    case 3734: // REGCONFIG
                    case 3769: // REGDICTIONARY
                    case 3802: // JSONB
                    case 4089: // REGNAMESPACE
                    case 4096: // REGROLE
                    default:
                        types[columnIndex] = "string"; break;
                }
            }

            if (recordset.rows && recordset.rows.length > 0 && Array.isArray(recordset.rows[0])) recordset.rows = recordset.rows[0];

            for (var recordIndex in recordset.rows) {
                var row = [];
                for (var columnName in recordset.rows[recordIndex]) {
                    var columnIndex = columns.indexOf(columnName);
                    if (recordset.rows[recordIndex][columnName] instanceof Uint8Array) {
                        types[columnIndex] = "array";
                        recordset.rows[recordIndex][columnName] = Buffer.from(recordset.rows[recordIndex][columnName]).toString('base64');
                    }

                    if (recordset.rows[recordIndex][columnName] != null && typeof recordset.rows[recordIndex][columnName].toISOString === "function") {
                        if (types[columnIndex] == "datetimeZ") {
                            recordset.rows[recordIndex][columnName] = recordset.rows[recordIndex][columnName].toISOString();
                        }
                        else {
                            var dateTime = new Date(recordset.rows[recordIndex][columnName].getTime() - (recordset.rows[recordIndex][columnName].getTimezoneOffset() * 60000)).toISOString();
                            recordset.rows[recordIndex][columnName] = dateTime.replace("Z", "");
                            types[columnIndex] = "datetime";
                        }
                    }

                    if (recordset.rows[recordIndex][columnName] != null && types[columnIndex] == "timeZ") {
                        var time = recordset.rows[recordIndex][columnName];
                        var offset = time.substr(time.indexOf("+"));
                        if (offset.indexOf(":") == -1) offset += ":00";
                        time = time.substr(0, time.indexOf("+"));
                        if (time.indexOf(".") == -1) time += ".000"
                        recordset.rows[recordIndex][columnName] = "0001-01-01T" + time + offset;
                    }

                    row[columnIndex] = recordset.rows[recordIndex][columnName];
                }
                if (maxDataRows != null && maxDataRows <= rows.length) break;
                rows.push(row);
            }

            for (var typeIndex in types) {
                if (types[typeIndex] == "timeZ") types[typeIndex] = "datetimeoffset";
                if (types[typeIndex] == "datetimeZ") types[typeIndex] = "datetime";
            }

            end({ success: true, columns: columns, rows: rows, types: types });
        }

        var getConnectionStringInfo = function (connectionString) {
            var info = { port: 5432 };

            for (var propertyIndex in connectionString.split(";")) {
                var property = connectionString.split(";")[propertyIndex];
                if (property) {
                    var match = property.split(new RegExp('=|:'));
                    if (match && match.length >= 2) {
                        match[0] = match[0].trim().toLowerCase();
                        match[1] = match[1].trim();

                        switch (match[0]) {
                            case "data source":
                            case "server":
                            case "host":
                                info["host"] = match[1];
                                break;

                            case "port":
                                info["port"] = match[1];
                                break;

                            case "database":
                            case "location":
                                info["database"] = match[1];
                                break;

                            case "uid":
                            case "user":
                            case "user id":
                                info["user"] = match[1];
                                break;

                            case "pwd":
                            case "password":
                                info["password"] = match[1];
                                break;

                            case "ssl":
                                info["ssl"] = match[1];
                                break;
                            case "sslmode":
                                if (match[1] == "require") info["ssl"] = 1;
                                else if (match[1] == "disable") info["ssl"] = 0;
                                break;
                        }
                    }
                }
            }

            return info;
        };

        var applyQueryParameters = function (baseSqlCommand, baseParameters, escapeQueryParameters) {
            var parameters = [];
            var result = "";

            if (baseSqlCommand != null && baseSqlCommand.indexOf("@") > -1) {
                while (baseSqlCommand.indexOf("@") >= 0 && baseParameters != null && baseParameters.length > 0) {
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

                    var parameter = baseParameters.find(parameter => parameter.name.toLowerCase() == parameterName.toLowerCase());
                    if (parameter) {
                        if (parameter.index == null) {
                            if (parameter.typeGroup == "number") parameters.push(+parameter.value);
                            else if (parameter.typeGroup == "datetime") parameters.push(new Date(parameter.value));
                            else parameters.push(parameter.value);
                            parameter.index = parameters.length;
                        }
                        //result += '"' + parameter.name + '" := $' + parameter.index.toString();
                        result += '$' + parameter.index.toString();
                    }
                    else
                        result += "@" + parameterName;
                }
            }

            return { queryString: result + baseSqlCommand, parameters };
        }

        var pg = require('pg');
        if (command.connectionString.startsWith("postgres://")) {
            var parse = require('pg-connection-string').parse;
            command.connectionStringInfo = parse(command.connectionString);
        }
        else {
            command.connectionStringInfo = getConnectionStringInfo(command.connectionString);
        }

        var client = new pg.Client(command.connectionStringInfo);

        connect();
    }
    catch (e) {
        onError(e.stack);
    }
}

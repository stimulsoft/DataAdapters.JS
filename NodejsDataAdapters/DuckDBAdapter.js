/*
Stimulsoft.Reports.JS
Version: 2026.3.1
Build date: 2026.07.16
License: https://www.stimulsoft.com/en/licensing/reports
*/
exports.process = function (command, onResult) {
    var connection;

    var end = function (result) {
        try {
            if (connection) connection.closeSync();
        }
        catch (e) {
        }

        result.adapterVersion = "2026.3.1";
        onResult(result);
    };

    var onError = function (error) {
        var message = error && (error.stack || error.message) ? (error.stack || error.message) : String(error);
        end({ success: false, notice: message });
    };

    var parseConnectionString = function (connectionString) {
        var info = { path: "", accessMode: null };
        var properties = [];
        var property = "";
        var quote = null;

        for (var index = 0; index < connectionString.length; index++) {
            var char = connectionString[index];

            if (quote != null) {
                property += char;
                if (char == quote) {
                    if (index + 1 < connectionString.length && connectionString[index + 1] == quote) {
                        property += connectionString[++index];
                    }
                    else quote = null;
                }
            }
            else if (char == '"' || char == "'") {
                quote = char;
                property += char;
            }
            else if (char == ";") {
                properties.push(property);
                property = "";
            }
            else property += char;
        }

        properties.push(property);

        var unquote = function (value) {
            value = value.trim();
            if (value.length >= 2 && (value[0] == '"' || value[0] == "'") && value[value.length - 1] == value[0]) {
                var currentQuote = value[0];
                value = value.substring(1, value.length - 1);
                value = value.split(currentQuote + currentQuote).join(currentQuote);
            }
            return value;
        };

        for (var propertyIndex = 0; propertyIndex < properties.length; propertyIndex++) {
            var item = properties[propertyIndex];
            var separatorIndex = item.indexOf("=");
            if (separatorIndex < 0) continue;

            var key = item.substring(0, separatorIndex).trim().toLowerCase().replace(/[ _-]/g, "");
            var value = unquote(item.substring(separatorIndex + 1));

            if (key == "datasource" || key == "database" || key == "filename") info.path = value;
            else if (key == "accessmode") info.accessMode = value;
        }

        if (!info.path) throw new Error("DuckDB database file path is empty.");
        return info;
    };

    var normalizeParameter = function (parameter) {
        var typeName = String(parameter.typeName || "").toLowerCase();
        var value = parameter.value;

        if (value == null) return null;

        if (typeName == "boolean") {
            return typeof value == "boolean" ? value : String(value).toLowerCase() == "true";
        }

        if (typeName == "tinyint" || typeName == "smallint" || typeName == "integer" ||
            typeName == "utinyint" || typeName == "usmallint" || typeName == "uinteger" ||
            typeName == "float" || typeName == "double" || typeName == "decimal" || parameter.typeGroup == "number") {
            return Number(value);
        }

        if (typeName == "bigint" || typeName == "hugeint" || typeName == "ubigint") {
            try {
                return BigInt(value);
            }
            catch (e) {
                return Number(value);
            }
        }

        if (typeName == "date" || typeName == "timestamp" || parameter.typeGroup == "datetime") {
            var date = value instanceof Date ? value : new Date(value);
            return isNaN(date.getTime()) ? value : date;
        }

        if (typeName == "blob") {
            if (Buffer.isBuffer(value)) return value;
            if (value instanceof Uint8Array || Array.isArray(value)) return Buffer.from(value);
            if (typeof value == "string") return Buffer.from(value, "base64");
        }

        return value;
    };

    var applyQueryParameters = function (queryString, baseParameters) {
        var parameters = [];
        var parameterIndexes = {};

        queryString = queryString.replace(/@([a-zA-Z0-9_-]+)/g, function (match, parameterName) {
            var parameter = (baseParameters || []).find(function (item) {
                return String(item.name).replace(/^@/, "").toLowerCase() == parameterName.toLowerCase();
            });

            if (!parameter) return match;

            var key = parameterName.toLowerCase();
            if (parameterIndexes[key] == null) {
                parameters.push(normalizeParameter(parameter));
                parameterIndexes[key] = parameters.length;
            }

            return "$" + parameterIndexes[key];
        });

        return { queryString: queryString, parameters: parameters };
    };

    var getResultType = function (typeId, DuckDBTypeId) {
        switch (typeId) {
            case DuckDBTypeId.BOOLEAN:
                return "boolean";

            case DuckDBTypeId.TINYINT:
            case DuckDBTypeId.SMALLINT:
            case DuckDBTypeId.INTEGER:
            case DuckDBTypeId.BIGINT:
            case DuckDBTypeId.UTINYINT:
            case DuckDBTypeId.USMALLINT:
            case DuckDBTypeId.UINTEGER:
            case DuckDBTypeId.UBIGINT:
            case DuckDBTypeId.HUGEINT:
            case DuckDBTypeId.UHUGEINT:
                return "int";

            case DuckDBTypeId.FLOAT:
            case DuckDBTypeId.DOUBLE:
            case DuckDBTypeId.DECIMAL:
            case DuckDBTypeId.BIGNUM:
                return "number";

            case DuckDBTypeId.TIMESTAMP:
            case DuckDBTypeId.DATE:
            case DuckDBTypeId.TIMESTAMP_S:
            case DuckDBTypeId.TIMESTAMP_MS:
            case DuckDBTypeId.TIMESTAMP_NS:
            case DuckDBTypeId.TIMESTAMP_TZ:
                return "datetime";

            case DuckDBTypeId.TIME_TZ:
                return "datetimeoffset";

            case DuckDBTypeId.TIME:
            case DuckDBTypeId.TIME_NS:
                return "time";

            case DuckDBTypeId.BLOB:
            case DuckDBTypeId.BIT:
            case DuckDBTypeId.GEOMETRY:
                return "array";

            default:
                return "string";
        }
    };

    var formatTime = function (micros) {
        micros = BigInt(micros);
        var microsPerDay = 86400000000n;
        micros = ((micros % microsPerDay) + microsPerDay) % microsPerDay;

        var hours = micros / 3600000000n;
        micros %= 3600000000n;
        var minutes = micros / 60000000n;
        micros %= 60000000n;
        var seconds = micros / 1000000n;
        var fraction = String(micros % 1000000n).padStart(6, "0");

        return String(hours).padStart(2, "0") + ":" +
            String(minutes).padStart(2, "0") + ":" +
            String(seconds).padStart(2, "0") + "." + fraction;
    };

    var formatOffset = function (offsetSeconds) {
        var sign = offsetSeconds < 0 ? "-" : "+";
        var seconds = Math.abs(offsetSeconds);
        var hours = Math.floor(seconds / 3600);
        var minutes = Math.floor((seconds % 3600) / 60);
        return sign + String(hours).padStart(2, "0") + ":" + String(minutes).padStart(2, "0");
    };

    var jsonStringify = function (value) {
        return JSON.stringify(value, function (key, item) {
            return typeof item == "bigint" ? item.toString() : item;
        });
    };

    var convertValue = function (value, typeId, DuckDBTypeId) {
        if (value == null) return null;

        if (typeId == DuckDBTypeId.BLOB || typeId == DuckDBTypeId.BIT || typeId == DuckDBTypeId.GEOMETRY) {
            return Buffer.from(value).toString("base64");
        }

        if (typeId == DuckDBTypeId.TIME || typeId == DuckDBTypeId.TIME_NS) {
            return formatTime(value);
        }

        if (typeId == DuckDBTypeId.TIME_TZ && value && value.micros != null) {
            return "0001-01-01T" + formatTime(value.micros) + formatOffset(value.offset || 0);
        }

        if (value instanceof Date) {
            var dateTime = value.toISOString();
            return typeId == DuckDBTypeId.TIMESTAMP_TZ ? dateTime : dateTime.replace("Z", "");
        }

        if (typeof value == "bigint") return value.toString();
        if (typeof value == "object") return jsonStringify(value);

        return value;
    };

    var onQuery = function (reader, maxDataRows, DuckDBTypeId) {
        var columns = reader.columnNames();
        var columnTypeIds = columns.map(function (column, columnIndex) {
            return reader.columnTypeId(columnIndex);
        });
        var types = columnTypeIds.map(function (typeId) {
            return getResultType(typeId, DuckDBTypeId);
        });
        var sourceRows = reader.getRowsJS();
        var rows = [];

        for (var rowIndex = 0; rowIndex < sourceRows.length; rowIndex++) {
            if (maxDataRows != null && rows.length >= maxDataRows) break;

            var row = [];
            for (var columnIndex = 0; columnIndex < columns.length; columnIndex++) {
                row[columnIndex] = convertValue(sourceRows[rowIndex][columnIndex], columnTypeIds[columnIndex], DuckDBTypeId);
            }
            rows.push(row);
        }

        end({ success: true, columns: columns, rows: rows, types: types });
    };

    var run = async function () {
        var duckdb = require("@duckdb/node-api");
        var connectionInfo = parseConnectionString(command.connectionString || "");
        var options = {};

        if (connectionInfo.accessMode) options.access_mode = connectionInfo.accessMode;

        var instance = await duckdb.DuckDBInstance.fromCache(connectionInfo.path, options);
        connection = await instance.connect();

        if (!command.queryString) {
            end({ success: true });
            return;
        }

        var query = applyQueryParameters(command.queryString, command.parameters);
        var reader;

        if (command.maxDataRows != null) {
            reader = await connection.streamAndReadUntil(query.queryString, Math.max(1, command.maxDataRows), query.parameters);
        }
        else {
            reader = await connection.runAndReadAll(query.queryString, query.parameters);
        }

        onQuery(reader, command.maxDataRows, duckdb.DuckDBTypeId);
    };

    run().catch(onError);
};

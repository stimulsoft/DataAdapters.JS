/*
Stimulsoft.Reports.JS
Version: 2025.1.6
Build date: 2025.02.28
License: https://www.stimulsoft.com/en/licensing/reports
*/
exports.process = function (command, onResult) {
    var getSchema = async function (collection) {
        return (await collection.aggregate(
            [
                { '$project': { 'data': { '$objectToArray': '$$ROOT' } } },
                { '$unwind': '$data' },
                {
                    '$group': {
                        '_id': null,
                        'data': { '$addToSet': { 'k': '$data.k', 'v': { '$type': '$data.v' } } }
                    }
                },
                { '$replaceRoot': { 'newRoot': { '$arrayToObject': '$data' } } }
            ]).toArray())[0];
    }

    var getType = function (type) {
        switch (type) {
            case "bool":
                return "boolean";

            case "int":
            case "long":
            case "minKey":
            case "maxKey":
                return "int";

            case "double":
            case "decimal":
                return "number";

            case "date":
            case "timestamp":
                return "datetime";

            case "string":
            case "objectId":
            case "regex":
            case "javascript":
            case "array":
            case "object":
                return "string";

            case "binData":
            case "null":
                return "array";
        }

        return "string";
    }

    setTimeout(async () => {
        var result = { success: false };

        try {
            var { MongoClient } = require("mongodb");
            var uri = command.connectionString;
            var client = new MongoClient(uri);

            await client.connect();
            var db = client.db(client.options.dbName);

            if (command.command == "TestConnection") {
                result = { success: true };
            }
            else if (command.command == "RetrieveSchema") {
                var collections = await db.listCollections().toArray();
                var rows = [];

                for (var collection of collections) {
                    if (command.dataSource && command.dataSource != collection.name)
                        continue;

                    collection = db.collection(collection.name);

                    var schema = await getSchema(collection);
                    for (var name in schema) {
                        rows.push([collection.collectionName, name, getType(schema[name])]);
                    }
                }

                result = { success: true, rows };
            }
            if (command.command == "ExecuteQuery") {
                var rows = [];
                var columns = [];
                var types = [];
                collection = db.collection(command.dataSource);
                var schema = await getSchema(collection);

                for (var name in schema) {
                    columns.push(name);
                    types.push(getType(schema[name]));
                }

                var query = command.queryString ? JSON.parse(command.queryString.replace(/(['"])?([a-z0-9A-Z_]+)(['"])?:/g, '"$2": ')) : {};

                var records = await collection.find(query).toArray();
                for (var record of records) {
                    var row = [];
                    for (var columnName in record) {
                        var columnIndex = columns.indexOf(columnName);
                        var value = record[columnName];

                        value = JSON.stringify(value);
                        if (value.charAt(0) === '"' && value.charAt(value.length - 1) === '"')
                            value = value.substr(1, value.length - 2)

                        row[columnIndex] = value;
                    }

                    if (command.maxDataRows != null && command.maxDataRows <= rows.length) break;
                    rows.push(row);
                }

                result = { success: true, rows, columns, types };
            }
        }
        catch (e) {
            result = { success: false, notice: e.message };
        }

        client.close();
        result.adapterVersion = "2025.1.6";
        onResult(result);
    });
}
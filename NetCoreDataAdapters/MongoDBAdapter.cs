/*
Stimulsoft.Reports.JS
Version: 2025.1.2
Build date: 2024.12.19
License: https://www.stimulsoft.com/en/licensing/reports
*/
﻿/*
Stimulsoft.Reports.JS
Version: 2023.3.3
Build date: 2023.08.23
License: https://www.stimulsoft.com/en/licensing/reports
*/
using MongoDB.Bson;
using MongoDB.Bson.Serialization;
using MongoDB.Driver;
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;

namespace NetCoreDataAdapters
{
    public class MongoDbAdapter
    {
        private static BsonDocument GetSchema(IMongoCollection<BsonDocument> collection)
        {
            var aggregate = collection
                        .Aggregate()
                        .Project(new BsonDocument { { "_id", 0 }, { "data", new BsonDocument("$objectToArray", "$$ROOT") } })
                        .Unwind("data")
                        .Group(new BsonDocument { { "_id", BsonNull.Value }, { "data", new BsonDocument("$addToSet", new BsonDocument { { "k", "$data.k" }, { "v", new BsonDocument("$type", "$data.v") } }) } })
                        .ReplaceRoot<BsonDocument>(new BsonDocument("newRoot", new BsonDocument("$arrayToObject", "$data"))).ToList();


            return aggregate.First().Values.First().ToBsonDocument();
        }

        private static string GetType(String type)
        {
            switch (type)
            {
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

        public static Result Process(CommandJson command)
        {
            var result = new Result();

            try
            {
                var settings = MongoClientSettings.FromConnectionString(command.ConnectionString);
                settings.ConnectTimeout = new TimeSpan(0, 0, command.Timeout / 2000);
                settings.MaxConnectionLifeTime = settings.ConnectTimeout;
                settings.ServerSelectionTimeout = settings.ConnectTimeout;

                var client = new MongoClient(settings);
                var builderUrl = new MongoUrlBuilder(command.ConnectionString);
                var database = client.GetDatabase(builderUrl.DatabaseName);

                if (command.Command == "TestConnection")
                {
                    var collection = database.ListCollectionNames();
                    result = new Result() { Success = true };
                }
                else if (command.Command == "RetrieveSchema")
                {
                    var collections = database.ListCollectionNames().ToEnumerable();
                    var rows = new List<string[]>();

                    foreach (var collectionName in collections)
                    {
                        if (!string.IsNullOrEmpty(command.DataSource) && command.DataSource == collectionName)
                            continue;

                        var collection = database.GetCollection<BsonDocument>(collectionName);
                        var schemaBson = GetSchema(collection);

                        var results = schemaBson.ToList();
                        foreach (var field in results)
                        {
                            rows.Add(new string[] { collectionName, field.Name, GetType(field.Value.ToString()) });
                        }
                    }

                    result = new Result()
                    {
                        Success = true,
                        Rows = rows.ToArray()
                    };
                }
                if (command.Command == "ExecuteQuery")
                {
                    var columns = new List<string>();
                    var rows = new List<string[]>();
                    var types = new List<string>();

                    var collection = database.GetCollection<BsonDocument>(command.DataSource);
                    var schemaBson = GetSchema(collection);

                    foreach (var field in schemaBson.ToList())
                    {
                        columns.Add(field.Name);
                        types.Add(GetType(field.Value.ToString()));
                    }

                    var query = string.IsNullOrEmpty(command.QueryString) ? FilterDefinition<BsonDocument>.Empty : BsonSerializer.Deserialize<BsonDocument>(command.QueryString);

                    CultureInfo.CurrentCulture = CultureInfo.InvariantCulture;
                    foreach (var record in collection.Find(query).ToEnumerable())
                    {
                        var row = new string[columns.Count];
                        foreach (var field in record)
                        {
                            var columnIndex = columns.IndexOf(field.Name);
                            var value = field.Value;
                            
                            if (field.Value.BsonType == BsonType.DateTime)
                                value = ((DateTime)value).ToString("yyyy-MM-dd'T'HH:mm:ss.fffZ");

                            row[columnIndex] = value.ToString();
                        }

                        if (command.MaxDataRows <= rows.Count) break;
                        rows.Add(row);
                    }

                    result = new Result()
                    {
                        Success = true,
                        Rows = rows.ToArray(),
                        Columns = columns.ToArray(),
                        Types = types.ToArray()
                    };
                }
            }
            catch (Exception ex)
            {
                result = new Result()
                {
                    Success = false,
                    Notice = ex.Message
                };
            }

            result.AdapterVersion = "2025.1.2";
            return result;
        }
    }
}
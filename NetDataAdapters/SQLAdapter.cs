/*
Stimulsoft.Reports.JS
Version: 2025.1.4
Build date: 2025.01.24
License: https://www.stimulsoft.com/en/licensing/reports
*/
using FirebirdSql.Data.FirebirdClient;
using MySql.Data.MySqlClient;
using Npgsql;
using System;
using System.Collections.Generic;
using System.Data;
using System.Data.Common;
using System.Data.OracleClient;
using System.Data.SqlClient;
using System.IO;

namespace AspNetDataAdapters
{
    public class SQLAdapter
    {
        private static DbConnection connection;
        private static DbDataReader reader;
        private static CommandJson command;

        private static Result End(Result result)
        {
            result.AdapterVersion = "2025.1.4";
            try
            {
                if (reader != null) reader.Close();
                if (connection != null) connection.Close();

                return result;
            }
            catch (Exception e)
            {
                return result;
            }
        }

        private static Result OnError(string message)
        {
            return End(new Result { Success = false, Notice = message });
        }

        private static Result Connect()
        {
            try
            {
                connection.Open();
                return OnConnect();
            }
            catch (Exception e)
            {
                return OnError(e.Message);
            }
        }

        private static Result OnConnect()
        {
            if (!String.IsNullOrEmpty(command.QueryString)) return Query();
            else return End(new Result { Success = true });
        }

        private static Result Query()
        {
            try
            {
                var sqlCommand = connection.CreateCommand();
                sqlCommand.CommandType = command.Command == "Execute" ? CommandType.StoredProcedure : CommandType.Text;
                sqlCommand.CommandText = command.QueryString;
                sqlCommand.CommandTimeout = command.Timeout / 1000;

                foreach (var parameter in command.Parameters)
                {
                    var sqlParameter = sqlCommand.CreateParameter();
                    sqlParameter.ParameterName = parameter.Name;
                    sqlParameter.DbType = GetDbType(parameter.TypeName);
                    sqlParameter.Size = parameter.Size;
                    sqlParameter.Value = parameter.Value;
                    if (sqlParameter.DbType == DbType.Decimal) sqlParameter.Precision = (byte)parameter.Size;
                    sqlParameter.Value = GetValue(parameter.Value, parameter.TypeGroup);
                    sqlCommand.Parameters.Add(sqlParameter);
                }
                
                reader = sqlCommand.ExecuteReader();
                return OnQuery();
            }
            catch (Exception e)
            {
                return OnError(e.Message);
            }
        }

        private static Result OnQuery()
        {
            var columns = new List<string>();
            var rows = new List<string[]>();
            var types = new List<string>();

            for (var index = 0; index < reader.FieldCount; index++)
            {
                var columnName = reader.GetName(index);
                var columnType = GetType(reader.GetDataTypeName(index));
                if (columnType == "string" && reader.GetFieldType(index).Equals(typeof(byte[])))
                    columnType = "array";

                columns.Add(columnName);
                types.Add(columnType);
            }

            while (reader.Read())
            {
                var row = new string[reader.FieldCount];
                for (var index = 0; index < reader.FieldCount; index++)
                {
                    object value = null;
                    try
                    {
                        if (!reader.IsDBNull(index))
                        {
                            value = reader.GetValue(index);
                        }
                    }
                    catch 
                    { 
                        value = null;
                    }

                    if (value == null) value = "";
                    if (value is DateTime)
                    {
                        row[index] = ((DateTime)value).ToString("yyyy-MM-dd'T'HH:mm:ss.fff");
                        types[index] = "datetime";
                    }
                    else if (value is DateTimeOffset)
                    {
                        row[index] = ((DateTimeOffset)value).ToString("yyyy-MM-dd'T'HH:mm:ss.fffK");
                        types[index] = "datetimeoffset";
                    }
                    else if (value is TimeSpan)
                    {
                        row[index] = Math.Truncate(((TimeSpan)value).TotalHours) + ":" + ((TimeSpan)value).Minutes + ":" + ((TimeSpan)value).Seconds;
                        types[index] = "time";
                    }
                    else
                    {
                        if (types[index] == "array")
                            value = GetBytes(index);

                        row[index] = value.ToString();
                    }
                }

                if (command.MaxDataRows <= rows.Count) break;
                rows.Add(row);
            }

            return End(new Result { Success = true, Columns = columns.ToArray(), Rows = rows.ToArray(), Types = types.ToArray() });
        }

        private static string GetBytes(int index)
        {
            if (reader.GetFieldValue<object>(index) == DBNull.Value) return "";

            var size = reader.GetBytes(index, 0, null, 0, 0);
            if (size == 0) return "";

            var destination = new MemoryStream();
            var buffer = new byte[8040];
            long offset = 0;
            long read;

            while ((read = reader.GetBytes(index, offset, buffer, 0, buffer.Length)) > 0)
            {
                offset += read;
                destination.Write(buffer, 0, (int)read);
                if (size == offset) break;
            }

            return System.Convert.ToBase64String(destination.ToArray());
        }

        private static string GetType(string dbType)
        {
            if (connection is MySqlConnection)
            {
                switch (dbType.ToLowerInvariant())
                {
                    case "uniqueidentifier":
                        return "string";

                    case "bigint":
                    case "int64":
                    case "year":
                    case "int32":
                    case "int24":
                    case "int":
                    case "int16":
                    case "smallint":
                    case "byte":
                    case "ubyte":
                    case "uint32":
                    case "uint24":
                    case "uint16":
                    case "tinyint":
                    case "uint64":
                    case "decimal":
                    case "newdecimal":
                    case "money":
                    case "smallmoney":
                    case "float":
                    case "real":
                    case "double":
                        return "number";

                    case "bit":
                        return "boolean";

                    case "newdatetime":
                    case "smalldatetime":
                    case "datetime":
                    case "date":
                    case "timestamp":
                        return "datetime";

                    case "time":
                        return "time";

                    case "blob":
                        return "array";
                }
            }
            else if (connection is FbConnection)
            {
                switch (dbType.ToLowerInvariant())
                {
                    case "uniqueidentifier":
                        return "string";

                    case "bigint":
                    case "numeric":
                    case "int":
                    case "integer":
                    case "smallint":
                        return "int";

                    case "decimal":
                    case "money":
                    case "smallmoney":
                    case "float":
                    case "real":
                    case "double":
                        return "number";

                    case "datetime":
                    case "date":
                    case "smalldatetime":
                    case "timestamp":
                        return "datetime";

                    case "time":
                        return "time";

                    case "boolean":
                        return "boolean";

                }
            }
            else if (connection is SqlConnection)
            {
                switch (dbType.ToLowerInvariant())
                {
                    case "uniqueidentifier":
                        return "string";

                    case "bigint":
                    case "timestamp":
                    case "int":
                    case "smallint":
                    case "tinyint":
                        return "int";

                    case "decimal":
                    case "money":
                    case "smallmoney":
                    case "float":
                    case "real":
                        return "number";

                    case "datetime":
                    case "date":
                    case "datetime2":
                    case "smalldatetime":
                        return "datetime";

                    case "time":
                        return "time";

                    case "datetimeoffset":
                        return "datetimeoffset";

                    case "bit":
                        return "boolean";

                    case "binary":
                    case "image":
                        return "array";
                }
            }
            else if (connection is NpgsqlConnection)
            {
                switch (dbType.ToLowerInvariant())
                {
                    case "uniqueidentifier":
                        return "string";

                    case "bigint":
                    case "int":
                    case "int4":
                    case "int8":
                    case "integer":
                    case "numeric":
                    case "smallint":
                    case "tinyint":
                        return "int";

                    case "decimal":
                    case "money":
                    case "smallmoney":
                    case "float":
                    case "real":
                    case "double":
                        return "number";

                    case "abstime":
                    case "date":
                    case "datetime":
                    case "smalldatetime":
                    case "timestamp":
                    case "timestamptz":
                        return "dateTime";

                    case "time":
                        return "time";

                    case "timetz":
                        return "datetime";

                    case "boolean":
                        return "boolean";
                }
            }
            else if (connection is OracleConnection)
            {
                switch (dbType.ToUpperInvariant())
                {
                    case "BFILE":
                    case "BLOB":
                    case "LONGRAW":
                    case "RAW":
                        return "array";

                    case "DATE":
                    case "TIMESTAMP":
                    case "TIMESTAMPWITHLOCALTIMEZONE":
                    case "TIMESTAMPWITHTIMEZONE":
                        return "datetime";

                    case "INTERVALDAYTOSECOND":
                        return "time";

                    case "INTERVALYEARTOMONTH":
                        return "int";

                    case "NUMBER":
                    case "BINARY_DOUBLE":
                    case "BINARY_FLOAT":
                    case "BINARY_INTEGER":
                        return "number";
                }
            }

            return "string";
        }

        private static object GetValue(object obj, string type)
        {
            try
            {
                switch (type)
                {
                    case "string": return obj.ToString();
                    case "number": return Decimal.Parse(obj.ToString());
                    case "datetime": return DateTime.Parse(obj.ToString());
                }
            }
            catch
            { 
            }
            return obj;
        }

		private static DbType GetDbType(string typeName)
        {
			if (connection is MySqlConnection)
			{
			}
			else if (connection is FbConnection)
			{
			}
			else if (connection is SqlConnection)
			{
				switch (typeName.ToLowerInvariant())
				{
					case "bit": return DbType.Boolean;
					case "float": return DbType.Double;
					case "tinyint": return DbType.Byte;
					case "smallint": return DbType.Int16;
					case "int": return DbType.Int32;
					case "bigint": return DbType.Int64;
					case "money": return DbType.Decimal;
					case "real": return DbType.Single;

					case "nchar": return DbType.String;
					case "ntext": return DbType.String;
					case "nvarchar": return DbType.String;
					case "text": return DbType.String;
					case "varchar": return DbType.String;
					case "char": return DbType.StringFixedLength;

					case "uniqueidentifier": return DbType.Guid;
					case "smalldatetime": return DbType.DateTime;
					case "smallmoney": return DbType.Decimal;
				}
			}
			else if (connection is NpgsqlConnection)
			{
			}
			else if (connection is OracleConnection)
			{
			}

            DbType type;
            if (Enum.TryParse(typeName, true, out type))
                return type;
                
            return DbType.Object;
        }

	    public static Result Process(CommandJson command, DbConnection connection)
        {
            SQLAdapter.connection = connection;
            SQLAdapter.command = command;
            return Connect();
        }
    }
}
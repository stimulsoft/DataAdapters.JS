"""
Stimulsoft.Reports.JS
Version: 2024.1.1
Build date: 2023.12.08
License: https://www.stimulsoft.com/en/licensing/reports
"""

from urllib.parse import urlparse

from .classes.StiDataResult import StiDataResult
from .StiDataAdapter import StiDataAdapter


class StiMongoDbAdapter(StiDataAdapter):
    version: str = '2024.1.1'
    checkVersion: bool = True

    def connect(self):
        try:
            from pymongo import MongoClient
            self.connectionLink = MongoClient(self.connectionString)
        except Exception as e:
            return StiDataResult.getError(self, str(e))
        
        return StiDataResult.getSuccess(self)
    
    def process(self):
        if not super().process():
            return False
        
        url = urlparse(self.connectionString)
        self.connectionInfo.host = url.hostname
        self.connectionInfo.port = url.port
        self.connectionInfo.userId = url.username
        self.connectionInfo.password = url.password
        self.connectionInfo.database = url.path.strip(' /')

        parameterNames = []
        return self.parseParameters(parameterNames)
    
    def parseParameters(self, parameterNames: dict[str, list[str]]):
        return True
    
    def parseType(self, meta: object):
        types = {
            'boolean': ['bool'],
            'int': ['int', 'long', 'minKey', 'maxKey'],
            'number': ['double', 'decimal'],
            'datetime': ['date', 'timestamp'],
            'array': ['binData', 'null'],
            'string': ['string', 'objectId', 'regex', 'javascript', 'array', 'object']
        }

        type = str(meta)
        for key, array in types.items():
            if type in array:
                return key

        return 'string'
    
    def getValue(self, value: object, valueType: str):
        if value is None:
            return None

        if valueType == 'string':
            return value if type(value) == str else str(value)

        return super().getValue(value, valueType)
    
    def executeNative(self, queryString: str, result: StiDataResult):
        if not queryString:
            return self.retrieveSchema(result)

        return self.retrieveData(result, queryString)
    
    def retrieveSchema(self, result: StiDataResult):
        from pymongo import MongoClient
        connectionLink: MongoClient = self.connectionLink

        database = connectionLink.get_database(self.connectionInfo.database)
        collectionNames = database.list_collection_names()

        schema: dict[str, dict] = {}
        for name in collectionNames:
            pipeline = [
                {'$project': {'_id': 0}},
                {'$project': {'data': {'$objectToArray': '$$ROOT'}}},
                {'$unwind': '$data'},
                {'$group': {
                    '_id': None,
                    'data': {'$addToSet': {'k': '$data.k', 'v': {'$type': '$data.v'}}}}
                },
                {'$replaceRoot': {'newRoot': {'$arrayToObject': '$data'}}}
            ]
            collection = database.get_collection(name)
            cursor = collection.aggregate(pipeline)
            for document in cursor:
                schema[name] = document
                break

        result.count = len(schema)
        for tableName, table in schema.items():
            for columnName, columnType in table.items():
                row = []
                row.append(tableName)
                row.append(columnName)
                row.append(self.parseType(columnType))
                result.rows.append(row)

        return result

    def retrieveData(self, result: StiDataResult, queryString: str):
        from pymongo import MongoClient
        connectionLink: MongoClient = self.connectionLink

        result = self.retrieveSchema(result)
        for item in result.rows:
            if item[0] == queryString:
                result.columns.append(item[1])
                result.types.append(item[2])

        result.count = len(result.columns)
        result.rows = []

        database = connectionLink.get_database(self.connectionInfo.database)
        collection = database.get_collection(queryString)
        cursor = collection.find()
        for document in cursor:
            row = [None] * result.count
            for key, value in document.items():
                try:
                    index = result.columns.index(key)
                    valueType = self.getValueType(value, index, result.types)
                    row[index] = self.getValue(value, valueType)
                except ValueError:
                    pass
            result.rows.append(row)
        cursor.close()

        result.count = len(result.rows)
        return result
import os
import json

from boto3 import client, resource
from boto3.dynamodb.conditions import Key, Attr

class NoItemException(Exception):
    pass

class DynamoDBTableHelper:
    def __init__(self, aws_region: str, table_name: str):
        self._resource = resource('dynamodb', region_name=aws_region)
        self._table = self._resource.Table(table_name)
    
    def get_item(self, key: dict):
        item = self._table.get_item(
                Key=key)

        if 'Item' in item:
            return item['Item']
        else:
            raise NoItemException

    def put_item(self, item: dict):
        self._table.put_item(
            Item=item
        )

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.query
    def query(self, partition_key_name: str, partition_key_value):
        return self._table.query(
            KeyConditionExpression=Key(partition_key_name).eq(partition_key_value)
        )

        return items

class DynamoDBHelper:
    def __init__(self, aws_region):
        self._client = client('dynamodb', region_name=aws_region)

    def list_tables(self):
        tables = self._client.list_tables()
        return tables['TableNames']
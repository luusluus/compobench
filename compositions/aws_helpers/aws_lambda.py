import os
import json
from boto3 import client as boto3_client

class LambdaHelper:
    def __init__(self, aws_region):
        self._client = boto3_client('lambda', region_name=aws_region)

    def invoke_lambda_async(self, function_name, payload):
        # print(f'Asynchronously invoking {function_name}')
        return self._client.invoke(
            FunctionName=function_name,
            InvocationType='Event',
            Payload=json.dumps(payload))

    def invoke_lambda(self, function_name, payload):
        # print(f'Synchronously invoking {function_name}')
        response = self._client.invoke(
            FunctionName=function_name,
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
        )
        return json.load(response['Payload'])

import os
import json

from boto3 import client as boto3_client
from botocore.config import Config

def compose(function_name, data):
    aws_region = os.environ['AWS_REGION']

    client = boto3_client('lambda', region_name=aws_region)

    print(f'asynchronously invoking {function_name}')
    
    response = client.invoke(
        FunctionName=function_name,
        InvocationType='Event',
        Payload=json.dumps(data))

    return {
        'statusCode': response['StatusCode'],
        'headers': {'Content-Type': 'application/json'}
    }

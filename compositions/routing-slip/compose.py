import os
import json

from boto3 import client as boto3_client
from botocore.config import Config

def compose(event):

    if isinstance(event['composition'], list) and len(event['composition']) > 0:
        function = event['composition'].pop(0)

        aws_region = os.environ['AWS_REGION']

        client = boto3_client('lambda', region_name=aws_region)

        print(f'asynchronously invoking {function}')
        
        response = client.invoke(
            FunctionName=function,
            InvocationType='Event',
            Payload=json.dumps(event))

        return {
            'statusCode': response['StatusCode'],
            'headers': {'Content-Type': 'application/json'}
        }
    else:
        return event

import os
import json

from boto3 import client as boto3_client
from botocore.config import Config

def compose(function_name, data):
    aws_region = os.environ['AWS_REGION']

    client = boto3_client('lambda', region_name=aws_region)

    print(f'Asynchronously invoking {function_name}')
    
    client.invoke(
        FunctionName=function_name,
        InvocationType='Event',
        Payload=json.dumps(data))

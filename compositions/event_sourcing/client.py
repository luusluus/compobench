import uuid
import json
from time import sleep

from boto3 import client as boto3_client

def invoke(sleep: int, input: str):
    aws_region = 'eu-central-1'

    # invoke controller once to start workflow
    payload = {
        'input': input,
        'sleep': sleep
    }
    client = boto3_client('lambda', region_name=aws_region)
    response = client.invoke(
        FunctionName='EventSourcingOrchestrator',
        InvocationType='RequestResponse',
        Payload=json.dumps(payload)
    )

    return response['StatusCode']

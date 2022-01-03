import sys
import json
import logging
from boto3 import client as boto3_client

def invoke(sleep: int):
    aws_region = 'eu-central-1'
    client = boto3_client('lambda', region_name=aws_region)

    # call the first function a to start the workflow
    event = {
        'sleep': sleep
    }
    response = client.invoke(
        FunctionName='SequenceFunctionA',
        InvocationType='RequestResponse',
        Payload=json.dumps(event)
    )

    logging.info(response)

    return response['StatusCode']

if __name__ == "__main__":
    sleep = sys.argv[1]
    status_code = invoke(sleep=int(sleep))
    print(status_code)
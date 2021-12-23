

import json
from boto3 import client as boto3_client


def invoke(sleep: int, workflow: list):
    aws_region = 'eu-central-1'
    client = boto3_client('lambda', region_name=aws_region)

    # call the first function a to start the workflow
    payload = {
        'workflow': workflow,
        'sleep': sleep
    }

    response = client.invoke(
        FunctionName='CoordinatorFunctionCoordinator',
        InvocationType='RequestResponse',
        Payload=json.dumps(payload)
    )

    return response['StatusCode']




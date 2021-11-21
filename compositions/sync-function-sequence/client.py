

import json
from boto3 import client as boto3_client

aws_region = 'eu-central-1'
client = boto3_client('lambda', region_name=aws_region)

# call the first function a to start the workflow
event = {
    'result': ''
}
response = client.invoke(
    FunctionName='SequenceFunctionA',
    InvocationType='RequestResponse',
    Payload=json.dumps(event)
)

if response['StatusCode'] == 200:
    result = json.load(response['Payload'])
    print(result['result'])




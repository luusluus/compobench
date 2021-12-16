import json
from boto3 import client as boto3_client

aws_region = 'eu-central-1'
client = boto3_client('lambda', region_name=aws_region)

# call the first function a to start the workflow
response = client.invoke(
    FunctionName='CompiledFunction',
    InvocationType='RequestResponse',
    Payload=json.dumps({'sleep': 8})
)

if response['StatusCode'] == 200:
    print(json.load(response['Payload']))

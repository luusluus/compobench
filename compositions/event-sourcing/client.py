import uuid
import json
from time import sleep

from boto3 import client as boto3_client

aws_region = 'eu-central-1'

# invoke controller once to start workflow
payload = {
    'input': '',
    'sleep': 2
}
client = boto3_client('lambda', region_name=aws_region)
response = client.invoke(
    FunctionName='EventSourcingProxyFunction',
    InvocationType='RequestResponse',
    Payload=json.dumps(payload)
)

if response['StatusCode'] == 200:
    print(response)
else:
    print('Composition Failed')

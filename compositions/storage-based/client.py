import json
import uuid
from boto3 import client as boto3_client
from compositions.aws_helpers.s3 import S3BucketHelper


aws_region = 'eu-central-1'

client = boto3_client('lambda', region_name=aws_region)

payload = {
    'workflow': ['function_b', 'function_c'],
    'sleep': 2,
    'waiter_config': {
        'delay': 1,
        'max_attempts': 30
    }
}

# call the first function a to start the workflow
response = client.invoke(
    FunctionName='StorageBasedProxyFunction',
    InvocationType='RequestResponse',
    Payload=json.dumps(payload)
)

if response['StatusCode'] == 200:
    print(response)
else:
    print('Composition Failed')



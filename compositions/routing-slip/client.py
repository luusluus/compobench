import json

from boto3 import client as boto3_client
from compositions.aws_helpers.s3 import S3BucketHelper


aws_region = 'eu-central-1'
bucket_name = 'routing-slip-store'
result_key = 'result_c.json'

client = boto3_client('lambda', region_name=aws_region)

payload = {
    'composition': ['RoutingSlipFunctionB', 'RoutingSlipFunctionC']
    }

response = client.invoke(
    FunctionName='RoutingSlipFunctionA',
    InvocationType='Event',
    Payload=json.dumps(payload),
)

if response['StatusCode'] == 202:
    s3_bucket_helper = S3BucketHelper(aws_region=aws_region)

    s3_bucket_helper.poll_object_from_bucket(bucket_name=bucket_name, object_key=result_key)

    response = s3_bucket_helper.get_object_from_bucket(bucket_name=bucket_name, object_key=result_key)
    result = json.loads(response['Body'].read())
    print(result['result'])

    s3_bucket_helper.delete_object_from_bucket(bucket_name=bucket_name, object_key=result_key)
else:
    print('Composition Failed')

import os
import json

from boto3 import client as boto3_client
from botocore.config import Config

from s3 import S3BucketHelper

def compose(event, business_logic_function):
    event['greet'] = business_logic_function(event['greet'])
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
        bucket_name = os.environ['BUCKET_NAME']
        s3_bucket_helper = S3BucketHelper(aws_region=os.environ['AWS_REGION'])
        result = event['greet']
        print(f'Saving final result: {result} to {bucket_name}')
        s3_bucket_helper.write_json_to_bucket(
            bucket_name=bucket_name,
            json_object={'result': result}, 
            object_key = 'result_c.json')

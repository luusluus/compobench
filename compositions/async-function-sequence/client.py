import requests
import json

from compositions.aws_helpers.api_gateway import ApiGatewayHelper
from compositions.aws_helpers.s3 import S3BucketHelper

aws_region = 'eu-central-1'
bucket_name = 'async-sequence-store'
result_key = 'result_c.json'

gateway_helper = ApiGatewayHelper(aws_region=aws_region)
endpoint = gateway_helper.get_api_gateway_endpoint(api_get_way_name='async-function-sequence')

# call the first function a to start the workflow
result = requests.get(endpoint + 'a')

s3_bucket_helper = S3BucketHelper(aws_region=aws_region)

s3_bucket_helper.poll_object_from_bucket(bucket_name=bucket_name, object_key=result_key)

response = s3_bucket_helper.get_object_from_bucket(bucket_name=bucket_name, object_key=result_key)
result = json.loads(response['Body'].read())
print(result['greet'])

s3_bucket_helper.delete_object_from_bucket(bucket_name=bucket_name, object_key=result_key)

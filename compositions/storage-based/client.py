

import json
import uuid
from boto3 import client as boto3_client
from botocore.exceptions import ClientError

from compositions.aws_helpers.s3 import S3BucketHelper


aws_region = 'eu-central-1'
result_key = 'result.json'
bucket_name = 'storage-based-store'


s3_bucket_helper = S3BucketHelper(aws_region=aws_region)


# Publish a message to the first topic to start the workflow
try:
    s3_bucket_helper.write_json_to_bucket(
        bucket_name=bucket_name, 
        json_object={
            'workflow': ['function_b', 'function_c', 'function_d'],
            'sleep': 8
        }, 
        object_key='function_a/result.json')


    s3_bucket_helper.poll_object_from_bucket(bucket_name=bucket_name, object_key=result_key)

    response = s3_bucket_helper.get_object_from_bucket(bucket_name=bucket_name, object_key=result_key)
    print(response)

    s3_bucket_helper.delete_object_from_bucket(bucket_name=bucket_name, object_key=result_key)

except ClientError as e:
    print(e)
    print('Composition Failed')



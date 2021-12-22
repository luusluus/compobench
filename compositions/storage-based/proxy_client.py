import os
import json
import uuid
import time

from boto3 import client as boto3_client
from botocore.exceptions import ClientError

from s3 import S3BucketHelper

def lambda_handler(event, context):
    aws_region = os.environ['AWS_REGION']
    workflow_instance_id = str(uuid.uuid4())
    bucket_name = os.environ.get('BUCKET_NAME')
    result_key = f'results/{workflow_instance_id}.json'

    s3_bucket_helper = S3BucketHelper(aws_region=aws_region)

    # Publish a message to the first topic to start the workflow
    
    s3_bucket_helper.write_json_to_bucket(
        bucket_name=bucket_name, 
        json_object={
            'workflow': event['workflow'],
            'sleep': event['sleep'],
            'workflow_instance_id': workflow_instance_id
        }, 
        object_key='function_a/result.json')

    time.sleep(event['sleep'] * 3 + 2)

    waiter_config = event['waiter_config']
    s3_bucket_helper.poll_object_from_bucket(
            bucket_name=bucket_name,
            object_key=result_key,
            waiter_config={
                'Delay': waiter_config['delay'],
                'MaxAttempts': waiter_config['max_attempts']
            }
        )

    s3_bucket_helper.delete_object_from_bucket(bucket_name=bucket_name, object_key=result_key)

    return




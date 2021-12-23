import os
import json
import uuid
import time
import logging

from boto3 import client as boto3_client
from botocore.exceptions import ClientError

from compositions.aws_helpers.s3 import S3BucketHelper

def invoke(sleep: int, workflow: list, full_workflow: list, waiter_config: dict):
    aws_region = 'eu-central-1'
    workflow_instance_id = str(uuid.uuid4())
    bucket_name = 'storage-based-store'
    result_key = f'results/{workflow_instance_id}.json'

    s3_bucket_helper = S3BucketHelper(aws_region=aws_region)

    # Publish a message to the first topic to start the workflow
    
    s3_bucket_helper.write_json_to_bucket(
        bucket_name=bucket_name, 
        json_object={
            'workflow': workflow,
            'sleep': sleep,
            'workflow_instance_id': workflow_instance_id
        }, 
        object_key=f'function_a/{workflow_instance_id}.json')

    time.sleep(sleep * 3 + 2)

    try:
        s3_bucket_helper.poll_object_from_bucket(
                bucket_name=bucket_name,
                object_key=result_key,
                waiter_config={
                    'Delay': waiter_config['delay'],
                    'MaxAttempts': waiter_config['max_attempts']
                }
            )

        for function in full_workflow:
            object_key = f'{function}/{workflow_instance_id}.json'
            print(f'deleting {object_key}')
            s3_bucket_helper.delete_object_from_bucket(bucket_name=bucket_name, object_key=object_key)

        print(f'deleting {result_key}')
        s3_bucket_helper.delete_object_from_bucket(bucket_name=bucket_name, object_key=result_key)
        status_code = 200
    
    except Exception as e:
        print(e)
        status_code = 404

    return status_code


# invoke(
#     sleep=2, 
#     workflow=["function_b", "function_c"],
#     full_workflow=["function_a", "function_b", "function_c"],
#     waiter_config={
#                     "delay": 1,
#                     "max_attempts": 30
#                 })
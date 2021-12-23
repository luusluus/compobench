import os
import json
import uuid
import time

from compositions.aws_helpers.aws_lambda import LambdaHelper
from compositions.aws_helpers.s3 import S3BucketHelper

def invoke(sleep: int, waiter_config: dict):
    aws_region = 'eu-central-1'
    lambda_helper = LambdaHelper(aws_region=aws_region)
    s3_helper = S3BucketHelper(aws_region=aws_region)

    workflow_instance_id = str(uuid.uuid4())
    bucket_name = 'async-sequence-store'
    result_key = f'result_{workflow_instance_id}.json'

    print(result_key)
    response = lambda_helper.invoke_lambda_async(
        function_name='AsyncSequenceFunctionA', 
        payload={
            'sleep': sleep,
            'workflow_instance_id': workflow_instance_id
        })

    status_code = response['StatusCode']
    if status_code == 202:
        time.sleep(sleep * 3)

        try:
            s3_helper.poll_object_from_bucket(
                    bucket_name=bucket_name,
                    object_key=result_key,
                    waiter_config={
                        'Delay': waiter_config['delay'],
                        'MaxAttempts': waiter_config['max_attempts']
                    }
                )
            status_code = 200
            s3_helper.delete_object_from_bucket(bucket_name=bucket_name, object_key=result_key)
        except Exception as e:
            print(e)
            status_code = 404

    return status_code
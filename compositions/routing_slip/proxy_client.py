import os
import json
import uuid
import time

from aws_lambda import LambdaHelper
from s3 import S3BucketHelper


def lambda_handler(event, context):
    aws_region = os.environ['AWS_REGION']
    lambda_helper = LambdaHelper(aws_region=aws_region)
    s3_helper = S3BucketHelper(aws_region=aws_region)

    workflow_instance_id = str(uuid.uuid4())
    bucket_name = os.environ.get('BUCKET_NAME')
    result_key = f'result_{workflow_instance_id}.json'

    print(result_key)
    response = lambda_helper.invoke_lambda_async(
        function_name='RoutingSlipFunctionA', 
        payload={
            'sleep': event['sleep'],
            'workflow_instance_id': workflow_instance_id,
            'composition': event['composition']
        })

    status_code = response['StatusCode']
    if status_code == 202:
        time.sleep(event['sleep'] * 3)

        waiter_config = event['waiter_config']
        s3_helper.poll_object_from_bucket(
                bucket_name=bucket_name,
                object_key=result_key,
                waiter_config={
                    'Delay': waiter_config['delay'],
                    'MaxAttempts': waiter_config['max_attempts']
                }
            )
        s3_helper.delete_object_from_bucket(bucket_name=bucket_name, object_key=result_key)

        return
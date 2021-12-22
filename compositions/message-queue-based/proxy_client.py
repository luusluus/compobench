import os
import json
import uuid
import time

from boto3 import client as boto3_client
from botocore.exceptions import ClientError

from s3 import S3BucketHelper


def lambda_handler(event, context):
    aws_region = os.environ['AWS_REGION']
    s3_helper = S3BucketHelper(aws_region=aws_region)

    workflow_instance_id = str(uuid.uuid4())
    bucket_name = os.environ.get('BUCKET_NAME')
    result_key = f'result_{workflow_instance_id}.json'

    client = boto3_client('sns', region_name=aws_region)

    topics = client.list_topics()['Topics']

    first_topic = topics[0]['TopicArn']
    client.publish(
        TopicArn=first_topic,
        MessageAttributes=event['message_attributes'],
        Message=json.dumps({
            'sleep': event['sleep'],
            'workflow_instance_id': workflow_instance_id
        })
    )

    time.sleep(event['sleep'] * 3)

    s3_bucket_helper = S3BucketHelper(aws_region=aws_region)

    waiter_config = event['waiter_config']
    s3_bucket_helper.poll_object_from_bucket(
        bucket_name=bucket_name, 
        object_key=result_key,
        waiter_config={
            'Delay': waiter_config['delay'],
            'MaxAttempts': waiter_config['max_attempts']
        })

    s3_bucket_helper.delete_object_from_bucket(bucket_name=bucket_name, object_key=result_key)

    return

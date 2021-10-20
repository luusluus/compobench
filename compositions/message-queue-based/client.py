

import json
import uuid
from boto3 import client as boto3_client
from botocore.exceptions import ClientError

from compositions.aws_helpers.s3 import S3BucketHelper


aws_region = 'eu-central-1'
result_key = 'result.json'
bucket_name = 'message-queue-store'

client = boto3_client('sns', region_name=aws_region)

topics = client.list_topics()['Topics']

first_topic = topics[0]['TopicArn']


# Publish a message to the first topic to start the workflow
try:
    client.publish(
        TopicArn=first_topic,
        Message=json.dumps({'message': 'start'})
    )

    s3_bucket_helper = S3BucketHelper(aws_region=aws_region)

    s3_bucket_helper.poll_object_from_bucket(bucket_name=bucket_name, object_key=result_key)

    response = s3_bucket_helper.get_object_from_bucket(bucket_name=bucket_name, object_key=result_key)
    print(response['result'])

    s3_bucket_helper.delete_object_from_bucket(bucket_name=bucket_name, object_key=result_key)

except ClientError as e:
    print(e)
    print('Composition Failed')



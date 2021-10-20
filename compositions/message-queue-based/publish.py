import os
import json

from boto3 import client as boto3_client

def publish(message, caller):
    aws_region = os.environ['AWS_REGION']

    topic_arn = os.environ['TOPIC_ARN']

    client = boto3_client('sns', region_name=aws_region)

    print(f'Publishing message: {message} to topic {topic_arn}')

    client.publish(
        Message=message,
        MessageAttributes={
            'caller': {
                'DataType': 'String',
                'StringValue': caller,
            }
        },
        TopicArn=topic_arn)
import os
import json

from boto3 import client as boto3_client

class S3BucketHelper():
    def __init__(self, aws_region):
        self._client = boto3_client('s3', region_name=aws_region)

    def write_json_to_bucket(self, bucket_name, json_object, object_key):
        self._client.put_object(
            Body=json.dumps(json_object),
            Bucket=bucket_name,
            Key=object_key # key_name.json
        )

    def poll_object_from_bucket(self, 
        bucket_name, 
        object_key, 
        waiter_config: dict = {
                'Delay': 1,
                'MaxAttempts': 30
            }):
        waiter = self._client.get_waiter('object_exists')

        waiter.wait(
            Bucket=bucket_name,
            Key=object_key,
            WaiterConfig=waiter_config
        )

    def get_object_from_bucket(self, bucket_name, object_key):
        response = self._client.get_object(
            Bucket=bucket_name,
            Key=object_key
        )

        return json.loads(response['Body'].read())

    def delete_object_from_bucket(self, bucket_name, object_key):
        return self._client.delete_object(
            Bucket=bucket_name,
            Key=object_key
        )
import json

from boto3 import client as boto3_client

from .WorkflowExecutor import WorkflowExecutor

class StorageBasedWorkflowExecutor(WorkflowExecutor):
    def __init__(
        self,
        payload: dict,
        bucket_name: str,
        first_function: str
    ):
        super().__init__(payload=payload)
        self.bucket_name = bucket_name
        self.first_function = first_function
        self.s3_client = boto3_client('s3', region_name='eu-central-1')

    def start(self):
        self.s3_client.put_object(
            Body=json.dumps(self._payload),
            Bucket=self.bucket_name,
            Key=f'{self.first_function}/{self._payload["workflow_instance_id"]}.json'
        )

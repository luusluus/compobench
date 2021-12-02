import json

from boto3 import client as boto3_client

from .WorkflowExecutor import WorkflowExecutor

class StorageBasedWorkflowExecutor(WorkflowExecutor):
    def __init__(self, composition_name, workflow_instance_id):
        super().__init__(composition_name, workflow_instance_id)
        self.s3_client = boto3_client('s3', region_name='eu-central-1')

    def start(self):
        payload = self.config["payload"]
        bucket_name = self.config["bucket_name"]
        first_function = self.config["first_function"]
        
        payload["workflow_instance_id"] = self.workflow_instance_id
        self.s3_client.put_object(
            Body=json.dumps(payload),
            Bucket=bucket_name,
            Key=f'{first_function}/{payload["workflow_instance_id"]}.json'
        )

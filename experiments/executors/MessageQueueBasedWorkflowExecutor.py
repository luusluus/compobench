import json

from boto3 import client as boto3_client

from .WorkflowExecutor import WorkflowExecutor

class MessageQueueBasedWorkflowExecutor(WorkflowExecutor):
    def __init__(self, composition_name, workflow_instance_id):
        super().__init__(composition_name, workflow_instance_id)
        self.sns_client = boto3_client('sns', region_name='eu-central-1')

    def start(self):
        topics = self.sns_client.list_topics()['Topics']
        first_topic = topics[0]['TopicArn']

        payload = self.config["payload"]
        message_attributes = self.config["message_attributes"]
        payload["workflow_instance_id"] = self.workflow_instance_id
        self.sns_client.publish(
            TopicArn=first_topic,
            MessageAttributes=message_attributes,
            Message=json.dumps(payload)
        )

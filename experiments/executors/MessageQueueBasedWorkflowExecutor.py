import json

from boto3 import client as boto3_client

from .WorkflowExecutor import WorkflowExecutor

class MessageQueueBasedWorkflowExecutor(WorkflowExecutor):
    def __init__(
        self,
        payload: dict,
        message_attributes: {},
    ):
        super().__init__(payload=payload)
        self.message_attributes = message_attributes
        self.sns_client = boto3_client('sns', region_name='eu-central-1')

    def start(self):
        topics = self.sns_client.list_topics()['Topics']
        first_topic = topics[0]['TopicArn']

        self.sns_client.publish(
            TopicArn=first_topic,
            MessageAttributes=self.message_attributes,
            Message=json.dumps(self._payload)
        )

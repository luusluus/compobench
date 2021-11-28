import os
import json

from boto3 import client as boto3_client
from aws_xray_sdk.core import xray_recorder

from .WorkflowExecutor import WorkflowExecutor

class ClientsideWorkflowExecutor(WorkflowExecutor):
    def __init__(
        self,
        payload: dict,
        workflow: list,
    ):
        super().__init__(payload=payload)
        self._workflow = workflow

        self._lambda_client = boto3_client('lambda', region_name='eu-central-1')


    def start(self):
        segment = xray_recorder.begin_segment('Client')

        segment.put_annotation('workflow_instance_id', self._payload['workflow_instance_id'])

        result = ''
        for step in self._workflow:
            response = self._lambda_client.invoke(
                FunctionName=step,
                InvocationType='RequestResponse',
                Payload=json.dumps(self._payload)
            )

            result = response

        print(result)
        xray_recorder.end_segment()
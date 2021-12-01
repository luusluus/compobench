import os
import json
from threading import Thread

from compositions.aws_helpers.aws_lambda import LambdaHelper

from aws_xray_sdk.core import xray_recorder

from .WorkflowExecutor import WorkflowExecutor

xray_recorder.configure(
    sampling=False,
    daemon_address='127.0.0.1:2000',
)

class ClientsideWorkflowThread(Thread):
    def __init__(self, payload, workflow, workflow_instance_id):
        Thread.__init__(self)
        self.payload = payload
        self.workflow = workflow
        self.workflow_instance_id = workflow_instance_id
        self.lambda_helper = LambdaHelper(aws_region='eu-central-1')

    def run(self):
        segment = xray_recorder.begin_segment('Client')
        segment.put_annotation('workflow_instance_id', self.workflow_instance_id)
        result = ''
        for step in self.workflow:
            response = self.lambda_helper.invoke_lambda(
                function_name=step, 
                payload=self.payload
            )

            result += response

        print(result)
        xray_recorder.end_segment()

class ClientsideWorkflowExecutor(WorkflowExecutor):
    def __init__(self, composition_name, workflow_instance_id):
        super().__init__(composition_name, workflow_instance_id)

    def start(self):
        workflow = self.config["workflow"]
        payload = self.config["payload"]
        payload["workflow_instance_id"] = self.workflow_instance_id

        thread = ClientsideWorkflowThread(
            payload=payload, 
            workflow=workflow,
            workflow_instance_id=self.workflow_instance_id)

        thread.start()

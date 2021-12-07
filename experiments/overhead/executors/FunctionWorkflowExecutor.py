import json
from threading import Thread

from compositions.aws_helpers.aws_lambda import LambdaHelper
from .WorkflowExecutor import WorkflowExecutor


class FunctionWorkflowExecutor(WorkflowExecutor):
    def __init__(self, composition_name, workflow_instance_id):
        super().__init__(composition_name, workflow_instance_id)

        self.lambda_helper = LambdaHelper(aws_region='eu-central-1')

    def start(self):
        first_function_name = self.config["first_function_name"]
        payload = self.config["payload"]
        payload["workflow_instance_id"] = self.workflow_instance_id

        if self.config["lambda_invocation_type"] == "SYNC":
            thread = Thread(target=self.lambda_helper.invoke_lambda, args = (first_function_name, payload, ))
            thread.start()
        else:
            self.lambda_helper.invoke_lambda_async(
                function_name=first_function_name, 
                payload=payload
            )

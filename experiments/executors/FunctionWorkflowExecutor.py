import json
import subprocess
import boto3
import uuid

from .WorkflowExecutor import WorkflowExecutor

class FunctionWorkflowExecutor(WorkflowExecutor):
    def __init__(self, experiment_name: str):
        super().__init__(experiment_name=experiment_name)


    def start(self, concurrent_workers, duration, rate_limit):
        first_function_name = self.workflow_config["first_function_name"]
        payload = self.workflow_config["payload"]

        # url = f'https://lambda.eu-central-1.amazonaws.com/2015-03-31/functions/{first_function_name}/invocations'
        url = f'http://localhost:8000/{self.experiment_name}'

        hey_command = self.build_hey_command(
            url=url, 
            payload=payload, 
            concurrent_workers=concurrent_workers,
            duration=duration,
            rate_limit=rate_limit)

        print(' '.join(hey_command))
        return self.execute_hey(hey_command=hey_command)




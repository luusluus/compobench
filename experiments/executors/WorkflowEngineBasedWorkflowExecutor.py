import json

from boto3 import client as boto3_client

from .WorkflowExecutor import WorkflowExecutor
class WorkflowEngineBasedWorkflowExecutor(WorkflowExecutor):
    def __init__(
        self,
        payload: dict,
        stack_name: str
    ):
        super().__init__(payload=payload)
        self.stack_name = stack_name
        self.cf_client = boto3_client('cloudformation', region_name='eu-central-1')
        self.sf_client = boto3_client('stepfunctions', region_name='eu-central-1')

    def start(self):
        response = self.cf_client.list_stack_resources(StackName=self.stack_name)
        resources = response["StackResourceSummaries"]
        state_machine_resources = [resource for resource in resources if resource["LogicalResourceId"] == "WorkflowStateMachine"]
        state_machine_arn = state_machine_resources[0]["PhysicalResourceId"]

        self.sf_client.start_execution(
            stateMachineArn=state_machine_arn, 
            name=f'integ-test-{self._payload["workflow_instance_id"]}', 
            input=json.dumps(self._payload)
        )
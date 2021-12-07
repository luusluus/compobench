import json

from boto3 import client as boto3_client

from .WorkflowExecutor import WorkflowExecutor
class WorkflowEngineBasedWorkflowExecutor(WorkflowExecutor):
    def __init__(self, composition_name, workflow_instance_id):
        super().__init__(composition_name, workflow_instance_id)
        self.cf_client = boto3_client('cloudformation', region_name='eu-central-1')
        self.sf_client = boto3_client('stepfunctions', region_name='eu-central-1')

    def start(self):
        payload = self.config["payload"]
        payload["workflow_instance_id"] = self.workflow_instance_id
        stack_name = self.config["stack_name"]

        response = self.cf_client.list_stack_resources(StackName=stack_name)
        resources = response["StackResourceSummaries"]
        state_machine_resources = [resource for resource in resources if resource["LogicalResourceId"] == "WorkflowStateMachine"]
        state_machine_arn = state_machine_resources[0]["PhysicalResourceId"]

        self.sf_client.start_execution(
            stateMachineArn=state_machine_arn, 
            name=f'integ-test-{payload["workflow_instance_id"]}', 
            input=json.dumps(payload)
        )
import os
import json
import uuid
import time

from boto3 import client as boto3_client

def invoke(sleep: int, waiter_config: dict):
    aws_region = 'eu-central-1'
    stack_name = 'workflow-engine'

    cloud_formations_client = boto3_client('cloudformation', region_name=aws_region)
    response = cloud_formations_client.list_stack_resources(StackName=stack_name)
    resources = response["StackResourceSummaries"]
    state_machine_resources = [resource for resource in resources if resource["LogicalResourceId"] == "WorkflowStateMachine"]
    state_machine_arn = state_machine_resources[0]["PhysicalResourceId"]

    step_functions_client = boto3_client('stepfunctions', region_name=aws_region)

    workflow_instance_id = str(uuid.uuid4())
    payload = {
        'sleep': sleep,
        'workflow_instance_id': workflow_instance_id
    }
    response = step_functions_client.start_execution(
                stateMachineArn=state_machine_arn, 
                name=f"integ-test-{workflow_instance_id}", 
                input=json.dumps(payload)
            )
    execution_arn = response["executionArn"]

    time.sleep(sleep * 3)
    while True:
        response = step_functions_client.describe_execution(executionArn=execution_arn)
        status = response["status"]
        if status == "SUCCEEDED":
            print(json.loads(response['output']))
            break
        elif status == "RUNNING":
            time.sleep(1)
        else:
            print(f"Execution {execution_arn} failed with status {status}")
            break

    return
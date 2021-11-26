import os

from aws_lambda import LambdaHelper
import event_definitions

    # NOTE: Constraint from AWS Lambda and DynamoDB. 
    # No way to specify in AWS CloudFormation or SAM to filter DynamoDB event
    # Have to pay one extra lambda invocation to filter this.

def lambda_handler(event, context):
    # split and filter events based on workflow_instance_id to dispatch events to each orchestrator
    workflows_data = filter_completed_workflows(event=event)
    # check if last event is caused by a business logic function
    workflows_data = filter_orchestrator_caused_events(workflows_data=workflows_data)
    # invoke orchestrators 
    invoke_orchestrators(workflows_data=workflows_data)

def filter_completed_workflows(event):
    workflows_data = {}
    for record in event['Records']:
        key = record['dynamodb']['Keys']
        workflow_instance_id = key['WorkflowInstanceId']['S']
        if 'workflow_instance_id' not in workflows_data:
            workflows_data[workflow_instance_id] = {}

        # check if workflow has finished
        image = record['dynamodb']['NewImage']
        is_finished = True if image['EventTypeId']['N'] == event_definitions.EXECUTION_COMPLETED['id'] else False

        workflows_data[workflow_instance_id]['is_finished'] = is_finished

        if 'events' not in workflows_data[workflow_instance_id]:
            workflows_data[workflow_instance_id]['events'] = []
        
        workflows_data[workflow_instance_id]['events'].append(record)
    return workflows_data

def filter_orchestrator_caused_events(workflows_data):
    for workflow_instance_id, value in workflows_data.items():
        is_orchestrator_caused = False if int(value['events'][-1]['dynamodb']['NewImage']['EventTypeId']['N']) == event_definitions.FUNCTION_COMPLETED['id'] else True
        workflows_data[workflow_instance_id]['is_orchestrator_caused'] = is_orchestrator_caused
    return workflows_data

def invoke_orchestrators(workflows_data):
    lambda_helper = LambdaHelper(aws_region=os.environ['AWS_REGION'])
    for workflow_instance_id, workflow_data in workflows_data.items():
        if not workflow_data['is_finished'] and not workflow_data['is_orchestrator_caused']:
            payload = { 
                'workflow_instance_id': workflow_instance_id,
            }
            lambda_helper.invoke_lambda_async(
                function_name='EventSourcingOrchestrator', 
                payload=payload)
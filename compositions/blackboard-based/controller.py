import os
from dynamodb import DynamoDBTableHelper, NoItemException
from aws_lambda import LambdaHelper

class NoValidWorkflowEvent(Exception):
    pass

def lambda_handler(event, context):
    aws_region = os.environ['AWS_REGION']
    table_name = os.environ['DEFINITION_TABLE']
    workflow_definition_table = DynamoDBTableHelper(
        aws_region=aws_region, 
        table_name=table_name)
    lambda_helper = LambdaHelper(aws_region=aws_region)

    # get first workflow by id = 1
    query_result = workflow_definition_table.query(
        partition_key_name='WorkflowId',
        partition_key_value=1
    )

    workflow = query_result
    workflow_definition = query_result[0]

    workflow_id = int(workflow_definition['WorkflowId'])
    try:
        # start a new workflow
        if 'workflow_instance_id' in event:
            workflow_instance_id = event['workflow_instance_id']
            step_id = int(workflow_definition['StepId'])
            function_name = workflow_definition['StepFunction']
            previous_step_id = step_id

        # currently executing a workflow
        elif 'Records' in event:

            # get workflow_instance_id, workflow_id and step_id
            dynamodb = event['Records'][0]['dynamodb']
            keys = dynamodb['Keys']
            workflow_instance_id = keys['WorkflowInstanceId']['S']
            previous_step_id = int(keys['StepId']['N'])
            step_id = previous_step_id + 1 

            # and determine what the next step is in the workflow

            function_name = next((step['StepFunction'] for step in workflow if int(step['StepId']) == step_id), None)
            if not function_name:
                print('workflow finished')
                return

        else:
            # not a valid event
            raise NoValidWorkflowEvent

        # invoke step
        lambda_helper.invoke_lambda_async(
            function_name=function_name, 
            payload={
                'instance_id': workflow_instance_id,
                'workflow_id': workflow_id,
                'step_id': step_id,
                'previous_step_id': previous_step_id
            })
    except NoValidWorkflowEvent:
        print('not a valid workflow event')
        raise
    except Exception:
        raise




import os
import cfnresponse

from botocore.exceptions import ClientError

from dynamodb import DynamoDBTableHelper

def lambda_handler(event, context):
    response_data = {}
    try:
        if event['RequestType'] == 'Delete':
            cfnresponse.send(event, context, cfnresponse.SUCCESS, response_data)
        
        elif event['RequestType'] == 'Create' or event['RequestType'] == 'Update':
            table_name = os.environ['DEFINITION_TABLE']
            
            populate_workflow_definition_table(table_name=table_name)
            cfnresponse.send(event, context, cfnresponse.SUCCESS, response_data)
            
        else:
            raise Exception
    except Exception as e:
        print(e)
        cfnresponse.send(event, context, cfnresponse.FAILED, response_data)

def populate_workflow_definition_table(table_name: str):
    dynamo_db_helper = DynamoDBTableHelper(
        aws_region=os.environ['AWS_REGION'],
        table_name=table_name)

    workflow = {
        'id': 1,
        'steps': [
            {
                'id': 1,
                'function': 'BlackboardFunctionA'
            },
            {
                'id': 2,
                'function': 'BlackboardFunctionB'
            },
            {
                'id': 3,
                'function': 'BlackboardFunctionC'
            },
        ]
    }

    for step in workflow['steps']:
        item = {
            'WorkflowId': workflow['id'],
            'StepId': step['id'],
            'StepFunction': step['function']
        }
        dynamo_db_helper.put_item(item=item)
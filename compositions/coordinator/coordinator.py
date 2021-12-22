import os
import uuid
from aws_lambda import LambdaHelper

def lambda_handler(event, context):
    if 'workflow_instance_id' not in event:
        event['workflow_instance_id'] = str(uuid.uuid4())
    workflow_instance_id = event['workflow_instance_id']

    workflow = event['workflow']

    lambda_helper = LambdaHelper(aws_region=os.environ['AWS_REGION'])

    payload = {
        'sleep': event['sleep'],
        'workflow_instance_id': workflow_instance_id
    }

    for step in workflow:
        lambda_helper.invoke_lambda(
            function_name=step, 
            payload=payload
        )

    return payload
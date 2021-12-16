import os
import uuid
import time
from aws_lambda import LambdaHelper

from aws_xray_sdk.core import patch_all
from aws_xray_sdk.core import xray_recorder

patch_all()

def lambda_handler(event, context):
    if 'workflow_instance_id' not in event:
        event['workflow_instance_id'] = str(uuid.uuid4())
        time.sleep(event['sleep'])

    subsegment = xray_recorder.begin_subsegment('Identification')
    workflow_instance_id = event['workflow_instance_id']
    subsegment.put_annotation('workflow_instance_id', event['workflow_instance_id'])
    xray_recorder.end_subsegment()

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
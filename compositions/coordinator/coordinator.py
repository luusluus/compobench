import os
from aws_lambda import LambdaHelper

from aws_xray_sdk.core import patch_all
from aws_xray_sdk.core import xray_recorder

patch_all()

def lambda_handler(event, context):
    subsegment = xray_recorder.begin_subsegment('Identification')
    workflow_instance_id = event['workflow_instance_id']
    subsegment.put_annotation('workflow_instance_id', event['workflow_instance_id'])
    xray_recorder.end_subsegment()

    workflow = event['workflow']
    function_input = event['input']

    lambda_helper = LambdaHelper(aws_region=os.environ['AWS_REGION'])

    payload = {
        'result': function_input,
        'workflow_instance_id': workflow_instance_id
    }

    for step in workflow:
        response = lambda_helper.invoke_lambda(
            function_name=step, 
            payload=payload
        )

        payload['result'] += response

    return payload['result']
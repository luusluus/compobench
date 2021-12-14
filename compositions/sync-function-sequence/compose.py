import os

from aws_xray_sdk.core import xray_recorder

from aws_lambda import LambdaHelper

def compose(event, function_name, business_logic_function):
    subsegment = xray_recorder.begin_subsegment('Identification')
    result = business_logic_function(event['result'])
    subsegment.put_annotation('workflow_instance_id', event['workflow_instance_id'])
    xray_recorder.end_subsegment()

    payload = {
        'result': business_logic_function(event['result']),
        'workflow_instance_id': event['workflow_instance_id']
    }
    if function_name == '':
        return payload
    else:
        lambda_helper = LambdaHelper(aws_region=os.environ['AWS_REGION'])
        return lambda_helper.invoke_lambda(
            function_name=function_name,
            payload=payload
        )

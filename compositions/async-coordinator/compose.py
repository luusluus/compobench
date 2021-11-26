import os

from aws_xray_sdk.core import xray_recorder

from aws_lambda import LambdaHelper

def compose(event, business_logic_function):
    subsegment = xray_recorder.begin_subsegment('Business Logic')
    result = business_logic_function(event['result'])
    subsegment.put_annotation('workflow_instance_id', event['workflow_instance_id'])
    xray_recorder.end_subsegment()

    aws_region = os.environ['AWS_REGION']
    event['result'] = result

    lambda_helper = LambdaHelper(aws_region=aws_region)
    lambda_helper.invoke_lambda_async(
        function_name='AsyncCoordinatorFunctionCoordinator', 
        payload=event)

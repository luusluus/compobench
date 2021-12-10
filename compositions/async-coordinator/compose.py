import os
import time

from aws_xray_sdk.core import xray_recorder

from aws_lambda import LambdaHelper

def compose(event):
    workflow_instance_id = event['workflow_instance_id']

    subsegment = xray_recorder.begin_subsegment('Identification')
    time.sleep(event['sleep'])
    subsegment.put_annotation('workflow_instance_id', workflow_instance_id)
    xray_recorder.end_subsegment()

    lambda_helper = LambdaHelper(aws_region=os.environ['AWS_REGION'])
    lambda_helper.invoke_lambda_async(
        function_name='AsyncCoordinatorFunctionCoordinator', 
        payload={
            'prev_invoked_function': os.environ.get('AWS_LAMBDA_FUNCTION_NAME'),
            'workflow': event['workflow'],
            'workflow_instance_id': workflow_instance_id,
            'sleep': event['sleep']
        })

import os
import time

from aws_lambda import LambdaHelper

def compose(event):
    workflow_instance_id = event['workflow_instance_id']

    time.sleep(event['sleep'])

    lambda_helper = LambdaHelper(aws_region=os.environ['AWS_REGION'])
    lambda_helper.invoke_lambda_async(
        function_name='AsyncCoordinatorFunctionCoordinator', 
        payload={
            'prev_invoked_function': os.environ.get('AWS_LAMBDA_FUNCTION_NAME'),
            'workflow': event['workflow'],
            'workflow_instance_id': workflow_instance_id,
            'sleep': event['sleep']
        })

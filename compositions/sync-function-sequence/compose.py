import os
import time

from aws_lambda import LambdaHelper

def compose(event, function_name):
    time.sleep(event['sleep'])

    payload = {
        'workflow_instance_id': event['workflow_instance_id'],
        'sleep': event['sleep']
    }
    if function_name == '':
        return payload
    else:
        lambda_helper = LambdaHelper(aws_region=os.environ['AWS_REGION'])
        return lambda_helper.invoke_lambda(
            function_name=function_name,
            payload=payload
        )

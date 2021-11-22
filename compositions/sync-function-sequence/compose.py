import os
from aws_lambda import LambdaHelper

def compose(event, function_name, business_logic_function):
    result = business_logic_function(event)
    result['workflow_id'] = event['workflow_id']
    if function_name == '':
        return result
    else:
        lambda_helper = LambdaHelper(aws_region=os.environ['AWS_REGION'])
        return lambda_helper.invoke_lambda(
            function_name=function_name,
            payload=result
        )

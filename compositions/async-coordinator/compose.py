import os
from aws_lambda import LambdaHelper

def compose(event, business_logic_function):
    print(event)
    aws_region = os.environ['AWS_REGION']
    return_value = business_logic_function(event['result'])
    event['result'] = return_value

    lambda_helper = LambdaHelper(aws_region=aws_region)
    lambda_helper.invoke_lambda_async(
        function_name='AsyncCoordinatorFunctionCoordinator', 
        payload=event)

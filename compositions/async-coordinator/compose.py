from aws_lambda import LambdaHelper

def compose(event, business_logic_function):
    aws_region = os.environ['AWS_REGION']
    result = business_logic_function()
    result['workflow_id'] = event['workflow_id']

    coordinator_function_name = 'AsyncCoordinatorFunctionCoordinator'

    lambda_helper = LambdaHelper(aws_region=aws_region)
    
    lambda_helper.invoke_lambda_async(function_name=coordinator_function_name, payload=result)

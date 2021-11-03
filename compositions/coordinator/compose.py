import os
from aws_lambda import LambdaHelper

def compose(function_name, payload):
    aws_region = os.environ['AWS_REGION']
    lambda_helper = LambdaHelper(aws_region=aws_region)
    return lambda_helper.invoke_lambda(function_name=function_name, payload=payload)

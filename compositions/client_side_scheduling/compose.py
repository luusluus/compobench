import os
from compositions.aws_helpers.aws_lambda import LambdaHelper

def compose(aws_region, function_name, data):
    lambda_helper = LambdaHelper(aws_region=aws_region)

    return lambda_helper.invoke_lambda(function_name=function_name, payload=data)

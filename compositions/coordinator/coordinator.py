from compose import compose

from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

patch_all()

def lambda_handler(event, context):
    workflow = event['workflow']
    function_input = event['input']

    result = {
        'result': function_input
    }

    for step in workflow:
        response = compose(function_name=step, payload=result)
        result = {
            'result': response
        }

    return result
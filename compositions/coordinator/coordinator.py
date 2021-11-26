from compose import compose

from aws_xray_sdk.core import patch_all

patch_all()

def lambda_handler(event, context):
    workflow_instance_id = event['workflow_instance_id']
    workflow = event['workflow']
    function_input = event['input']

    result = {
        'result': function_input,
        'workflow_instance_id': workflow_instance_id
    }

    for step in workflow:
        response = compose(function_name=step, payload=result)
        result = {
            'result': response,
            'workflow_instance_id': workflow_instance_id
        }

    return result
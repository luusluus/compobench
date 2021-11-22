from compose import compose

from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

patch_all()

def lambda_handler(event, context):
    workflow_id = event['workflow_id']
    subsegment = xray_recorder.begin_subsegment('Identification')
    subsegment.put_annotation('workflow_id', workflow_id)
    xray_recorder.end_subsegment()

    workflow = event['workflow']
    function_input = event['input']

    result = {
        'result': function_input,
        'workflow_id': workflow_id
    }

    for step in workflow:
        response = compose(function_name=step, payload=result)
        result = {
            'result': response,
            'workflow_id': workflow_id
        }

    return result
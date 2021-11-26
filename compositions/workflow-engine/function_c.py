import os

from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

patch_all()

def lambda_handler(event, context):
    subsegment = xray_recorder.begin_subsegment('Identification')
    subsegment.put_annotation('workflow_instance_id', event['workflow_instance_id'])
    xray_recorder.end_subsegment()
    return {
        'result': hello_world(prev_hello_world=event['result']),
        'workflow_instance_id': event['workflow_instance_id']
    }

def hello_world(prev_hello_world):
    function_name = os.path.basename(__file__).split('.')[0]
    return prev_hello_world + f'Hello world from {function_name}. '
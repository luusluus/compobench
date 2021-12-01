import os

from aws_xray_sdk.core import xray_recorder

def compose(event, business_logic_function):
    subsegment = xray_recorder.begin_subsegment('Business Logic')
    result = business_logic_function(event['result'])
    subsegment.put_annotation('workflow_instance_id', event['workflow_instance_id'])
    xray_recorder.end_subsegment()

    return result

import time
from aws_xray_sdk.core import xray_recorder

def compose(event):
    workflow_instance_id = event['workflow_instance_id']
    subsegment = xray_recorder.begin_subsegment('Identification')
    time.sleep(event['sleep'])
    subsegment.put_annotation('workflow_instance_id', workflow_instance_id)
    xray_recorder.end_subsegment()

    return {
        'workflow_instance_id': workflow_instance_id,
        'sleep': event['sleep']
    }
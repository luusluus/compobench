import os
import time
from aws_xray_sdk.core import xray_recorder

def compose(event):
    subsegment = xray_recorder.begin_subsegment('Identification')
    subsegment.put_annotation('workflow_instance_id', event['workflow_instance_id'])
    time.sleep(event['sleep'])
    xray_recorder.end_subsegment()

    return

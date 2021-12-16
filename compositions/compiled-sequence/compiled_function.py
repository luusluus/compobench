import time
import uuid
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

patch_all()

def function_a(sleep_time):
    time.sleep(sleep_time)

def function_b():
    pass

def function_c():
    pass

def function_d():
    pass

def lambda_handler(event, context):
    subsegment = xray_recorder.begin_subsegment('Identification')
    subsegment.put_annotation('workflow_instance_id', str(uuid.uuid4()))
    function_a(event['sleep'])
    function_b()
    function_c()
    function_d()
    xray_recorder.end_subsegment()
    
    return
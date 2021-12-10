import time
import uuid
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

patch_all()

def function_a(sleep_time):
    time.sleep(sleep_time)

def function_b(sleep_time):
    time.sleep(sleep_time)

def function_c(sleep_time):
    time.sleep(sleep_time)

def function_d(sleep_time):
    time.sleep(sleep_time)

def lambda_handler(event, context):
    subsegment = xray_recorder.begin_subsegment('Identification')
    subsegment.put_annotation('workflow_instance_id', str(uuid.uuid4()))
    function_a(event['sleep'])
    function_b(event['sleep'])
    function_c(event['sleep'])
    function_d(event['sleep'])
    xray_recorder.end_subsegment()
    
    return
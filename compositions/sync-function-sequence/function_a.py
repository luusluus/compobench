import os
from compose import compose
import uuid
import time


from aws_xray_sdk.core import patch_all

patch_all()

def lambda_handler(event, context):
    event['workflow_instance_id'] = str(uuid.uuid4())
    time.sleep(event['sleep'])
    return compose(event=event, function_name='SequenceFunctionB')
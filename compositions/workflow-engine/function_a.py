import os
import uuid
import time
from compose import compose

from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

patch_all()

def lambda_handler(event, context):
    event['workflow_instance_id'] = str(uuid.uuid4())
    time.sleep(event['sleep'])
    return compose(event=event)
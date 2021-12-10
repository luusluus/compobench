import os
from compose import compose
import uuid

from aws_xray_sdk.core import patch_all

patch_all()

def lambda_handler(event, context):
    event['workflow_instance_id'] = str(uuid.uuid4())
    return compose(event=event, function_name='SequenceFunctionB')
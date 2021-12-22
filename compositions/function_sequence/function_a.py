import os
from compose import compose
import uuid

def lambda_handler(event, context):
    event['workflow_instance_id'] = str(uuid.uuid4())
    return compose(event=event, function_name='SequenceFunctionB')
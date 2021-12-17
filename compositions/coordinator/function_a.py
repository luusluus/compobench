import os
import uuid
import time
from compose import compose

from aws_xray_sdk.core import patch_all

patch_all()

def lambda_handler(event, context):
    time.sleep(event['sleep'])
    return compose(event=event)
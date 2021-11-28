import os
from controller import Controller

from aws_xray_sdk.core import patch_all

patch_all()

def lambda_handler(event, context):
    controller = Controller(workflow_id=1)
    controller.determine_next_step(event=event)
    if controller.is_end_workflow():
        return

    controller.schedule_next_function()


import os
from controller import Controller

from aws_xray_sdk.core import patch_all

patch_all()

def lambda_handler(event, context):
    coordinator = Controller(workflow_id=1)
    coordinator.determine_next_step(event=event)
    if coordinator.is_end_workflow():
        return

    coordinator.schedule_next_function()


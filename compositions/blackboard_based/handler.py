import os
from controller import Controller

def lambda_handler(event, context):
    controller = Controller(workflow_id=1)
    controller.determine_next_step(event=event)
    if controller.is_end_workflow():
        return

    controller.schedule_next_function()


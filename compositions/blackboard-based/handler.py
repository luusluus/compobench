import os
from controller import Controller

def lambda_handler(event, context):
    coordinator = Controller(workflow_id=1)
    coordinator.determine_next_step(event=event)
    if coordinator.is_end_workflow():
        return

    coordinator.schedule_next_function()



from coordinator import Coordinator

from aws_xray_sdk.core import patch_all

patch_all()

def lambda_handler(event, context):
    workflow_instance_id = event['workflow_instance_id']
    if 'input' in event:
        workflow = event['workflow']
        workflow_input = event['input']
        coordinator = Coordinator(
            workflow_instance_id=workflow_instance_id,
            workflow_data={
                'workflow': workflow,
                'input': workflow_input
            })
    else:
        coordinator = Coordinator(workflow_instance_id=workflow_instance_id)

    if coordinator.is_end_workflow(event=event):
        return

    coordinator.determine_next_step(event=event)


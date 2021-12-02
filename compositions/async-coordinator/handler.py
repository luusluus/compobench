
from coordinator import Coordinator

from aws_xray_sdk.core import patch_all
from aws_xray_sdk.core import xray_recorder

patch_all()

def lambda_handler(event, context):
    subsegment = xray_recorder.begin_subsegment('Identification')
    workflow_instance_id = event['workflow_instance_id']
    subsegment.put_annotation('workflow_instance_id', event['workflow_instance_id'])
    xray_recorder.end_subsegment()
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


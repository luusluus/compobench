import uuid
from coordinator import Coordinator

def lambda_handler(event, context):
    if 'workflow_instance_id' not in event:
        event['workflow_instance_id'] = str(uuid.uuid4())

    workflow_instance_id = event['workflow_instance_id']

    coordinator = Coordinator(workflow_instance_id=workflow_instance_id)

    if coordinator.is_end_workflow(event=event):
        return

    coordinator.determine_next_step(event=event)


import time

def compose(event):
    workflow_instance_id = event['workflow_instance_id']
    time.sleep(event['sleep'])

    return {
        'workflow_instance_id': workflow_instance_id,
        'sleep': event['sleep']
    }
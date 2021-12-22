import os
import time
import uuid

import event_definitions
from orchestrator import Orchestrator
workflow_name = 'SimpleSequence'
workflow = ['EventSourcingFunctionA', 'EventSourcingFunctionB', 'EventSourcingFunctionC']
sleep_time = 2

def lambda_handler(event, context):
    # start a new workflow
    if 'input' in event:
        orchestrator = Orchestrator(
            is_start=True,
            workflow_data={
                'instance_id': event['workflow_instance_id'],
                'workflow': workflow,
                'name': workflow_name,
                'sleep': sleep_time
            })

        orchestrator.schedule_next_function(
            function_name=workflow[0],
            function_input=event['input']
        )

    else:
        # continue workflow
        orchestrator = Orchestrator(
            workflow_data={
                'instance_id': event['workflow_instance_id'],
                'workflow': workflow,
                'name': workflow_name,
                'sleep': sleep_time
            })

        orchestrator.replay_events()
        orchestrator.determine_next_step()




import os
import time

from aws_xray_sdk.core import patch_all
from aws_xray_sdk.core import xray_recorder

patch_all()

import event_definitions
from orchestrator import Orchestrator
workflow_name = 'SimpleSequence'
workflow = ['EventSourcingFunctionA', 'EventSourcingFunctionB', 'EventSourcingFunctionC']


def lambda_handler(event, context):
    workflow_instance_id = event['workflow_instance_id']
    print(f'workflow instance id: {workflow_instance_id}')

    # start a new workflow
    if 'input' in event:
        orchestrator = Orchestrator(
            is_start=True,
            workflow_data={
                'instance_id': workflow_instance_id,
                'workflow': workflow,
                'name': workflow_name,
            })

        orchestrator.schedule_next_function(
            function_name=workflow[0],
            function_input=event['input']
        )

    else:
        # continue workflow
        orchestrator = Orchestrator(
            workflow_data={
                'instance_id': workflow_instance_id,
                'workflow': workflow,
                'name': workflow_name,
            })

        orchestrator.replay_events()
        orchestrator.determine_next_step()




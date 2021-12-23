import os
from dynamodb import DynamoDBTableHelper, NoItemException
from aws_lambda import LambdaHelper

from aws_xray_sdk.core import xray_recorder

sleep_time = 2
class NoValidWorkflowEvent(Exception):
    pass

class Controller:
    def __init__(self, workflow_id: int):
        aws_region = os.environ['AWS_REGION']
        self._workflow_definition_table = DynamoDBTableHelper(
            aws_region=aws_region, 
            table_name=os.environ['DEFINITION_TABLE'])
        self._lambda_helper = LambdaHelper(aws_region=aws_region)

        self._workflow_data = self.__retrieve_workflow_data(workflow_id=workflow_id)
        self._state = None
        self._workflow_id = workflow_id

    def __retrieve_workflow_data(self, workflow_id):
        return self._workflow_definition_table.query(
            partition_key_name='WorkflowId',
            partition_key_value=workflow_id
        )

    def determine_next_step(self, event):
        # start a new workflow
        if 'workflow_instance_id' in event:
            print(event['workflow_instance_id'])
            # parse first step
            first_step = self._workflow_data[0]
            workflow_instance_id = event['workflow_instance_id']
            step_id = int(first_step['StepId'])
            next_function_name = first_step['StepFunction']
            previous_step_id = step_id

        # currently executing a workflow
        elif 'Records' in event:
            # get workflow_instance_id, workflow_id and step_id
            dynamodb = event['Records'][0]['dynamodb']
            keys = dynamodb['Keys']
            workflow_instance_id = keys['WorkflowInstanceId']['S']
            previous_step_id = int(keys['StepId']['N'])
            step_id = previous_step_id + 1
            next_function_name = next((step['StepFunction'] for step in self._workflow_data if int(step['StepId']) == step_id), None)
        else:
        # not a valid event
            raise NoValidWorkflowEvent

        subsegment = xray_recorder.begin_subsegment('Identification')
        subsegment.put_annotation('workflow_instance_id', workflow_instance_id)
        xray_recorder.end_subsegment()
        self._state = {
                'workflow_instance_id': workflow_instance_id,
                'next_function_name': next_function_name,
                'step_id': step_id,
                'previous_step_id': previous_step_id
            }

    def schedule_next_function(self):
        self._lambda_helper.invoke_lambda_async(
            function_name=self._state['next_function_name'], 
            payload={
                'workflow_instance_id': self._state['workflow_instance_id'],
                'workflow_id': self._workflow_id,
                'step_id': self._state['step_id'],
                'previous_step_id': self._state['previous_step_id'],
                'sleep': sleep_time
            })
    
    def is_end_workflow(self):
        if not self._state['next_function_name']:
            print('workflow finished')
            return True
        return False


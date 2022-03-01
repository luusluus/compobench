import os
import event_definitions
from aws_lambda import LambdaHelper
from event_helper import EventHelper
from dynamodb import DynamoDBTableHelper, NoItemException

class Orchestrator:
    def __init__(self, workflow_data, is_start: bool = False):
        self._lambda_helper = LambdaHelper(aws_region=os.environ['AWS_REGION'])
        self._eventhelper = EventHelper(
            aws_region=os.environ['AWS_REGION'], 
            table_name=os.environ['EVENT_HISTORY_TABLE'],
            workflow_instance_id=workflow_data['instance_id'])

        self._workflow_instance_id = workflow_data['instance_id']
        self._workflow = workflow_data['workflow']
        self._state = {}

        if is_start:
            self._eventhelper.start_execution(name=workflow_data['name'])
        self._eventhelper.start_orchestrator()
        

    def determine_next_step(self):
        function_states = self._state['function_states']
        try:
            index = next((index for (index, function_state) in enumerate(function_states) if function_state["is_completed"] == False))
            next_function = function_states[index]
            if index > 0:
                previous_function_result = function_states[index - 1]['result']
            else:
                previous_function_result = ''

            print(f'scheduling next function {next_function["name"]}')
            self.schedule_next_function(
                function_name=next_function['name'],
                function_input=previous_function_result)

        except StopIteration:
            result = function_states[-1]['result']
            self._eventhelper.complete_orchestrator()
            self._eventhelper.complete_execution(result=result)
            self._eventhelper.write_events_batch()

    
    def schedule_next_function(self, function_name, function_input):
        self._eventhelper.schedule_function(name=function_name)
        self._eventhelper.complete_orchestrator()
        self._eventhelper.write_events_batch()

        self._lambda_helper.invoke_lambda_async(
            function_name=function_name, 
            payload={
                'workflow_instance_id': self._workflow_instance_id,
                'input': function_input,
            })

    def replay_events(self):
        events = self._eventhelper.get_events_by_id(instance_id=self._workflow_instance_id)

        execution_state = {
            'is_started': False,
            'is_completed': False,
        }

        orchestrator_state = {
            'is_started': False,
            'is_completed': False,
        }
        function_states = [
            {
                'is_scheduled': False,
                'is_completed': False,
                'name': function_name,
                'result': '',
                'input': ''
            }
            for function_name in self._workflow] 

        for event in events:
            event_type_id = int(event.get('EventTypeId', ''))
            
            if event_type_id == event_definitions.EXECUTION_STARTED['id']:
                execution_state['is_started'] = True

            if event_type_id == event_definitions.EXECUTION_COMPLETED['id']:
                execution_state['is_completed'] = True

            if event_type_id == event_definitions.ORCHESTRATOR_STARTED['id']:
                orchestrator_state['is_started'] = True

            if event_type_id == event_definitions.ORCHESTRATOR_COMPLETED['id']:
                orchestrator_state['is_completed'] = True
            
            if event_type_id == event_definitions.FUNCTION_SCHEDULED['id']:
                function = next((function_state for function_state in function_states if function_state['name'] == event.get('Name', '')), None)
                if function:
                    function['is_scheduled'] = True
                    function['input'] = event.get('FunctionInput', '')

            if event_type_id == event_definitions.FUNCTION_COMPLETED['id']:
                function = next((function_state for function_state in function_states if function_state['name'] == event.get('Name', '')), None)
                if function:
                    function['is_completed'] = True
                    function['result'] = event.get('Result', '')

        self._state = {
            'execution_state': execution_state,
            'orchestrator_state': orchestrator_state,
            'function_states': function_states
        }



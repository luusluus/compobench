import time
import uuid

from dynamodb import DynamoDBTableHelper
import event_definitions as events


class EventHelper:
    def __init__(self, 
            aws_region: str, 
            table_name: str, 
            workflow_instance_id: str,
        ):
        self._table = DynamoDBTableHelper(
            aws_region=aws_region,
            table_name=table_name)

        self._items = []
        self._workflow_instance_id = workflow_instance_id

    def __map_event_to_item(self, event, event_type):
        return {
            'WorkflowInstanceId': self._workflow_instance_id,
            'EventId': str(uuid.uuid4()),
            'EventTypeId': event_type.get('id', ''),
            'EventTypeName': event_type.get('name', ''),
            'FunctionInput': event.get('function_input', ''),
            'Name': event.get('name', ''),
            'Result': event.get('result', ''),
            'Timestamp': int(time.time_ns() / 1000) # UNIX timestamp millisecond precision
        }
    
    def get_events_by_id(self, instance_id):
        return self._table.query(
                partition_key_name='WorkflowInstanceId',
                partition_key_value=instance_id
            )

    def write_events_batch(self):
        self._table.batch_write(items=self._items)
        self._items = []

    def start_execution(self, name):
        event_data = {
            'name': name,
        }
        self._items.append(self.__map_event_to_item(event=event_data, event_type=events.EXECUTION_STARTED))

    def complete_execution(self, result):
        event_data = {
            'result': result,
        }
        self._items.append(self.__map_event_to_item(event=event_data, event_type=events.EXECUTION_COMPLETED))

    def start_orchestrator(self):
        event_data = {}
        self._items.append(self.__map_event_to_item(event=event_data, event_type=events.ORCHESTRATOR_STARTED))

    def complete_orchestrator(self):
        event_data = {}
        self._items.append(self.__map_event_to_item(event=event_data, event_type=events.ORCHESTRATOR_COMPLETED))

    def schedule_function(self, name):
        event_data = {
            'name': name,
        }
        self._items.append(self.__map_event_to_item(event=event_data, event_type=events.FUNCTION_SCHEDULED))

    def complete_function(self, function_input, result, name):
        event_data = {
            'function_input': function_input,
            'result': result,
            'name': name
        }
        self._items.append(self.__map_event_to_item(event=event_data, event_type=events.FUNCTION_COMPLETED))
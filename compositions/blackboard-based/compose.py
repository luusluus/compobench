import os
import pytz
from datetime import datetime
from dynamodb import DynamoDBTableHelper, NoItemException

from aws_xray_sdk.core import xray_recorder

def compose(event, business_logic_function):
    print(os.environ.get('_X_AMZN_TRACE_ID'))
    workflow_instance_id = event['workflow_instance_id']
    workflow_id = event['workflow_id']
    step_id = event['step_id']
    previous_step_id = event['previous_step_id']

    workflow_execution_table = DynamoDBTableHelper(
        aws_region=os.environ['AWS_REGION'],
        table_name=os.environ['EXECUTION_TABLE'])

    read_key = {
        'WorkflowInstanceId': workflow_instance_id,
        'StepId': int(previous_step_id)
    }
    try:
        previous_step = workflow_execution_table.get_item(key=read_key)
        step_input = previous_step['Input']
        step_output = previous_step['Output']
    except NoItemException:
        print('key not found')
        step_input = step_output = {
            'result': ''
        }

    subsegment = xray_recorder.begin_subsegment('Business Logic')
    result = business_logic_function(step_output['result'])
    subsegment.put_annotation('workflow_instance_id', workflow_instance_id)
    xray_recorder.end_subsegment()
    
    output_item = {
        'result': result
    }
    item = {
        'WorkflowInstanceId': workflow_instance_id,
        'WorkflowId': workflow_id,
        'StepId': step_id,
        'Input': step_output,
        'Output': output_item,
        'Timestamp': datetime.now().astimezone().replace(microsecond=0, tzinfo=pytz.utc).isoformat()
    }
    workflow_execution_table.put_item(item=item)
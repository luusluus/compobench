import os

from aws_xray_sdk.core import xray_recorder

from event_helper import EventHelper

def compose(event, business_logic_function):
    workflow_instance_id = event['workflow_instance_id']
    function_input = event['input']

    subsegment = xray_recorder.begin_subsegment('Business Logic')
    result = business_logic_function(function_input)
    subsegment.put_annotation('workflow_instance_id', event['workflow_instance_id'])
    xray_recorder.end_subsegment()

    eventhelper = EventHelper(
        aws_region=os.environ['AWS_REGION'], 
        table_name=os.environ['EVENT_HISTORY_TABLE'],
        workflow_instance_id=workflow_instance_id)

    eventhelper.complete_function(
        function_input=function_input, 
        result=result, 
        name=os.environ['AWS_LAMBDA_FUNCTION_NAME']
    )
    eventhelper.write_events_batch()
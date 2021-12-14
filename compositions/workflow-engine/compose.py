from aws_xray_sdk.core import xray_recorder

def compose(event, business_logic_function):
    workflow_instance_id = event['workflow_instance_id']
    subsegment = xray_recorder.begin_subsegment('Identification')
    result = business_logic_function(event['result'])
    subsegment.put_annotation('workflow_instance_id', workflow_instance_id)
    xray_recorder.end_subsegment()

    return {
        'result': result,
        'workflow_instance_id': workflow_instance_id
    }
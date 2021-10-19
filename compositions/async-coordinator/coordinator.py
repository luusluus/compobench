
import os
from compose import compose
from s3 import S3BucketHelper

def lambda_handler(event, context):
    # always in payload
    workflow_id = event['workflow_id']

    object_key = workflow_id + '.json'

    # read workflow state from S3 using workflow_id
    bucket_name = os.environ['BUCKET_NAME']
    s3_bucket_helper = S3BucketHelper(aws_region=os.environ['AWS_REGION'])
    try:
        workflow_state = s3_bucket_helper.get_object_from_bucket(bucket_name=bucket_name, object_key=object_key)
        workflow = workflow_state['workflow']
        prev_invoked_function = workflow_state['prev_invoked_function']
        current_result = workflow_state['current_result']

        # concat the string result
        new_result = current_result + event['result']
    except Exception as e:
        # NoSuchKey Exception
        print(e)
        # only in initial invocation by client
        workflow = event['workflow']
        print(workflow)
        new_result = ''
        prev_invoked_function = ''

    if prev_invoked_function == workflow[-1]:
        # end of workflow
        s3_bucket_helper.write_json_to_bucket(
            bucket_name=bucket_name,
            json_object={'result': new_result}, 
            object_key = 'result.json')
    else:
        # continue workflow
        # determine next function
        try:
            index = workflow.index(prev_invoked_function)
            function_name = workflow[index + 1]
        except ValueError:
            function_name = workflow[0]

        new_workflow_state = {
            'workflow': workflow,
            'prev_invoked_function': function_name,
            'current_result': new_result
        }
        s3_bucket_helper.write_json_to_bucket(bucket_name=bucket_name, json_object=new_workflow_state, object_key=object_key)
        compose(function_name=function_name, data={
            'workflow_id': workflow_id
        })
    
    # { 'workflow': [{'function': 'FunctionA', 'state': 'finished', ....}]}
    # { 'workflow': ['FunctionA', 'FunctionB'], 'prev_function': 'FunctionA', 'payload': '....' }



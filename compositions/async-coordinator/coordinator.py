import os

from botocore.exceptions import ClientError

from aws_lambda import LambdaHelper
from s3 import S3BucketHelper

class Coordinator:
    def __init__(self, workflow_instance_id, workflow_data={}):
        self._lambda_helper = LambdaHelper(aws_region=os.environ['AWS_REGION'])
        self._s3_bucket_helper = S3BucketHelper(aws_region=os.environ['AWS_REGION'])
        self._bucket_name = os.environ['BUCKET_NAME']
        self._workflow_instance_id = workflow_instance_id


    def __schedule_next_function(self, function_name, workflow_state):
        self._lambda_helper.invoke_lambda_async(
            function_name=function_name, 
            payload=workflow_state)

    def is_end_workflow(self, event):
        if event.get('prev_invoked_function') == event['workflow'][-1]:
            # end of workflow

            self._s3_bucket_helper.write_json_to_bucket(
                bucket_name=self._bucket_name,
                json_object={'result': event.get('result')}, 
                object_key = f'result_{self._workflow_instance_id}.json')

            return True
        return False


    def determine_next_step(self, event):
        print(event)
        workflow = event['workflow']
        try:
            index = workflow.index(event.get('prev_invoked_function'))
            function_name = workflow[index + 1]
        except ValueError:
            function_name = workflow[0]

        workflow_instance_id = event['workflow_instance_id']

        new_workflow_state = {
            'workflow_instance_id': workflow_instance_id,
            'workflow': event['workflow'],
            'prev_invoked_function': function_name,
            'result': event.get('result')
        }
        self.__schedule_next_function(
            workflow_state=new_workflow_state,
            function_name=function_name)
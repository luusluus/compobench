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

        self._state = self.__retrieve_workflow_state(workflow_data=workflow_data)

    def __schedule_next_function(self, function_name, function_input):
        self._lambda_helper.invoke_lambda_async(
            function_name=function_name, 
            payload={
                'workflow_instance_id': self._workflow_instance_id,
                'result': function_input
            })

    def __dump_workflow_state(self, new_workflow_state):
        self._s3_bucket_helper.write_json_to_bucket(
            bucket_name=self._bucket_name,
            json_object=new_workflow_state, 
            object_key=f'{self._workflow_instance_id}.json')

    def is_end_workflow(self, event):
        if self._state['prev_invoked_function'] == self._state['workflow'][-1]:
            # end of workflow
            current_result = self.__parse_function_result(event=event)

            self._s3_bucket_helper.write_json_to_bucket(
                bucket_name=self._bucket_name,
                json_object={'result': current_result}, 
                object_key = f'result_{self._workflow_instance_id}.json')

            return True
        return False
    
    def __parse_function_result(self, event):
        if 'input' in event:
            return event['input']
        else:
            return event['result']


    def determine_next_step(self, event):
        print(event)
        workflow = self._state['workflow']
        try:
            index = workflow.index(self._state['prev_invoked_function'])
            function_name = workflow[index + 1]
        except ValueError:
            function_name = workflow[0]

        workflow_instance_id = event['workflow_instance_id']

        current_result = self.__parse_function_result(event=event)
        new_workflow_state = {
            'workflow_instance_id': workflow_instance_id,
            'workflow': self._state['workflow'],
            'prev_invoked_function': function_name,
            'current_result': current_result
        }
        self.__dump_workflow_state(new_workflow_state=new_workflow_state)
        self.__schedule_next_function(
            function_name=function_name,
            function_input=current_result)

    def __retrieve_workflow_state(self, workflow_data):
        # read workflow state from S3 using workflow_instance_id
        try:
            return self._s3_bucket_helper.get_object_from_bucket(
                bucket_name=self._bucket_name, 
                object_key=f'{self._workflow_instance_id}.json')

        except ClientError as e:
            # NoSuchKey Exception
            if e.response['Error']['Code'] == 'NoSuchKey':
                return {
                    'workflow': workflow_data['workflow'],
                    'prev_invoked_function': '',
                    'current_result': workflow_data['input']
                }
            else:
                raise
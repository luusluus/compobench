import json

from boto3 import client as boto3_client

from .WorkflowExecutor import WorkflowExecutor

class LambdaInvocationType:
    Synchronous = 'RequestResponse'
    Asynchronous = 'Event'

class FunctionWorkflowExecutor(WorkflowExecutor):
    def __init__(
        self,
        payload: dict,
        lambda_invocation_type: LambdaInvocationType,
        first_function_name: str,
    ):
        super().__init__(payload=payload)
        self.lambda_invocation_type = lambda_invocation_type
        self.first_function_name = first_function_name
        self.lambda_client = boto3_client('lambda', region_name='eu-central-1')

    def start(self):
        response = self.lambda_client.invoke(
            FunctionName=self.first_function_name,
            InvocationType=self.lambda_invocation_type,
            Payload=json.dumps(self._payload)
        )

        if response['StatusCode'] == 200:
            result = json.load(response['Payload'])
            if 'result' in result:
                print(result['result'])
            else:
                print(result)

        elif response['StatusCode'] == 202:
            print(response)
        else:
            print('Something wrong')
            print(response)
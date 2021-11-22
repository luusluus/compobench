from datetime import datetime, timedelta, timezone
import json
import time
import uuid

from boto3 import client as boto3_client

from XRayClient import XRayClient
from ExperimentData import ExperimentData, InvocationType

class OverheadExperiment:
    def __init__(self, experiment_data: ExperimentData):
        aws_region = 'eu-central-1'
        self._lambda_client = boto3_client('lambda', region_name=aws_region)
        self._experiment_data = experiment_data

        self._xray_client = XRayClient()

        self._workflow_ids = []

    def invoke_lambda(self, invocation_type, function_name, payload):
        response = self._lambda_client.invoke(
            FunctionName=function_name,
            InvocationType=invocation_type,
            Payload=json.dumps(payload)
        )

        if response['StatusCode'] == 200:
            result = json.load(response['Payload'])
            if 'result' in result:
                print(result['result'])
            else:
                print(result)
        else:
            print('Something wrong')
            print(response)

    def start(self):
        print(f'starting experiment: {self._experiment_data.name}')
        start = datetime.utcnow()
        print(start)
            
        for i in range(self._experiment_data.amount_of_workflows):
            workflow_id = str(uuid.uuid4())
            self._workflow_ids.append(workflow_id)
            print(f'workflow id: {workflow_id}')
            self._experiment_data.payload['workflow_id'] = workflow_id
            self.invoke_lambda(
                function_name=self._experiment_data.first_function_name,
                payload=self._experiment_data.payload,
                invocation_type=self._experiment_data.invocation_type)

        end = datetime.utcnow()
        print(end)
        # wait until all traces appear in XRay API
        time.sleep(10)
        # Correct for minute drift between my local machine and XRay API
        self.process_results(
            start=start - timedelta(minutes=1), 
            end=end + timedelta(minutes=2))

    def process_results(self, start, end):
        traces = self._xray_client.batch_get_traces(
            start=start, 
            end=end
        )

        # print(f'fetched {len(traces)} traces')

        self._experiment_data.parser.parse(traces=traces)

    def get_results(self, is_dataframe: bool):
        if is_dataframe:
            return self._experiment_data.parser.get_aggregate_results_df()
        else:
            return self._experiment_data.parser.get_all_results()

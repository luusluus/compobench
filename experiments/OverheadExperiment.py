from datetime import datetime, timedelta, timezone
import json
import time
import uuid

from boto3 import client as boto3_client

from XRayWrapper import XRayWrapper
from ExperimentData import ExperimentData
from executors.FunctionWorkflowExecutor import FunctionWorkflowExecutor, LambdaInvocationType

class OverheadExperiment:
    def __init__(self, experiment_data: ExperimentData):
        aws_region = 'eu-central-1'
        self._lambda_client = boto3_client('lambda', region_name=aws_region)
        self._experiment_data = experiment_data

        self._xray_wrapper = XRayWrapper()

        self._workflow_instance_ids = []

    def start(self):
        print(f'starting experiment: {self._experiment_data.name}')
        start = datetime.utcnow()
        for i in range(self._experiment_data.amount_of_workflows):
            workflow_instance_id = str(uuid.uuid4())
            self._workflow_instance_ids.append(workflow_instance_id)
            print(f'workflow id: {workflow_instance_id}')
            payload = self._experiment_data.workflow_executor.payload
            payload['workflow_instance_id'] = workflow_instance_id
            self._experiment_data.workflow_executor.payload = payload

            self._experiment_data.workflow_executor.start()

        end = datetime.utcnow()
        # wait until all traces appear in XRay API
        time.sleep(20)
        # Correct for minute drift between my local machine and XRay API
        self.process_results(
            start=start - timedelta(minutes=3), 
            end=end + timedelta(minutes=3))

    def process_results(self, start, end):
        traces = self._xray_wrapper.batch_get_traces(
            start=start, 
            end=end,
            workflow_instance_ids=self._workflow_instance_ids
        )
        is_sync = False
        if isinstance(self._experiment_data.workflow_executor, FunctionWorkflowExecutor):
            lambda_invocation_type = getattr(self._experiment_data.workflow_executor, 'lambda_invocation_type')
            if lambda_invocation_type == LambdaInvocationType.Synchronous:
                is_sync = True

        self._experiment_data.parser.parse(
            traces=traces,
            is_sync=is_sync
        )

    def get_results(self, is_dataframe: bool):
        if is_dataframe:
            return self._experiment_data.parser.get_aggregate_results_df()
        else:
            return self._experiment_data.parser.get_all_results()

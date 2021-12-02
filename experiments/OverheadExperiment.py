from datetime import datetime, timedelta, timezone
import json
import time
import uuid

import pandas as pd

from boto3 import client as boto3_client

from XRayWrapper import XRayWrapper
from ExperimentData import ExperimentData
from executors.FunctionWorkflowExecutor import FunctionWorkflowExecutor

class OverheadExperiment:
    def __init__(self, experiment_data: ExperimentData):
        aws_region = 'eu-central-1'
        self._lambda_client = boto3_client('lambda', region_name=aws_region)
        self._experiment_data = experiment_data

        self._xray_wrapper = XRayWrapper()

        self._results = pd.DataFrame()

    def start(self):
        is_sync = False
        # if isinstance(self._experiment_data.workflow_executor, FunctionWorkflowExecutor):
        #     lambda_invocation_type = getattr(self._experiment_data.workflow_executor, 'lambda_invocation_type')
        #     if lambda_invocation_type == LambdaInvocationType.Synchronous:
        #         is_sync = True
        cold_start = True
        for i in range(self._experiment_data.repetitions):
            if i == 1:
                cold_start = False

            print(f'Starting experiment: {self._experiment_data.name}. Repetition: {i + 1}')
            workflow_instance_ids = []
            start = datetime.utcnow()
            for i in range(self._experiment_data.amount_of_workflows):
                workflow_instance_id = str(uuid.uuid4())
                workflow_instance_ids.append(workflow_instance_id)

                executor = self._experiment_data.workflow_executor(self._experiment_data.name, workflow_instance_id)
                executor.start()
                executor_config = executor.config
                if executor_config.get('lambda_invocation_type') == 'SYNC':
                    is_sync = True

                # time.sleep(0.01)

            end = datetime.utcnow()
            # wait until all traces appear in XRay API
            time.sleep(20)
            # Correct for minute drift between my local machine and XRay API

            result_df = self.process_results(
                start=start - timedelta(minutes=3), 
                end=end + timedelta(minutes=3),
                workflow_instance_ids=workflow_instance_ids,
                cold_start=cold_start,
                is_sync=is_sync)
            
            self._results = self._results.append(result_df)

            # Wait until next repetition
            time.sleep(1)

    def process_results(self, start, end, workflow_instance_ids, cold_start, is_sync):
        traces = self._xray_wrapper.batch_get_traces(
            start=start, 
            end=end,
            workflow_instance_ids=workflow_instance_ids
        )

        self._experiment_data.parser.parse(
            traces=traces,
            is_sync=is_sync
        )

        results = self._experiment_data.parser.get_aggregate_results_df(cold_start=cold_start)
        self._experiment_data.parser.reset()
        return results

    def get_results(self):
        return self._results.reset_index(drop=True)
        # if is_dataframe:
        #     return self._experiment_data.parser.get_aggregate_results_df()
        # else:
        #     return self._experiment_data.parser.get_all_results()

    def get_experiment_name(self):
        return self._experiment_data.name
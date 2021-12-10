from datetime import datetime, timedelta, timezone
import json
import time
import uuid
import subprocess
import json
import uuid

import boto3
import pandas as pd

from aws_auth import AWSRequestsAuth
from experiments.XRayWrapper import XRayWrapper
from experiments.ExperimentData import ThroughputExperimentData

class ThroughputExperiment:
    def __init__(self, experiment_data: ThroughputExperimentData):
        self._xray_wrapper = XRayWrapper()

        self._experiment_data = experiment_data

        self._results = pd.DataFrame()

    def start(self):
        executor = self._experiment_data.workflow_executor(self._experiment_data.name)
        workload = executor.get_workload()
        for load in workload:
            # warm-up phase
            # executor = self._experiment_data.workflow_executor(self._experiment_data.name)

            # executor.start(
            #     concurrent_workers=load['concurrent_workers'],
            #     duration='10s',
            #     rate_limit=-1
            # )

            # start throughput measurement
            start = datetime.utcnow()

            executor.start(
                concurrent_workers=load['concurrent_workers'],
                duration='10s',
                rate_limit=-1
            )

            end = datetime.utcnow() + timedelta(seconds=10)

            print(start)
            print(end)
            # wait until all traces appear in XRay API
            time.sleep(20)

            trace_summaries = self._xray_wrapper.get_trace_summaries(start=start, end=end)

            result_df = self.process_results(trace_summaries=trace_summaries, rps=load['rps'])

            self._results = self._results.append(result_df)

    def process_results(self, trace_summaries, rps):
        filtered_summaries = []
        for trace_summary in trace_summaries:
            if 'Duration' in trace_summary:
                filtered_summaries.append({
                    'Id': trace_summary['Id'],
                    'Duration': trace_summary['Duration'],
                    'HasFault': trace_summary['HasFault'],
                    'HasError': trace_summary['HasError'],
                    'HasThrottle': trace_summary['HasThrottle'],
                    'RPS': rps
                })

        return pd.DataFrame(filtered_summaries)

    def get_results(self):
        return self._results.reset_index(drop=True)

    def get_experiment_name(self):
        return self._experiment_data.name
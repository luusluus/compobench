from datetime import datetime, timedelta, timezone
from io import StringIO
import time
import subprocess

import boto3
import pandas as pd

from ExperimentData import ThroughputExperimentData
from CloudWatch import CloudWatch

class ThroughputExperiment:
    def __init__(self, experiment_data: ThroughputExperimentData):
        self._experiment_data = experiment_data
        self._cloudwatch = CloudWatch()
        self._hey_results = pd.DataFrame()
        self._aws_results = pd.DataFrame()

    def start(self):
        executor = self._experiment_data.workflow_executor(self._experiment_data.name)
        workload = executor.get_workload()
        for load in workload:
            print(f'composition: {self._experiment_data.name}')
            print(f'RPS: {load["rps"]}')
            print()
            # warm-up phase
            print('warm up phase')
            print()
            executor.start(
                concurrent_workers=load['concurrent_workers'],
                rate_limit=-1
            )

            print('sleep 60 sec')
            time.sleep(60)
            # start throughput measurement
            print()
            print('measurement phase')
            
            start = datetime.utcnow()
            output = executor.start(
                concurrent_workers=load['concurrent_workers'],
                rate_limit=-1
            )

            end = datetime.utcnow() + timedelta(minutes=1)
            start = start - timedelta(minutes=2)
            print(start)
            print(end)

            print('sleep 90 sec')
            time.sleep(90)
            self.process_aws_results(rps=load['rps'], start=start, end=end)
            self.process_hey_results(output=output, rps=load['rps'])

    def process_hey_results(self, output, rps):
        df = pd.read_csv(StringIO(output))
        df['composition'] = self._experiment_data.name
        df['rps'] = rps

        self._hey_results = self._hey_results.append(df)

    def get_hey_results(self):
        return self._hey_results.reset_index(drop=True)

    def process_aws_results(self, rps, start, end):
        print('get statistics from cloudwatch')
        print(start)
        print(end)
        error_count = self._cloudwatch.get_statistics(metric_name='Errors', start=start, end=end)
        invocation_count = self._cloudwatch.get_statistics(metric_name='Invocations', start=start, end=end)
        throttle_count = self._cloudwatch.get_statistics(metric_name='Throttles', start=start, end=end)

        if invocation_count > 0:
            error_rate = error_count / invocation_count
        else:
            error_rate = 0
        df = pd.DataFrame({
            'error_count': [error_count],
            'error_rate': [error_rate],
            'invocation_count': [invocation_count],
            'throttle_count': [throttle_count],
            'rps': rps,
            'composition': self._experiment_data.name
        })

        self._aws_results = self._aws_results.append(df)

    def get_aws_results(self):
        return self._aws_results.reset_index(drop=True)

    def get_experiment_name(self):
        return self._experiment_data.name
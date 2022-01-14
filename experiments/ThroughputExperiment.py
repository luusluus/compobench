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
            rps = load["concurrent_workers"]
            print(f'composition: {self._experiment_data.name}')
            print(f'RPS: {rps}')
            print()
            # warm-up phase
            print('warm up phase')
            print()
            print(f'start: {datetime.now(timezone.utc)}')
            executor.start(
                concurrent_workers=load['concurrent_workers'],
                rate_limit=-1
            )
            print(f'end: {datetime.now(timezone.utc)}')

            print('sleep 180 sec')
            time.sleep(180)
            # start throughput measurement
            print()
            print('measurement phase')
            
            start = datetime.now(timezone.utc)
            print(f'start: {start}')
            output = executor.start(
                concurrent_workers=load['concurrent_workers'],
                rate_limit=-1
            )
            end = datetime.now(timezone.utc) + timedelta(minutes=1)
            print(f'end: {end}')
            start = start - timedelta(seconds=120) # 2 min

            print()
            print('wait time between next throughput round')
            print('sleep 180 sec')
            time.sleep(180)
            self.process_aws_results(rps=rps, start=start, end=end)
            self.process_hey_results(output=output, rps=rps)

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
        period=60
        statistic = 'Sum'
        error_count = self._cloudwatch.get_statistics(
            metric_name='Errors',
            statistic=statistic,
            period=period,
            start=start, 
            end=end)

        invocation_count = self._cloudwatch.get_statistics(
            metric_name='Invocations', 
            statistic=statistic,
            period=period,
            start=start, 
            end=end
            )

        throttle_count = self._cloudwatch.get_statistics(
            metric_name='Throttles', 
            statistic=statistic,
            period=period,
            start=start, 
            end=end)

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
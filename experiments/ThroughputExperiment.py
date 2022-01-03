from datetime import datetime, timedelta, timezone
from io import StringIO
import time
import subprocess

import boto3
import pandas as pd

from ExperimentData import ThroughputExperimentData

class ThroughputExperiment:
    def __init__(self, experiment_data: ThroughputExperimentData):
        self._experiment_data = experiment_data

        self._results = pd.DataFrame()

    def start(self):
        executor = self._experiment_data.workflow_executor(self._experiment_data.name)
        workload = executor.get_workload()
        for load in workload:
            print(f'composition: {self._experiment_data.name}')
            # warm-up phase
            executor = self._experiment_data.workflow_executor(self._experiment_data.name)
            print('warm up phase')
            executor.start(
                concurrent_workers=load['concurrent_workers'],
                rate_limit=-1
            )

            time.sleep(10)
            # start throughput measurement
            print('measurement phase')
            print(f'RPS: {load["rps"]}')
            # start = datetime.utcnow()

            output = executor.start(
                concurrent_workers=load['concurrent_workers'],
                rate_limit=-1
            )

            # end = datetime.utcnow() + timedelta(seconds=10)

            result_df = self.process_results(output=output, rps=load['rps'])
            self._results = self._results.append(result_df)

    def process_results(self, output, rps):
        df = pd.read_csv(StringIO(output))
        df['composition'] = self._experiment_data.name
        df['rps'] = rps
        print(df.to_string())

        return df

    def get_results(self):
        return self._results.reset_index(drop=True)

    def get_experiment_name(self):
        return self._experiment_data.name
from abc import ABC, abstractmethod
import pathlib
import json
import subprocess

import boto3
from aws_auth import AWSRequestsAuth

class WorkflowExecutor(ABC):
    def __init__(self, experiment_name: str):
        self.config = self.read_from_config()
        self.workflow_config = self.config['compositions'][experiment_name]

        credentials = boto3.Session().get_credentials()

        self.auth = AWSRequestsAuth(
            aws_access_key=credentials.access_key,
            aws_secret_access_key=credentials.secret_key,
            aws_host='lambda.eu-central-1.amazonaws.com',
            aws_region='eu-central-1',
            aws_service='lambda')


    @abstractmethod
    def start(self, concurrent_workers, duration, rate_limit):
        pass


    def get_workload(self):
        return self.config['rps']
        
    def execute_hey(self, hey_command):
        process = subprocess.Popen(hey_command, stdout=subprocess.PIPE)

        output, error = process.communicate()
        return output.decode('utf-8')

    def build_hey_command(self, url, payload, concurrent_workers, duration, rate_limit):
        headers = self.auth.get_aws_request_headers(
            url=url, 
            payload=json.dumps(payload),
            method='POST'
        )

        hey_command = [
            'hey',
            '-c',
            str(concurrent_workers),
            '-z',
            duration,
        ]
        if rate_limit != -1:
            hey_command.append('-q')
            hey_command.append(str(rate_limit))

        hey_command.extend([
            '-m',
            'POST',
            '-o',
            'csv',
            '-d',
            json.dumps(payload)
        ])
        for key, value in headers.items():
            hey_command.append('-H')
            hey_command.append(f'{key}: {value}')

        hey_command.append(url)
        return hey_command

    def read_from_config(self):
        with open(f'{pathlib.Path(__file__).parent.resolve()}/config.json') as json_file:
            config = json.load(json_file)
            return config

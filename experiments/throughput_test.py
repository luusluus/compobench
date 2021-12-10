import subprocess
from aws_auth import AWSRequestsAuth
import json
import boto3
import uuid


session = boto3.Session()
credentials = session.get_credentials()
access_key = credentials.access_key
secret_key = credentials.secret_key

function_name = 'AsyncSequenceFunctionA'
payload = {
    'result': '',
    'workflow_instance_id': str(uuid.uuid4())
}

auth = AWSRequestsAuth(aws_access_key=access_key,
                       aws_secret_access_key=secret_key,
                       aws_host='lambda.eu-central-1.amazonaws.com',
                       aws_region='eu-central-1',
                       aws_service='lambda')

url = f'https://lambda.eu-central-1.amazonaws.com/2015-03-31/functions/{function_name}/invocations'
headers = auth.get_aws_request_headers(
    url=url, 
    payload=json.dumps(payload),
    method='POST')

# print(headers)

hey_command = [
    'hey',
    '-c',
    '10',
    '-z',
    '10s',
    '-q',
    '1',
    '-m',
    'POST',
    # '-o',
    # 'csv',
    '-d',
    json.dumps(payload)
]
for key, value in headers.items():
    hey_command.append('-H')
    hey_command.append(f'{key}: {value}')

hey_command.append(url)
# print(' '.join(hey_command))
process = subprocess.Popen(hey_command, stdout=subprocess.PIPE)

output, error = process.communicate()

print(output.decode('utf-8'))
f = open('./out.csv', 'wb')
f.write(output)
f.close()
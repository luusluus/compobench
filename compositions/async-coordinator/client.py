

import json
import uuid
from boto3 import client as boto3_client
from compositions.aws_helpers.s3 import S3BucketHelper


aws_region = 'eu-central-1'
bucket_name = 'async-coordinator-store'
result_key = 'result.json'

client = boto3_client('lambda', region_name=aws_region)

workflow_id = str(uuid.uuid4())
payload = {
    'workflow': ['AsyncCoordinatorFunctionA', 'AsyncCoordinatorFunctionB', 'AsyncCoordinatorFunctionC'],
    'workflow_id': workflow_id
}

# call the first function a to start the workflow
response = client.invoke(
    FunctionName='AsyncCoordinatorFunctionCoordinator',
    InvocationType='Event',
    Payload=json.dumps(payload)
)

if response['StatusCode'] == 202:
    s3_bucket_helper = S3BucketHelper(aws_region=aws_region)

    s3_bucket_helper.poll_object_from_bucket(bucket_name=bucket_name, object_key=result_key)

    response = s3_bucket_helper.get_object_from_bucket(bucket_name=bucket_name, object_key=result_key)
    print(response['result'])

    s3_bucket_helper.delete_object_from_bucket(bucket_name=bucket_name, object_key=result_key)

    # delete coordinator state file
    coordinator_state_file = workflow_id + '.json'
    s3_bucket_helper.delete_object_from_bucket(bucket_name=bucket_name, object_key=coordinator_state_file)
else:
    print('Composition Failed')



import os

from aws_xray_sdk.core import xray_recorder

from aws_lambda import LambdaHelper
from s3 import S3BucketHelper

def compose(event, business_logic_function):
    workflow_instance_id = event['workflow_instance_id']
    subsegment = xray_recorder.begin_subsegment('Business Logic')
    result = business_logic_function(event['result'])
    subsegment.put_annotation('workflow_instance_id', workflow_instance_id)
    xray_recorder.end_subsegment()
    
    payload = {
        'result': result,
        'workflow_instance_id': workflow_instance_id
    }

    aws_region = os.environ['AWS_REGION']
    if isinstance(event['composition'], list) and len(event['composition']) > 0:
        function_name = event['composition'].pop(0)

        payload['composition'] = event['composition']
        lambda_helper = LambdaHelper(aws_region=aws_region)
        lambda_helper.invoke_lambda_async(
            function_name=function_name,
            payload=payload
        )
    else:
        bucket_name = os.environ['BUCKET_NAME']
        s3_bucket_helper = S3BucketHelper(aws_region=aws_region)

        print(f'Saving final result: {result} to {bucket_name}')

        s3_bucket_helper.write_json_to_bucket(
            bucket_name=bucket_name,
            json_object=payload, 
            object_key='result.json')

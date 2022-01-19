import os

from aws_xray_sdk.core import xray_recorder

from aws_lambda import LambdaHelper
from s3 import S3BucketHelper

def compose(event, function_name, business_logic_function):
    workflow_instance_id = event['workflow_instance_id']
    subsegment = xray_recorder.begin_subsegment('Identification')
    result = business_logic_function(event['result'])
    subsegment.put_annotation('workflow_instance_id', workflow_instance_id)
    xray_recorder.end_subsegment()
    
    payload = {
        'result': result,
        'workflow_instance_id': workflow_instance_id
    }
    if function_name == '':
        bucket_name = os.environ['BUCKET_NAME']
        s3_bucket_helper = S3BucketHelper(aws_region=os.environ['AWS_REGION'])
        
        print(f'Saving final result: {payload["result"]} to {bucket_name}')
        s3_bucket_helper.write_json_to_bucket(
            bucket_name=bucket_name,
            json_object=payload, 
            object_key='result.json')
    else:
        aws_region = os.environ['AWS_REGION']

        lambda_helper = LambdaHelper(aws_region=aws_region)
        lambda_helper.invoke_lambda_async(
            function_name=function_name, 
            payload=payload)
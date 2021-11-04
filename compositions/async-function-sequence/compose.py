import os

from aws_lambda import LambdaHelper
from s3 import S3BucketHelper

def compose(event, function_name, business_logic_function):
    result = business_logic_function(event)
    if function_name == '':
        bucket_name = os.environ['BUCKET_NAME']
        s3_bucket_helper = S3BucketHelper(aws_region=os.environ['AWS_REGION'])
        
        print(f'Saving final result: {result} to {bucket_name}')
        s3_bucket_helper.write_json_to_bucket(
            bucket_name=bucket_name,
            json_object=result, 
            object_key='result.json')
    else:
        aws_region = os.environ['AWS_REGION']

        lambda_helper = LambdaHelper(aws_region=aws_region)
        lambda_helper.invoke_lambda_async(
            function_name=function_name, 
            payload=result)
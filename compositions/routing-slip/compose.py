import os
from aws_lambda import LambdaHelper
from s3 import S3BucketHelper

def compose(event, business_logic_function):
    result = business_logic_function(event)
    aws_region = os.environ['AWS_REGION']
    if isinstance(event['composition'], list) and len(event['composition']) > 0:
        function_name = event['composition'].pop(0)

        result['composition'] = event['composition']
        lambda_helper = LambdaHelper(aws_region=aws_region)
        lambda_helper.invoke_lambda(
            function_name=function_name,
            payload=result
        )
    else:
        bucket_name = os.environ['BUCKET_NAME']
        s3_bucket_helper = S3BucketHelper(aws_region=aws_region)

        print(f'Saving final result: {result} to {bucket_name}')

        s3_bucket_helper.write_json_to_bucket(
            bucket_name=bucket_name,
            json_object=result, 
            object_key='result.json')

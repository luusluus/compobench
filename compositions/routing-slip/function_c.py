import os
from compose import compose
# import layer
from s3 import S3BucketHelper

def lambda_handler(event, context):
    function_name = os.path.basename(__file__).split('.')[0]
    event['greet'] = event['greet'] + f'Hello world from {function_name}. '
    print(event['greet'])

    bucket_name = os.environ['BUCKET_NAME']
    s3_bucket_helper = S3BucketHelper(aws_region=os.environ['AWS_REGION'])

    s3_bucket_helper.write_json_to_bucket(
        bucket_name=bucket_name,
        json_object={'result': event['greet']}, 
        object_key = 'result_c.json')
    
    return {
        'statusCode': 200
    }
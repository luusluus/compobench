import os
from publish import publish
from s3 import S3BucketHelper

def lambda_handler(event, context):
    sns = event['Records'][0]['Sns']
    message = sns['Message']
    timestamp = sns['Timestamp']
    function_name = os.path.basename(__file__).split('.')[0]
    message += f'Hello world from {function_name}. '

    bucket_name = os.environ['BUCKET_NAME']
    s3_bucket_helper = S3BucketHelper(aws_region=os.environ['AWS_REGION'])

    s3_bucket_helper.write_json_to_bucket(
        bucket_name=bucket_name,
        json_object={'result': message}, 
        object_key = 'result.json')
    
    return {
        'statusCode': 200
    }
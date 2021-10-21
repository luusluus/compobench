import os
from s3 import S3BucketHelper

def compose(event, business_logic_function):
    s3_record = event['Records'][0]['s3']
    bucket_name = s3_record['bucket']['name']
    object_key = s3_record['object']['key']

    s3_bucket_helper = S3BucketHelper(aws_region=os.environ['AWS_REGION'])

    s3_object = s3_bucket_helper.get_object_from_bucket(bucket_name=bucket_name, object_key=object_key)

    result = business_logic_function(s3_object['result'])

    workflow = s3_object['workflow']
    if len(workflow) == 0:
        result_key = 'result.json'
    else:
        next_function_name = workflow.pop(0)
        result_key = f'{next_function_name}_result.json'

    s3_bucket_helper.write_json_to_bucket(
        bucket_name=bucket_name,
        json_object={
            'result': result,
            'workflow': workflow
        }, 
        object_key = result_key)
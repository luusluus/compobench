import os
import time

from s3 import S3BucketHelper

def compose(event):
    s3_record = event['Records'][0]['s3']
    bucket_name = s3_record['bucket']['name']
    object_key = s3_record['object']['key']

    s3_bucket_helper = S3BucketHelper(aws_region=os.environ['AWS_REGION'])

    s3_object = s3_bucket_helper.get_object_from_bucket(bucket_name=bucket_name, object_key=object_key)

    workflow_instance_id = s3_object['workflow_instance_id']
    
    time.sleep(s3_object['sleep'])

    result_object = {
        'workflow_instance_id': workflow_instance_id,
        'sleep': s3_object['sleep']
    }

    workflow = s3_object['workflow']
    if len(workflow) == 0:
        result_key = f'results/{workflow_instance_id}.json'
    else:
        next_function_name = workflow.pop(0)
        result_key = f'{next_function_name}/{workflow_instance_id}.json'

    result_object['workflow'] = workflow
    s3_bucket_helper.write_json_to_bucket(
        bucket_name=bucket_name,
        json_object=result_object, 
        object_key=result_key)
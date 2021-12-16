import os
import json

from aws_xray_sdk.core import xray_recorder

from boto3 import client as boto3_client
from s3 import S3BucketHelper

def compose(event):
    aws_region = os.environ['AWS_REGION']
    topic_arn = os.environ['TOPIC_ARN']
    function_name = os.environ['AWS_LAMBDA_FUNCTION_NAME']
    
    sns = event['Records'][0]['Sns']
    message = json.loads(sns['Message'])

    if 'workflow_instance_id' in event:
        workflow_instance_id = event['workflow_instance_id']
    elif 'workflow_instance_id' in message:
        workflow_instance_id = message['workflow_instance_id']


    subsegment = xray_recorder.begin_subsegment('Identification')
    subsegment.put_annotation('workflow_instance_id', workflow_instance_id)
    xray_recorder.end_subsegment()
    
    message_attributes = sns['MessageAttributes']
    last_function_name = message_attributes['last_function']['Value']


    result_object = {
        'workflow_instance_id': workflow_instance_id
    }
    
    if function_name == last_function_name:
        bucket_name = os.environ['BUCKET_NAME']
        s3_bucket_helper = S3BucketHelper(aws_region=os.environ['AWS_REGION'])

        s3_bucket_helper.write_json_to_bucket(
            bucket_name=bucket_name,
            json_object=result_object, 
            object_key=f'result_{workflow_instance_id}.json')
    else:
        client = boto3_client('sns', region_name=aws_region)
        client.publish(
            Message=json.dumps(result_object),
            MessageAttributes={
                'caller': {
                    'DataType': 'String',
                    'StringValue': function_name
                },
                'last_function':{
                    'DataType': 'String',
                    'StringValue': last_function_name
                }
            },
            TopicArn=topic_arn)

    
    
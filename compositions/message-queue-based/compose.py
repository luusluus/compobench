import os
import json

from aws_xray_sdk.core import xray_recorder

from boto3 import client as boto3_client
from s3 import S3BucketHelper

def compose(event, business_logic_function):
    aws_region = os.environ['AWS_REGION']
    topic_arn = os.environ['TOPIC_ARN']
    function_name = os.environ['AWS_LAMBDA_FUNCTION_NAME']

    sns = event['Records'][0]['Sns']
    message = json.loads(sns['Message'])

    subsegment = xray_recorder.begin_subsegment('Identification')
    result = business_logic_function(message['result'])
    subsegment.put_annotation('workflow_instance_id', message['workflow_instance_id'])
    xray_recorder.end_subsegment()
    
    message_attributes = sns['MessageAttributes']
    last_function_name = message_attributes['last_function']['Value']


    result_object = {
        'result': result,
        'workflow_instance_id': message['workflow_instance_id']
    }
    
    if function_name == last_function_name:
        bucket_name = os.environ['BUCKET_NAME']
        print(f'Saving final result: {result} to {bucket_name}')
        s3_bucket_helper = S3BucketHelper(aws_region=os.environ['AWS_REGION'])

        s3_bucket_helper.write_json_to_bucket(
            bucket_name=bucket_name,
            json_object=result_object, 
            object_key='result.json')
    else:
        print(f'Publishing message: {result} to topic {topic_arn}')
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

    
    
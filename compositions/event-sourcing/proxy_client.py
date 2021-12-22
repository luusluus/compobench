import os
import json
import uuid
import time


from aws_lambda import LambdaHelper
from dynamodb import DynamoDBHelper, DynamoDBTableHelper, NoItemException
import event_definitions

def lambda_handler(event, context):
    aws_region = os.environ['AWS_REGION']
    lambda_helper = LambdaHelper(aws_region=aws_region)

    workflow_instance_id = str(uuid.uuid4())

    print(workflow_instance_id)
    response = lambda_helper.invoke_lambda_async(
        function_name='EventSourcingOrchestrator', 
        payload={
            'input': event['input'],
            'sleep': event['sleep'],
            'workflow_instance_id': workflow_instance_id
        })

    if response['StatusCode'] == 202:
        time.sleep(event['sleep'] * 3 + 2)

        dynamodb_helper = DynamoDBHelper(aws_region=aws_region)
        tables = dynamodb_helper.list_tables()
        event_history_table = 'EventHistoryTable'
        table_name = next((table for table in tables if event_history_table in table), None)

        event_history_table_helper = DynamoDBTableHelper(aws_region=aws_region, table_name=table_name)

        retries = 1
        while retries < 30:
            try:
                items = event_history_table_helper.query(
                    partition_key_name='WorkflowInstanceId',
                    partition_key_value=workflow_instance_id
                )

                if len(items) > 0:
                    result = next((item for item in items if int(item['EventTypeId']) == event_definitions.EXECUTION_COMPLETED['id']))
                    print(result['Result'])
                    break

            except StopIteration:
                wait = 1
                print('Waiting {} secs and retry attempt: {}'.format(wait, retries))
                time.sleep(wait)
                retries += 1

        print('done')
        return
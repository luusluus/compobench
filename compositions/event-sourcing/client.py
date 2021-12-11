import uuid
from time import sleep

from compositions.aws_helpers.aws_lambda import LambdaHelper
from compositions.aws_helpers.dynamodb import DynamoDBHelper, DynamoDBTableHelper, NoItemException
import event_definitions

aws_region = 'eu-central-1'

lambda_helper = LambdaHelper(aws_region=aws_region)

# invoke controller once to start workflow
payload = {
    'input': '',
    'sleep': 2
}
lambda_helper.invoke_lambda_async(
    function_name='EventSourcingOrchestrator', 
    payload=payload)

dynamodb_helper = DynamoDBHelper(aws_region=aws_region)
tables = dynamodb_helper.list_tables()
event_history_table = 'EventHistoryTable'
table_name = next((table for table in tables if event_history_table in table), None)

event_history_table_helper = DynamoDBTableHelper(aws_region=aws_region, table_name=table_name)

# retries = 1
# while retries < 5:
#     try:
#         items = event_history_table_helper.query(
#             partition_key_name='WorkflowInstanceId',
#             partition_key_value=workflow_instance_id
#         )

#         if len(items) > 0:
#             result = next((item for item in items if int(item['EventTypeId']) == event_definitions.EXECUTION_COMPLETED['id']))
#             print(result['Result'])
#             break

#     except StopIteration:
#         wait = retries * 3
#         print('Waiting {} secs and retry attempt: {}'.format(wait, retries))
#         sleep(wait)
#         retries += 1
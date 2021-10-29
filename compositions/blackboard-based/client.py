import uuid
from time import sleep
from compositions.aws_helpers.aws_lambda import LambdaHelper
from compositions.aws_helpers.dynamodb import DynamoDBHelper, DynamoDBTableHelper, NoItemException

aws_region = 'eu-central-1'

lambda_helper = LambdaHelper(aws_region=aws_region)

# invoke controller once to start workflow
workflow_instance_id = str(uuid.uuid4())
payload = {
    'workflow_instance_id': workflow_instance_id
}
lambda_helper.invoke_lambda_async(
    function_name='BlackboardFunctionController', 
    payload=payload)


dynamodb_helper = DynamoDBHelper(aws_region=aws_region)
tables = dynamodb_helper.list_tables()

definition_table = 'BlackboardWorkflowDefinitionTable'
definition_table_name = next((table for table in tables if definition_table in table), None)

definition_table_helper = DynamoDBTableHelper(aws_region=aws_region, table_name=definition_table_name)

query_result = definition_table_helper.query(
        partition_key_name='WorkflowId',
        partition_key_value=1
    )

workflow = query_result['Items']
last_step = int(workflow[-1]['StepId'])

execution_table = 'BlackboardWorkflowExecutionTable'
execution_table_name = next((table for table in tables if execution_table in table), None)


execution_table_helper = DynamoDBTableHelper(aws_region=aws_region, table_name=execution_table_name)

retries = 1
while retries < 5:
    try:
        item = execution_table_helper.get_item(key={
                'WorkflowInstanceId': workflow_instance_id,
                'StepId': last_step
            })
        print(item['Output']['result'])
        break
    except NoItemException:
        wait = retries * 3
        print('Waiting {} secs and retry attempt: {}'.format(wait, retries))
        sleep(wait)
        retries += 1

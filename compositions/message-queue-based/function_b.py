import os
from publish import publish

def lambda_handler(event, context):
    print(event)
    sns = event['Records'][0]['Sns']
    message = sns['Message']
    print(message)
    timestamp = sns['Timestamp']
    function_name = os.path.basename(__file__).split('.')[0]
    message += f'Hello world from {function_name}. '

    caller = os.environ['AWS_LAMBDA_FUNCTION_NAME']
    print(caller)
    publish(message=message, caller=caller)
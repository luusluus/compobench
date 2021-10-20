import os
from publish import publish

def lambda_handler(event, context):
    sns = event['Records'][0]['Sns']
    print(sns)
    function_name = os.path.basename(__file__).split('.')[0]
    message = f'Hello world from {function_name}. '

    print(message)

    caller = os.environ['AWS_LAMBDA_FUNCTION_NAME']
    print(caller)
    publish(message=message, caller=caller)
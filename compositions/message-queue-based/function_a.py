import os
from publish import publish

def lambda_handler(event, context):
    sns = event['Records'][0]['Sns']
    print(sns)
    function_name = os.path.basename(__file__).split('.')[0]
    message = f'Hello world from {function_name}. '

    print(message)

    publish(message=message)
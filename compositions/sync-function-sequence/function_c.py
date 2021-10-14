
import os
from compose import compose

def lambda_handler(event, context):
    function_name = os.path.basename(__file__).split('.')[0]
    event['greet'] = event['greet'] + f'Hello world from {function_name}. '
    response = event['greet']

    return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': response
        }
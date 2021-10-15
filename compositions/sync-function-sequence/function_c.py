
import os
import json
from compose import compose

def lambda_handler(event, context):
    function_name = os.path.basename(__file__).split('.')[0]
    event['greet'] = event['greet'] + f'Hello world from {function_name}. '
    print(event['greet'])
    return {'result': event['greet']}
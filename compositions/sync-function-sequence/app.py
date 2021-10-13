import json

from compose import compose

def return_message(message, status_code: int = 200):
    return {
        'statusCode': status_code,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(message)
    }

def a(event, context):
    data = {
        'greet': f'Hello world from {a.__name__}. ' 
    }
    response = compose(function_name='SequenceFunctionB', data=data)
    return return_message(message=response)

def b(event, context):
    event['greet'] = event['greet'] + f'Hello world from {b.__name__}. '
    response = compose(function_name='SequenceFunctionC', data=event)
    return return_message(message=response)

def c(event, context):
    event['greet'] = event['greet'] + f'Hello world from {c.__name__}. '
    response = event['greet']
    return return_message(message=response)

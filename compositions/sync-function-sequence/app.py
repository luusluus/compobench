import json

from compose import compose

def return_message(message, status_code: int = 200):
    return {
        'statusCode': status_code,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(message)
    }

def a(event, context):
    data = {}
    response = compose(function_name='FunctionB', data=data)
    response = response + f'Hello world from {a.__name__}. ' 
    return return_message(message=response)

def b(event, context):
    response = compose(function_name='FunctionC', data=event)
    response = response + f'Hello world from {b.__name__}. ' 
    return return_message(message=response)

def c(event, context):
    response = f'Hello world from {c.__name__}. '
    return return_message(message=response)

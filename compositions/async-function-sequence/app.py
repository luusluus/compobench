import json

from compose import compose


def a(event, context):
    data = {
        'greet': f'Hello world from {a.__name__}. '
    }
    response = compose(function_name='AsyncSequenceFunctionB', data=data)
    return response

def b(event, context):
    event['greet'] = event['greet'] + f'Hello world from {b.__name__}. '
    response = compose(function_name='AsyncSequenceFunctionC', data=event)
    return response

def c(event, context):
    event['greet'] = event['greet'] + f'Hello world from {c.__name__}. '
    print(event['greet'])
    return {
        'statusCode': 200
    }

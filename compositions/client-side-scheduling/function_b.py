import os

def lambda_handler(event, context):
    return hello_world(prev_hello_world=event)

def hello_world(prev_hello_world):
    function_name = os.path.basename(__file__).split('.')[0]
    return prev_hello_world + f'Hello world from {function_name}. '
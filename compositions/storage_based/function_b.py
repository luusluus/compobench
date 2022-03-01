import os
from compose import compose

def lambda_handler(event, context):
    compose(event=event, business_logic_function=hello_world)

def hello_world(prev_hello_world):
    function_name = os.path.basename(__file__).split('.')[0]
    return {
        'result': prev_hello_world['result'] + f'Hello world from {function_name}. '
    }
import os
from compose import compose

def lambda_handler(event, context):
    return compose(event=event, business_logic_function=hello_world)

def hello_world(prev_hello_world):
    function_name = os.path.basename(__file__).split('.')[0]
    return  prev_hello_world + f'Hello world from {function_name}. '
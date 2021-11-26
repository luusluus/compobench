import os
from compose import compose

from aws_xray_sdk.core import patch_all

patch_all()

def lambda_handler(event, context):
    return compose(event=event, function_name='', business_logic_function=hello_world)

def hello_world(prev_hello_world):
    function_name = os.path.basename(__file__).split('.')[0]
    return prev_hello_world + f'Hello world from {function_name}. '
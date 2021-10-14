import os
from compose import compose

def lambda_handler(event, context):
    function_name = os.path.basename(__file__).split('.')[0]
    data = {
        'greet': f'Hello world from {function_name}. '
    }
    response = compose(function_name='AsyncSequenceFunctionB', data=data)
    return response
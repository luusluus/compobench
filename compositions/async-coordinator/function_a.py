import os
from compose import compose

def lambda_handler(event, context):
    workflow_id = event['workflow_id']
    function_name = os.path.basename(__file__).split('.')[0]
    result = f'Hello world from {function_name}. '
    data = {
        'result': result,
        'workflow_id': workflow_id
    }
    return compose(
        function_name='AsyncCoordinatorFunctionCoordinator', 
        data=data)
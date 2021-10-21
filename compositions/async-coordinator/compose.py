from invoke import invoke

def compose(event, business_logic_function):
    result = business_logic_function()
    result['workflow_id'] = event['workflow_id']

    coordinator_function_name = 'AsyncCoordinatorFunctionCoordinator'
    
    invoke(function_name=coordinator_function_name, payload=result)

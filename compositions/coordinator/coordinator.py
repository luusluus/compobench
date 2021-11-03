from compose import compose

def lambda_handler(event, context):
    workflow = event['workflow']
    function_input = event['input']

    result = {
        'result': function_input
    }

    for step in workflow:
        response = compose(function_name=step, payload=result)
        result = {
            'result': response
        }

    return result
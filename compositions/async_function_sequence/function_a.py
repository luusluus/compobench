from compose import compose

def lambda_handler(event, context):
    return compose(event=event, function_name='AsyncSequenceFunctionB')
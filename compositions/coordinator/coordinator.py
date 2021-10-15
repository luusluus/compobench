
import os
from compose import compose

def lambda_handler(event, context):
    result_a = compose(function_name='CoordinatorFunctionA', data={})
    result_b = compose(function_name='CoordinatorFunctionB', data={})
    result_c = compose(function_name='CoordinatorFunctionC', data={})

    return result_a + result_b + result_c
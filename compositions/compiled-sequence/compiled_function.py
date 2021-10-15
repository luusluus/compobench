
import os

def function_a():
    return f'Hello world from {function_a.__name__}. '

def function_b():
    return f'Hello world from {function_b.__name__}. '

def function_c():
    return f'Hello world from {function_c.__name__}. '

def lambda_handler(event, context):
    return function_a() + function_b() + function_c()
import time
import uuid

def function_a(sleep_time):
    time.sleep(sleep_time)

def function_b(sleep_time):
    time.sleep(sleep_time)

def function_c(sleep_time):
    time.sleep(sleep_time)


def lambda_handler(event, context):
    function_a(event['sleep'])
    function_b(event['sleep'])
    function_c(event['sleep'])
    
    return
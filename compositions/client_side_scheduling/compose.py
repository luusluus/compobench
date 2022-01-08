import os
import time

def compose(event, business_logic_function):
    time.sleep(event['sleep'])
    return business_logic_function(event['input'])

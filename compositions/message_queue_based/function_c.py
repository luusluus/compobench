import os
from compose import compose

def lambda_handler(event, context):
    compose(event=event)



import json
from compose import compose

aws_region = 'eu-central-1'

workflow = ['ClientSideFunctionA', 'ClientSideFunctionB', 'ClientSideFunctionC']
result = ''
for step in workflow:
    response = compose(
        aws_region=aws_region, 
        function_name=step, 
        data=result)
    result = response

print(result)


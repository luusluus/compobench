

import json
from compose import compose

aws_region = 'eu-central-1'

# call the first function a to start the workflow
result_a = compose(aws_region=aws_region, function_name='ClientSideFunctionA', data={})
result_b = compose(aws_region=aws_region, function_name='ClientSideFunctionB', data={})
result_c = compose(aws_region=aws_region, function_name='ClientSideFunctionC', data={})

print(result_a + result_b + result_c)



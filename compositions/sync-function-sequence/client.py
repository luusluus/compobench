

import json

import requests

from compositions.aws_helpers.api_gateway import ApiGatewayHelper

gateway_helper = ApiGatewayHelper(aws_region='eu-central-1')
endpoint = gateway_helper.get_api_gateway_endpoint(api_get_way_name='sync-function-sequence')

# call the first function a to start the workflow
response = requests.get(endpoint + 'a')

print(response.content.decode('utf-8'))
# print(json.loads(response.content.decode('utf-8')))



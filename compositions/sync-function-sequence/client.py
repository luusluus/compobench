

import json

import requests

from compositions.helpers.api_gateway import get_api_gateway_endpoint

endpoint = get_api_gateway_endpoint(api_get_way_name='sync-function-sequence')

# call the first function a to start the workflow
result = requests.get(endpoint + 'function/a')
print(json.loads(result.content))



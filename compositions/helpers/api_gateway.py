from boto3 import client as boto3_client

API_GATE_STAGES_PROD = 'Prod'
API_GATEWAY_STAGES_STAGE = 'Stage'

class ApiGatewayNotFound(Exception):
    pass

def get_api_gateway_endpoint(api_get_way_name: str, aws_region: str ='eu-central-1', stage: str = API_GATE_STAGES_PROD):
    client = boto3_client('apigateway', region_name=aws_region)

    rest_apis = client.get_rest_apis()

    rest_api = next((rest_api for rest_api in rest_apis['items'] if rest_api['name'] == api_get_way_name), None)

    if rest_api:
        rest_api_id = rest_api['id']
        rest_api_base_url = f'https://{rest_api_id}.execute-api.{aws_region}.amazonaws.com/{stage}/'
        return rest_api_base_url

    raise ApiGatewayNotFound

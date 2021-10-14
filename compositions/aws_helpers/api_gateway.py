from boto3 import client as boto3_client

API_GATE_STAGES_PROD = 'Prod'
API_GATEWAY_STAGES_STAGE = 'Stage'

class ApiGatewayNotFound(Exception):
    pass

class ApiGatewayHelper():
    def __init__(self, aws_region):
        self._client = boto3_client('apigateway', region_name=aws_region)
        self._aws_region = aws_region

    def get_api_gateway_endpoint(self, api_get_way_name: str, stage: str = API_GATE_STAGES_PROD):
        rest_apis = self._client.get_rest_apis()

        rest_api = next((rest_api for rest_api in rest_apis['items'] if rest_api['name'] == api_get_way_name), None)

        if rest_api:
            rest_api_id = rest_api['id']
            rest_api_base_url = f'https://{rest_api_id}.execute-api.{self._aws_region}.amazonaws.com/{stage}/'
            return rest_api_base_url

        raise ApiGatewayNotFound

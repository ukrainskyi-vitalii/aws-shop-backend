from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as api_gateway
)
from constructs import Construct


class ApiGateway(Stack):
    def __init__(self, scope: Construct, construct_id: str, import_products_file_fn: _lambda, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        api = api_gateway.RestApi(self, 'ImportServiceGateway',
                                  rest_api_name='Import Service',
                                  description='Service for importing product files'
                                  )

        import_resource = api.root.add_resource('import')
        import_resource.add_method('GET', api_gateway.LambdaIntegration(import_products_file_fn))

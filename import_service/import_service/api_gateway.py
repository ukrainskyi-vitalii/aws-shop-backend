from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as api_gateway
)
from constructs import Construct


class ApiGateway(Stack):
    def __init__(self, scope: Construct, construct_id: str, import_products_file_fn: _lambda.IFunction,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        api = api_gateway.RestApi(self, 'ImportServiceGateway',
                                  rest_api_name='Import Service',
                                  description='Service for importing product files',
                                  default_cors_preflight_options={
                                      "allow_origins": api_gateway.Cors.ALL_ORIGINS,
                                      "allow_methods": api_gateway.Cors.ALL_METHODS,
                                      "allow_headers": api_gateway.Cors.DEFAULT_HEADERS
                                  })

        basic_authorizer_lambda = _lambda.Function.from_function_name(self, 'authFunction', 'AuthFunction')

        authorizer = api_gateway.TokenAuthorizer(self, 'BasicAuthorizer',
                                                 handler=basic_authorizer_lambda,
                                                 identity_source='method.request.header.Authorization')

        import_resource = api.root.add_resource('import', default_cors_preflight_options={
            "allow_origins": api_gateway.Cors.ALL_ORIGINS,
            "allow_methods": api_gateway.Cors.ALL_METHODS,
            "allow_headers": api_gateway.Cors.DEFAULT_HEADERS
        })
        import_resource.add_method('GET', api_gateway.LambdaIntegration(import_products_file_fn),
                                   authorization_type=api_gateway.AuthorizationType.CUSTOM,
                                   authorizer=authorizer
                                   )

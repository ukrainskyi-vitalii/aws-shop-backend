from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_apigateway as apigateway
from aws_cdk import Stack
from constructs import Construct


class ApiGateway(Stack):

    def __init__(self, scope: Construct, construct_id: str, get_product_list_fn: _lambda, get_product_by_id_fn: _lambda,
                 create_product_fn: _lambda, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        api = apigateway.RestApi(self, 'ProductServiceGateway', rest_api_name='Product Service',
                                 description='Product Service',
                                 default_cors_preflight_options={
                                     "allow_origins": apigateway.Cors.ALL_ORIGINS,
                                     "allow_methods": apigateway.Cors.ALL_METHODS,
                                     "allow_headers": apigateway.Cors.DEFAULT_HEADERS
                                 })

        products_resource = api.root.add_resource('products')
        products_resource.add_method('GET', apigateway.LambdaIntegration(get_product_list_fn))
        products_resource.add_method('POST', apigateway.LambdaIntegration(create_product_fn))

        product_by_id_resource = products_resource.add_resource('{id}')
        product_by_id_resource.add_method('GET', apigateway.LambdaIntegration(get_product_by_id_fn))


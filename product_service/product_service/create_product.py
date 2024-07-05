from aws_cdk import aws_lambda as _lambda
from aws_cdk import Stack
from constructs import Construct


class CreateProduct(Stack):

    def __init__(self, scope: Construct, construct_id: str, environment, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.create_product = _lambda.Function(self, 'CreateProductHandler',
                                               runtime=_lambda.Runtime.PYTHON_3_11,
                                               code=_lambda.Code.from_asset('product_service/lambda_func/'),
                                               handler='product_create.lambda_handler',
                                               environment=environment
                                               )
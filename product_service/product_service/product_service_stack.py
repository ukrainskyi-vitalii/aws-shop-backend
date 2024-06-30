from aws_cdk import Stack
from .api_gateway import ApiGateway
from .get_products import GetProducts
from .get_product_by_id import GetProductById
from constructs import Construct


class ProductServiceStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        get_product_list_lbd = GetProducts(self, 'ProductsList')
        get_product_by_id_lbd = GetProductById(self, 'ProductById')
        ApiGateway(self, 'ApiGateway', get_product_list_fn=get_product_list_lbd.get_product_list,
                   get_product_by_id_fn=get_product_by_id_lbd.get_product_by_id)

from aws_cdk import Stack
from aws_cdk import aws_dynamodb as dynamodb
from .api_gateway import ApiGateway
from .get_products import GetProducts
from .get_product_by_id import GetProductById
from .create_product import CreateProduct
from .catalog_batch import CatalogBatch
from constructs import Construct


class ProductServiceStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        products_table_name = 'products'
        stocks_table_name = 'stocks'

        product_table = dynamodb.Table.from_table_name(self, 'ProductsTable', products_table_name)
        stock_table = dynamodb.Table.from_table_name(self, 'StocksTable', stocks_table_name)

        environment = {
            "PRODUCTS_TABLE_NAME": products_table_name,
            "STOCKS_TABLE_NAME": stocks_table_name,
            "REGION": "eu-west-1"
        }

        get_product_list_lbd = GetProducts(self, 'ProductsList', environment)
        get_product_by_id_lbd = GetProductById(self, 'ProductById', environment)
        create_product_lbd = CreateProduct(self, 'CreateProduct', environment)

        ApiGateway(self, 'ApiGateway', get_product_list_fn=get_product_list_lbd.get_product_list,
                   get_product_by_id_fn=get_product_by_id_lbd.get_product_by_id,
                   create_product_fn=create_product_lbd.create_product)

        product_table.grant_read_data(get_product_list_lbd.get_product_list)
        product_table.grant_read_data(get_product_by_id_lbd.get_product_by_id)
        product_table.grant_write_data(create_product_lbd.create_product)

        stock_table.grant_read_data(get_product_list_lbd.get_product_list)
        stock_table.grant_read_data(get_product_by_id_lbd.get_product_by_id)
        stock_table.grant_write_data(create_product_lbd.create_product)

        CatalogBatch(self, 'CatalogBatch', environment)

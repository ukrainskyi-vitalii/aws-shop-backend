from aws_cdk import Stack
from constructs import Construct
from .import_products import ImportProducts
from .api_gateway import ApiGateway
from .import_file_parser import ImportFileParser


class ImportServiceStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket_name = 'aws-cdk-uploaded'

        import_products_file_lbd = ImportProducts(self, 'ImportProducts', bucket_name)
        ImportFileParser(self, 'ImportFileParser', bucket_name)

        ApiGateway(self, 'ApiGateway', import_products_file_fn=import_products_file_lbd.import_products_file)

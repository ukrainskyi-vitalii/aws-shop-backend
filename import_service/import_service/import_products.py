from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_s3 as s3
)
from constructs import Construct


class ImportProducts(Stack):
    def __init__(self, scope: Construct, construct_id: str, bucket_name: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket = s3.Bucket.from_bucket_name(self, 'ProductImportBucket', bucket_name)

        self.import_products_file = _lambda.Function(self, 'ImportProductsFileHandler',
                                                     runtime=_lambda.Runtime.PYTHON_3_11,
                                                     code=_lambda.Code.from_asset('import_service/lambda_func/'),
                                                     handler='import_products_file.lambda_handler',
                                                     environment={
                                                         "BUCKET_NAME": bucket.bucket_name
                                                     }
                                                     )

        bucket.grant_put(self.import_products_file)
        bucket.grant_read_write(self.import_products_file)

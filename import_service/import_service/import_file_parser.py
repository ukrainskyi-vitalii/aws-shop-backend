from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_s3 as s3,
    aws_s3_notifications as s3_notifications
)
from constructs import Construct


class ImportFileParser(Stack):
    def __init__(self, scope: Construct, construct_id: str, bucket_name: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket = s3.Bucket.from_bucket_name(self, 'ProductImportBucket', bucket_name)

        self.import_file_parser = _lambda.Function(self, 'ImportFileParserHandler',
                                                   runtime=_lambda.Runtime.PYTHON_3_11,
                                                   code=_lambda.Code.from_asset('import_service/lambda_func/'),
                                                   handler='import_file_parser.lambda_handler',
                                                   environment={
                                                       "BUCKET_NAME": bucket.bucket_name
                                                   }
                                                   )

        bucket.grant_put(self.import_file_parser)
        bucket.grant_read_write(self.import_file_parser)
        bucket.grant_delete(self.import_file_parser)

        notification = s3_notifications.LambdaDestination(self.import_file_parser)
        bucket.add_event_notification(s3.EventType.OBJECT_CREATED, notification,
                                      s3.NotificationKeyFilter(prefix="uploaded/"))

from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions,
    aws_lambda_event_sources as lambda_event_sources,
    aws_dynamodb as dynamodb,
    CfnOutput
)
from constructs import Construct


class CatalogBatch(Stack):

    def __init__(self, scope: Construct, construct_id: str, environment, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        queue = sqs.Queue(self, "CatalogItemsQueue")

        sns_topic = sns.Topic(self, "CreateProductTopic")
        sns_topic.add_subscription(subscriptions.EmailSubscription("ukrainskyi.vitalii@gmail.com"))
        sns_topic.add_subscription(subscriptions.EmailSubscription(
            "aws.vit86@gmail.com",
            filter_policy={
                "price": sns.SubscriptionFilter.numeric_filter(greater_than_or_equal_to=100)
            }
        ))

        self.catalog_batch = _lambda.Function(self, 'catalogBatchProcess',
                                              runtime=_lambda.Runtime.PYTHON_3_11,
                                              code=_lambda.Code.from_asset('product_service/lambda_func/'),
                                              handler='catalog_batch_process.lambda_handler',
                                              environment={
                                                  **environment,
                                                  "SQS_QUEUE_URL": queue.queue_url,
                                                  "SNS_TOPIC_ARN": sns_topic.topic_arn
                                              }
                                              )

        queue.grant_consume_messages(self.catalog_batch)
        sns_topic.grant_publish(self.catalog_batch)

        self.catalog_batch.add_event_source(lambda_event_sources.SqsEventSource(queue, batch_size=5))

        self.product_table = dynamodb.Table.from_table_name(self, "ProductsTable", environment['PRODUCTS_TABLE_NAME'])
        self.stock_table = dynamodb.Table.from_table_name(self, "StocksTable", environment['STOCKS_TABLE_NAME'])

        self.product_table.grant_read_write_data(self.catalog_batch)
        self.stock_table.grant_read_write_data(self.catalog_batch)

        CfnOutput(self, "CatalogItemsQueueArnOutput", value=queue.queue_arn, export_name="CatalogItemsQueueArn")
        CfnOutput(self, "CatalogItemsQueueUrlOutput", value=queue.queue_url, export_name="CatalogItemsQueueUrl")

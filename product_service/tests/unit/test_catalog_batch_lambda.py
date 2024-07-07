import json
import os
from unittest.mock import MagicMock, patch
from product_service.product_service.lambda_func import catalog_batch_process


@patch('product_service.product_service.lambda_func.catalog_batch_process.boto3.client')
def test_lambda_handler(mock_boto_client):
    mock_dynamodb = MagicMock()
    mock_sns = MagicMock()
    mock_boto_client.side_effect = lambda service_name, **kwargs: {
        'dynamodb': mock_dynamodb,
        'sns': mock_sns
    }[service_name]

    # Mock data for DynamoDB and SNS
    mock_dynamodb.transact_write_items.return_value = {}
    mock_sns.publish.return_value = {}

    os.environ['PRODUCTS_TABLE_NAME'] = 'products'
    os.environ['STOCKS_TABLE_NAME'] = 'stocks'
    os.environ['SNS_TOPIC_ARN'] = 'arn:aws:sns:eu-west-1:590184028943:ProductServiceStackCatalogBatchE5BCD2AC-CreateProductTopicE4CD9217-wIfxwdk1QMv9'

    event = {
        'Records': [
            {
                'body': json.dumps({
                    'title': 'Test Product',
                    'description': 'Test Description',
                    'price': 150,
                    'count': 10
                })
            }
        ]
    }
    context = {}

    response = catalog_batch_process.lambda_handler(event, context)

    # Check the response
    assert response['statusCode'] == 200
    assert json.loads(response['body']) == 'Processed successfully'

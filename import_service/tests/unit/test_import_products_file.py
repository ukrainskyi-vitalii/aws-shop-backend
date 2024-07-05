import os
import json
import boto3
import unittest
from unittest.mock import patch, MagicMock
from import_service.lambda_func.import_products_file import lambda_handler


class TestImportProductsFile(unittest.TestCase):

    @patch('import_service.lambda_func.import_products_file.boto3.client')
    def test_lambda_handler(self, mock_boto_client):
        mock_s3_client = MagicMock()
        mock_boto_client.return_value = mock_s3_client

        bucket_name = 'aws-cdk-uploaded'
        os.environ['BUCKET_NAME'] = bucket_name

        event = {
            'queryStringParameters': {
                'name': 'test.csv'
            }
        }
        context = {}

        response = lambda_handler(event, context)
        print(f"{response}")

        self.assertEqual(response['statusCode'], 200)
        self.assertIn('https://', response['body'])
        self.assertEqual(response['headers']['Content-Type'], 'application/json')
        self.assertEqual(response['headers']['Access-Control-Allow-Origin'], '*')
        self.assertEqual(response['headers']['Access-Control-Allow-Methods'], 'GET,PUT,OPTIONS,POST')

        del os.environ['BUCKET_NAME']


if __name__ == '__main__':
    unittest.main()

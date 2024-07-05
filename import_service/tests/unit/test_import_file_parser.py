import os
import io
import json
import unittest
from unittest.mock import patch, MagicMock
from import_service.lambda_func.import_file_parser import lambda_handler


class TestImportFileParser(unittest.TestCase):

    @patch('import_service.lambda_func.import_file_parser.s3.get_object')
    @patch('import_service.lambda_func.import_file_parser.s3.copy_object')
    @patch('import_service.lambda_func.import_file_parser.s3.delete_object')
    def test_lambda_handler(self, mock_delete_object, mock_copy_object, mock_get_object):
        # Mocking get_object response
        mock_body = MagicMock()
        mock_body.read.return_value = b"id,product_name,description,price,value\ndf59ba55-8152-4992-9973-245f12f547b3,Product 1,Description 1,99,1"
        mock_get_object.return_value = {
            'Body': mock_body
        }

        # Mocking copy_object and delete_object to do nothing
        mock_copy_object.return_value = {}
        mock_delete_object.return_value = {}

        # Setting the environment variable for the bucket name
        bucket_name = 'aws-cdk-uploaded'
        os.environ['BUCKET_NAME'] = bucket_name

        # Creating an event to trigger the lambda function
        event = {
            'Records': [
                {
                    's3': {
                        'bucket': {
                            'name': bucket_name
                        },
                        'object': {
                            'key': 'uploaded/test.csv'
                        }
                    }
                }
            ]
        }
        context = {}

        # Calling the lambda function
        lambda_handler(event, context)

        # Checking that get_object was called correctly
        mock_get_object.assert_called_once_with(Bucket=bucket_name, Key='uploaded/test.csv')

        # Checking that copy_object was called correctly
        copy_source = {'Bucket': bucket_name, 'Key': 'uploaded/test.csv'}
        parsed_key = 'parsed/test.csv'
        mock_copy_object.assert_called_once_with(CopySource=copy_source, Bucket=bucket_name, Key=parsed_key)

        # Checking that delete_object was called correctly
        mock_delete_object.assert_called_once_with(Bucket=bucket_name, Key='uploaded/test.csv')


if __name__ == '__main__':
    unittest.main()

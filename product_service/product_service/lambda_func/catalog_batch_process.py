import json
import os
import boto3
import uuid

dynamodb = boto3.client('dynamodb')
sns = boto3.client('sns')

table_name = os.environ['PRODUCTS_TABLE_NAME']
stocks_table_name = os.environ['STOCKS_TABLE_NAME']
sns_topic_arn = os.getenv('SNS_TOPIC_ARN')


def lambda_handler(event, context):
    for record in event['Records']:
        message = json.loads(record['body'])
        print(f"message {message}")
        product_id = str(uuid.uuid4())
        price = str(message.get('price', 0))

        product_item = {
            'id': {'S': product_id},
            'title': {'S': message.get('title', '')},
            'description': {'S': message.get('description', '')},
            'price': {'N': price}
        }

        stock_item = {
            'product_id': {'S': product_id},
            'count': {'N': str(message.get('count', 0))}
        }

        transaction_items = [
            {
                'Put': {
                    'TableName': os.getenv('PRODUCTS_TABLE_NAME'),
                    'Item': product_item
                }
            },
            {
                'Put': {
                    'TableName': os.getenv('STOCKS_TABLE_NAME'),
                    'Item': stock_item
                }
            }
        ]

        try:
            dynamodb.transact_write_items(TransactItems=transaction_items)
            print(f"Product {product_id} added successfully")

            sns.publish(
                TopicArn=sns_topic_arn,
                Message=json.dumps({
                    'default': json.dumps(message),
                    'email': f"Product created: {json.dumps(message)}"
                }),
                Subject='Product Creation Notification',
                MessageStructure='json',
                MessageAttributes={
                    'price': {
                        'DataType': 'Number',
                        'StringValue': price
                    }
                }
            )
        except Exception as e:
            print(f"Error adding product {product_id}: {str(e)}")

        return {
            'statusCode': 200,
            'body': json.dumps('Processed successfully')
        }

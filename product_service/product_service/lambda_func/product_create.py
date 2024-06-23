import json
import os
import boto3
import uuid


def lambda_handler(event, context):
    print(f"Received event: {json.dumps(event)}")
    print(f"Received context: {context}")

    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST"
    }

    try:
        body = json.loads(event['body'])
    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Invalid JSON formart"}),
            "headers": headers
        }

    required_fields = ['title', 'description', 'price', 'count']
    for field in required_fields:
        if field not in body:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": f"Missing required field: {field}"}),
                "headers": headers
            }

    title = body['title']
    description = body['description']
    price = body['price']
    count = body['count']

    if not isinstance(price, (int, float)):
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Price must be a number"}),
            "headers": headers
        }

    if not isinstance(count, int):
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Count must be a number"}),
            "headers": headers
        }

    try:
        dynamodb = boto3.client('dynamodb', region_name=os.getenv('REGION'))

        product_id = str(uuid.uuid4())

        product_item = {
            'id': {'S': product_id},
            'title': {'S': title},
            'description': {'S': description},
            'price': {'N': str(price)},
        }

        stock_item = {
            'product_id': {'S': product_id},
            'count': {'N': str(count)}
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

        dynamodb.transact_write_items(TransactItems=transaction_items)

        response = {
            "statusCode": 200,
            "body": json.dumps({
                'message': 'Product added successfully',
                'product_id': product_id
            }),
            "headers": headers
        }

        return response
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": f"Internal server error: {str(e)}"}),
            "headers": headers
        }

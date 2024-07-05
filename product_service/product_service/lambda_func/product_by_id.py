import json
import os
import boto3


def lambda_handler(event, context):
    print(f"Received event: {json.dumps(event)}")
    print(f"Received context: {context}")

    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET"
    }

    try:
        product_id = event.get('pathParameters', {}).get('id')

        dynamodb = boto3.resource('dynamodb', region_name=os.getenv('REGION'))

        products_table = dynamodb.Table(os.getenv('PRODUCTS_TABLE_NAME'))
        products_response = products_table.get_item(
            Key={'id': product_id}
        )

        product_item = products_response.get('Item')
        if not product_item:
            return {
                "statusCode": 404,
                "body": json.dumps({"message": "Product not found"}),
                "headers": headers
            }

        stocks_table = dynamodb.Table(os.getenv('STOCKS_TABLE_NAME'))
        stocks_response = stocks_table.get_item(
            Key={'product_id': product_id}
        )

        stock_item = stocks_response.get('Item', {})
        stock_count = int(stock_item.get('count', 0))

        product = {
            **product_item,
            'count': stock_count,
            'price': int(product_item['price'])
        }

        return {
            "statusCode": 200,
            "body": json.dumps(product),
            "headers": headers
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": f"Internal server error: {str(e)}"}),
            "headers": headers
        }


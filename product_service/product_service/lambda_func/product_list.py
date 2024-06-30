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
        dynamodb = boto3.resource('dynamodb', region_name=os.getenv('REGION'))

        products_table = dynamodb.Table(os.getenv('PRODUCTS_TABLE_NAME'))
        stocks_table = dynamodb.Table(os.getenv('STOCKS_TABLE_NAME'))

        products_response = products_table.scan()
        products_items = products_response.get('Items', [])

        stocks_response = stocks_table.scan()
        stocks_items = stocks_response.get('Items', [])

        products_dict = {item['id']: item for item in products_items}

        for item in stocks_items:
            product_id = item['product_id']
            if product_id in products_dict:
                products_dict[product_id]['count'] = int(item['count'])
                products_dict[product_id]['price'] = int(products_dict[product_id]['price'])

        products = list(products_dict.values())

        response = {
            "statusCode": 200,
            "body": json.dumps(products),
            "headers": headers
        }

        return response
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": f"Internal server error: {str(e)}"}),
            "headers": headers
        }

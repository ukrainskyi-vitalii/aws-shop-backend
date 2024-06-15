import json


def lambda_handler(event, context):
    products = [
        {
            "id": "1",
            "name": "Golden Retriever",
            "description": "Golden Retrievers are friendly, intelligent, and devoted. They are great family pets.",
            "price": 120
        },
        {
            "id": "2",
            "name": "German Shepherd",
            "description": "German Shepherds are confident, courageous, and smart. They are excellent working dogs.",
            "price": 1200
        },
        {
            "id": "3",
            "name": "Bulldog",
            "description": "Bulldogs are calm, courageous, and friendly. They are known for their loose, wrinkled skin.",
            "price": 1500
        },
        {
            "id": "4",
            "name": "Beagle",
            "price": 800,
            "description": "Beagles are curious, friendly, and merry. They are known for their excellent sense of smell."
        },
        {
            "id": "5",
            "name": "Poodle",
            "price": 900,
            "description": "Poodles are active, proud, and very smart. They come in three sizes: standard, miniature, and toy."
        }
    ]

    product_id = event.get('pathParameters', {}).get('id')
    product = next((product for product in products if product["id"] == product_id), None)

    if not product:
        return {
            "statusCode": 404,
            "body": json.dumps({"message": "Product not found"}),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS"
            }
        }

    return {
        "statusCode": 200,
        "body": json.dumps(product),
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS"
        }
    }

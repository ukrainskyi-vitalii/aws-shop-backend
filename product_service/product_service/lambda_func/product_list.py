import json


def lambda_handler(event, context):
    products = [
        {
            "id": "1",
            "title": "Golden Retriever",
            "description": "Golden Retrievers are friendly, intelligent, and devoted. They are great family pets.",
            "price": 120
        },
        {
            "id": "2",
            "title": "German Shepherd",
            "description": "German Shepherds are confident, courageous, and smart. They are excellent working dogs.",
            "price": 1200
        },
        {
            "id": "3",
            "title": "Bulldog",
            "description": "Bulldogs are calm, courageous, and friendly. They are known for their loose, wrinkled skin.",
            "price": 1500
        },
        {
            "id": "4",
            "title": "Beagle",
            "price": 800,
            "description": "Beagles are curious, friendly, and merry. They are known for their excellent sense of smell."
        },
        {
            "id": "5",
            "title": "Poodle",
            "price": 900,
            "description": "Poodles are active, proud, and very smart. They come in three sizes: standard, miniature, and toy."
        }
    ]

    response = {
        "statusCode": 200,
        "body": json.dumps(products),
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET"
        }
    }

    return response

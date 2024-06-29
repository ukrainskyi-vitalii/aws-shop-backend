import json
import os
import boto3

s3_client = boto3.client('s3')


def lambda_handler(event, context):
    print(f"Received event: {json.dumps(event)}")
    print(f"Received context: {context}")

    file_name = event.get('queryStringParameters')['name']
    bucket_name = os.environ['BUCKET_NAME']
    key = f"uploaded/{file_name}"

    params = {
        'Bucket': bucket_name,
        'Key': key
    }

    signed_url = s3_client.generate_presigned_url('put_object', Params=params)

    print(f"signed url: {signed_url}")

    return {
        "statusCode": 200,
        "body": signed_url,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS"
        }
    }

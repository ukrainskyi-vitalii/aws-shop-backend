import json
import os
import boto3

s3_client = boto3.client('s3')


def lambda_handler(event, context):
    print(f"Received event: {json.dumps(event)}")

    file_name = event.get('queryStringParameters')['name']
    bucket_name = os.environ['BUCKET_NAME']
    key = f"uploaded/{file_name}"

    params = {
        'Bucket': bucket_name,
        'Key': key,
        'ContentType': 'text/csv'
    }

    signed_url = s3_client.generate_presigned_url('put_object', Params=params, ExpiresIn=3600)

    print(f"signed url: {signed_url}")

    return {
        "statusCode": 200,
        "body": json.dumps({"url": signed_url}),
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,PUT,OPTIONS,POST"
        }
    }

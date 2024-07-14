import os
import base64


def lambda_handler(event, context):
    print(f"event: {event}")

    authorization_header = event.get('authorizationToken', '')
    if not authorization_header or ' ' not in authorization_header:
        raise Exception('Unauthorized')

    try:
        auth_scheme, auth_b64 = authorization_header.split(' ', 1)

        print(f"auth_scheme: {auth_scheme} auth_b64 {auth_b64}")

        if not auth_b64 or auth_b64 == 'null' or auth_scheme != 'Basic':
            return generate_policy('user', 'Deny', event['methodArn'])

        try:
            auth_decoded = base64.b64decode(auth_b64).decode('utf-8')
        except Exception:
            return generate_policy('user', 'Deny', event['methodArn'])

        username, password = auth_decoded.split('=', 1)
        expected_password = os.environ.get(username)
        if not expected_password or expected_password != password:
            return generate_policy(username, 'Deny', event['methodArn'])

        return generate_policy(username, 'Allow', event['methodArn'])

    except Exception as e:
        print(f"Exception: {str(e)}")
        return {
            'statusCode': 500,
            'body': f'Internal server error: {str(e)}',
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                "content-type": "text/plain"
            }
        }


def generate_policy(principal_id, effect, resource):
    auth_response = {
        'principalId': principal_id
    }
    if effect and resource:
        policy_document = {
            'Version': '2012-10-17',
            'Statement': [{
                'Action': 'execute-api:Invoke',
                'Effect': effect,
                'Resource': resource
            }]
        }
        auth_response['policyDocument'] = policy_document

    print(f"auth_response: {auth_response}")

    return auth_response

import json

from product_service.product_service.lambda_func import product_by_id
from product_service.product_service.lambda_func import product_list


def test_get_product_by_id():
    event = {
        "pathParameters": {"id": "1"}
    }
    response = product_by_id.lambda_handler(event, None)
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert len(body) > 0
    assert body['id'] == '1'
    assert body['name'] == 'Golden Retriever'


def test_get_product_by_id_for_unknown_product():
    event = {
        "pathParameters": {"id": "11"}
    }
    response = product_by_id.lambda_handler(event, None)
    assert response['statusCode'] == 404
    body = json.loads(response['body'])
    assert body['message'] == 'Product not found'


def test_get_all_products():
    response = product_list.lambda_handler(None, None)
    print(f"response")
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert len(body) > 0

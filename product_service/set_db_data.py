import boto3
import uuid
from decimal import Decimal
from faker import Faker

dynamodb = boto3.resource('dynamodb')

products_table = dynamodb.Table('products')
stocks_table = dynamodb.Table('stocks')

fake = Faker()


def add_product(title, description, price):
    product_id = str(uuid.uuid4())
    products_table.put_item(
        Item={
            'id': product_id,
            'title': title,
            'description': description,
            'price': Decimal(price)
        }
    )
    return product_id


def add_stock(product_id, count):
    stocks_table.put_item(
        Item={
            'product_id': product_id,
            'count': count
        }
    )


def generate_test_data(num_entries):
    for _ in range(num_entries):
        title = fake.name()
        description = fake.text()
        price = fake.random_int(min=10, max=1000)
        count = fake.random_int(min=1, max=100)

        product_id = add_product(title, description, price)
        add_stock(product_id, count)


generate_test_data(10)

print("Test data added to both tables successfully.")

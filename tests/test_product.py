'''
Test the Product operations


Use the product_fixture to have data to retrieve, it generated three products
'''
from unittest.mock import ANY
import http.client


def test_create_product(client, product_fixture):
    new_product = {
        'product_description': 'New product',
    }
    response = client.post('/api/product/', data=new_product)
    result = response.json

    assert http.client.CREATED == response.status_code

    expected = {
        'product_id': ANY,
        'product_description': 'New product'
    }
    assert result == expected


def test_list_products(client, product_fixture):
    response = client.get('/api/product/')
    result = response.json

    assert http.client.OK == response.status_code
    assert len(result) > 0

    # Check that the ids are increasing
    previous_id = -1
    for product in result:
        expected = {
            'product_id': ANY,
            'product_description': ANY,
        }
        assert expected == product
        assert product['product_id'] > previous_id
        previous_id = product['product_id']


def test_get_product(client, product_fixture):
    product_id = product_fixture[0]
    response = client.get(f'/api/product/{product_id}')
    result = response.json

    assert http.client.OK == response.status_code
    assert result['product_description'] == f'Product A'
    assert 'product_id' in result


def test_get_not_found_product(client):
    response = client.get('/api/product/1234')

    assert http.client.NOT_FOUND == response.status_code


def test_delete_product(client, product_fixture):
    product_id = product_fixture[0]
    url = f'/api/product/{product_id}'
    response = client.delete(url)

    assert http.client.NO_CONTENT == response.status_code

    # The product is gone
    response = client.get(url)
    assert http.client.NOT_FOUND == response.status_code

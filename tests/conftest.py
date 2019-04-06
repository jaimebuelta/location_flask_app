import pytest
from locations.app import create_app


@pytest.fixture
def app():
    application = create_app()
    return application


@pytest.fixture
def product_fixture(client):
    '''
    Generate three products in the system.
    The description will be "Product A", "Product B" and "Product C"
    '''

    product_ids = []
    for index in ('A', 'B', 'C'):
        product = {
            'product_description': f'Product {index}',
        }
        response = client.post('/api/product/', data=product)
        result = response.json
        product_ids.append(result['product_id'])

    yield product_ids

    # Clean up all products
    response = client.get('/api/product/')
    for product in response.json:
        product_id = product['product_id']
        url = f'/api/product/{product_id}'
        client.delete(url)

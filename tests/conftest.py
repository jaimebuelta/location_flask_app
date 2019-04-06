import pytest
import random
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

    # Clean up products
    for product_id in product_ids:
        url = f'/api/product/{product_id}'
        client.delete(url)


@pytest.fixture
def locations_fixture(client, product_fixture):
    '''
    Generate four locations in the system
    for each of the product fixtures
    '''

    all_locations = {}
    for product in product_fixture:
        locations = []
        for _ in range(4):
            location = {
                'elevation': random.randint(-10000, 9000),
                'longitude': random.uniform(-180, 180),
                'latitude': random.uniform(-90, 90),
            }
            url = f'/api/product/{product}/location/'
            response = client.post(url, data=location)
            result = response.json
            locations.append(result)
        all_locations[product] = locations

    yield all_locations

    # The locations will be cleaned when the products are
    # deleted

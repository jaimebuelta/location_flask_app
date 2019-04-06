'''
Test the Product operations


Use the product_fixture to have products available and
location_fixture to have locations
'''
from unittest.mock import ANY
import http.client
from freezegun import freeze_time


def test_create_location(client, product_fixture):
    new_location = {
        'latitude': -47.15,
        'longitude': -126.716667,
        'elevation': -10000,
    }
    product_id = product_fixture[0]
    with freeze_time('2012-01-14T17:52:53'):
        response = client.post(f'/api/product/{product_id}/location/',
                               data=new_location)
    result = response.json

    assert http.client.CREATED == response.status_code
    expected = {
        'latitude': -47.15,
        'longitude': -126.716667,
        'elevation': -10000,
        'timestamp': '2012-01-14T17:52:53',
    }

    assert result == expected
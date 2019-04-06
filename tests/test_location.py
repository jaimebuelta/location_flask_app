'''
Test the Product operations


Use the product_fixture to have products available and
location_fixture to have locations
'''
import pytest
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


@pytest.mark.parametrize(['new_location'],
    [
        [{'latitude': 0}],
        [{'longitude': 0}],
        [{'elevation': 0}],
        [{'latitude': 0, 'longitude': 0}],
        [{'latitude': 0, 'elevation': 0}],
        [{'longitude': 0, 'elevation': 0}],
    ],
)
def test_create_location_missing_input(new_location, client, product_fixture):
    product_id = product_fixture[0]
    with freeze_time('2012-01-14T17:52:53'):
        response = client.post(f'/api/product/{product_id}/location/',
                               data=new_location)

    assert http.client.BAD_REQUEST == response.status_code
    result = response.json
    # Check there's a "missing" error message
    assert 'errors' in result
    assert [error_msg for error_msg in result['errors'].values()
            if 'Missing' in error_msg]


@pytest.mark.parametrize(['new_location', 'error_msg'],
    [
        [{'latitude': 'BAD', 'longitude': 0, 'elevation': 0}, 'convert'],
        [{'latitude': 0, 'longitude': 'BAD', 'elevation': 0}, 'convert'],
        [{'latitude': 0, 'longitude': 0, 'elevation': 'BAD'}, 'base 10'],
        [{'latitude': 0, 'longitude': 0, 'elevation': 0.1}, 'base 10'],
        [{'latitude': 90.01, 'longitude': 0, 'elevation': 0}, 'Not valid'],
        [{'latitude': -90.01, 'longitude': 0, 'elevation': 0}, 'Not valid'],
        [{'latitude': 0, 'longitude': 180.01, 'elevation': 0}, 'Not valid'],
        [{'latitude': 0, 'longitude': -180.01, 'elevation': 0}, 'Not valid'],
    ],
)
def test_create_location_bad_input(new_location, error_msg,
                                   client, product_fixture):
    '''
    Validate input, including longitude and latitude ranges
    '''
    product_id = product_fixture[0]
    with freeze_time('2012-01-14T17:52:53'):
        response = client.post(f'/api/product/{product_id}/location/',
                               data=new_location)

    assert http.client.BAD_REQUEST == response.status_code
    result = response.json
    # Check there's a "convert" error message
    assert 'errors' in result
    assert [msg for msg in result['errors'].values()
            if error_msg in msg]


def test_list_location(client, product_fixture, locations_fixture):
    product_id = product_fixture[0]
    response = client.get(f'/api/product/{product_id}/location/')

    results = response.json

    assert http.client.OK == response.status_code
    assert len(results) == 4
    expected = {
        'latitude': ANY,
        'longitude': ANY,
        'elevation': ANY,
        'timestamp': ANY,
    }

    for result in results:
        assert result == expected


def test_list_location_not_found_product(client, product_fixture,
                                         locations_fixture):
    response = client.get(f'/api/product/2345/location/')

    assert http.client.NOT_FOUND == response.status_code


def test_list_all_locations(client, product_fixture, locations_fixture):
    response = client.get(f'/api/location/')

    assert http.client.OK == response.status_code

    paginated_format = {
        'result': ANY,
        'next': ANY,
        'previous': ANY,
        # 17 initial elements from input.txt
        # 12 in the fixtures (3 * 4)
        'total': 12 + 17,
    }
    assert paginated_format == response.json

    expected = {
        'product_id': ANY,
        'description': ANY,
        'latitude': ANY,
        'longitude': ANY,
        'elevation': ANY,
        'timestamp': ANY,
    }
    for result in response.json['result']:
        assert result == expected


def test_list_all_locations_pagination(client, product_fixture,
                                       locations_fixture):
    '''
    Paginate so we retrieve the values in two pages.

    Check the next and previous are the expected results
    '''
    response = client.get(f'/api/location/?size=20')

    assert http.client.OK == response.status_code

    paginated_format = {
        'result': ANY,
        'next': ANY,
        'previous': ANY,
        # 17 initial elements from input.txt
        # 12 in the fixtures (3 * 4)
        'total': 12 + 17,
    }
    assert paginated_format == response.json
    assert len(response.json['result']) == 20

    assert response.json['previous'] is None

    next_page = response.json['next']
    response = client.get(next_page)

    assert http.client.OK == response.status_code
    assert len(response.json['result']) == 9
    assert response.json['next'] is None
    assert 'size=20' in response.json['previous']
    assert 'page=1' in response.json['previous']


@pytest.mark.parametrize(['size', 'page', 'error_msg'],
    [
        ('BAD', 1, 'base 10'),
        (1, 'BAD', 'base 10'),
        (0, 1, 'positive integer'),
        (1, 0, 'positive integer'),
        (-1, 1, 'positive integer'),
        (1, -1, 'positive integer'),
        (0.1, 1, 'base 10'),
        (1, 0.1, 'base 10'),
    ],
)
def test_list_all_locations_bad_pagination(client, size, page, error_msg):
    '''
    Check only valid pagination params are accepted
    '''
    params = {
        'size': size,
        'page': page,
    }
    response = client.get(f'/api/location/', query_string=params)
    assert response.status_code == http.client.BAD_REQUEST
    result = response.json
    # Check there's a "convert" error message
    assert 'errors' in result
    assert [msg for msg in result['errors'].values()
            if error_msg in msg]

'''
Test the ops operations
'''
from unittest import mock
import http.client


def test_healthcheck(client):
    response = client.get('/ops/healthcheck')
    assert http.client.OK == response.status_code


def test_healthcheck_no_db_connection(client):
    with mock.patch('locations.db.db.session.execute') as mock_db:
        mock_db.side_effect = Exception('bad connection')
        response = client.get('/ops/healthcheck')

    assert http.client.INTERNAL_SERVER_ERROR == response.status_code

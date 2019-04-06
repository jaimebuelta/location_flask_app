'''
Test the ops operations
'''
import http.client


def test_healthcheck(client):
    response = client.get('/ops/healthcheck')
    assert http.client.OK == response.status_code

import http.client


def test_healthcheck(client):
    response = client.get('/healthcheck')
    assert http.client.OK == response.status_code

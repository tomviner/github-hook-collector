import pytest
import json

from distutils.version import LooseVersion
import django


def test_django_version():
    ver = django.get_version()
    assert LooseVersion (ver) > LooseVersion('1.8.0')

def test_collect_body(client):
    data = {'repo': 'blog'}
    response = client.post('/hook/', data)
    assert response.status_code == 200
    assert response.content == json.dumps(data)

def test_collect_headers(client):
    headers = {
        'Host': 'localhost: 4567',
        'User-Agent': 'GitHub-Hookshot/044aadd',
        'Content-Type': 'application/json',
    }
    xheaders = {
        'X-Github-Delivery': '72d3162e-cc78-11e3-81ab-4c9367dc0958',
        'X-Github-Event': 'issues',
    }
    headers.update(xheaders)
    response = client.get('/hook/', **headers)
    assert response.status_code == 200
    assert response.content == json.dumps(xheaders)


# @pytest.mark.django_db
def test_collector():
    """
    submit data as github would
    ensure it's saved to db as expected
    """

def test_collector_admin(client, admin_client):
    response = client.get('/admin/collector/call/')
    assert response.status_code == 302

    response = admin_client.get('/admin/collector/call/')
    assert response.status_code == 200
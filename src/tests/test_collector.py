import pytest
import json

try:
    from httplib import CREATED
except ImportError:
    from http.client import CREATED
from distutils.version import LooseVersion

import django
from django.utils import timezone
from django.db import connection

from collector.models import Call


def test_django_version():
    ver = django.get_version()
    assert LooseVersion (ver) > LooseVersion('1.8')

@pytest.mark.django_db
def test_hstore_extension():
    sql = "select count(*) from pg_available_extensions where name = %s;"
    cursor = connection.cursor()

    cursor.execute(sql, ['hstore'])
    count = cursor.fetchone()

    assert count == (1,)


@pytest.mark.django_db
def test_collector(client):
    """
    Submit data as github would.
    Ensure it's saved to db.
    """
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
    data = {'repo': 'blog'}

    time_before = timezone.now()

    response = client.post('/hook/', data, **headers)
    assert response.status_code == CREATED

    (call,) = Call.objects.all()
    assert call.data == data
    assert call.headers == xheaders

    time_after = timezone.now()
    # make sure current time is used
    assert time_before <= call.submitted_at <= time_after


def test_collector_admin(client, admin_client):
    response = client.get('/admin/collector/call/')
    assert response.status_code == 302

    response = admin_client.get('/admin/collector/call/')
    assert response.status_code == 200
import json
from distutils.version import LooseVersion
try:
    from httplib import CREATED
except ImportError:
    from http.client import CREATED

import pytest

import django
from django.db import connection
from django.utils import timezone

from collector.models import Call


def test_django_version():
    "We need the latest dev version of django"
    ver = django.get_version()
    assert LooseVersion(ver) > LooseVersion('1.8')


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
    }
    xheaders = {
        'X-Github-Delivery': '72d3162e-cc78-11e3-81ab-4c9367dc0958',
        'X-Github-Event': 'issues',
    }
    headers.update(xheaders)
    data = {'repo': 'blog'}

    time_before = timezone.now()

    response = client.post(
        '/hook/', json.dumps(data),
        content_type='application/json', **headers
    )
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


@pytest.mark.django_db
def test_transform():
    this_year = timezone.now().year
    Call.objects.create(headers={}, data={})
    Call.objects.create(headers={}, data={},
                        submitted_at=timezone.datetime(2010, 10, 20))
    Call.objects.create(headers={}, data={},
                        submitted_at=timezone.datetime(2210, 10, 20))
    assert Call.objects.filter(submitted_at__year__gte=this_year).count() == 2

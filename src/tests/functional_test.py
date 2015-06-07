from __future__ import unicode_literals

import sys
import json

import pytest
import requests


url_map = {
    'prod': 'http://do.tomviner.co.uk/hook/',
    'staging': 'http://10.0.0.100/hook/',
    'dev': 'http://127.0.0.1:8000/hook/',
}

@pytest.mark.skipif(len(sys.argv) < 2, reason='Requires command line arg')
@pytest.fixture(params=url_map.items())
def end_point(request):
    if len(sys.argv) < 2:
        raise pytest.skip()
    name, url = request.param
    if sys.argv[1] in (name, 'all'):
        return url
    raise pytest.skip()


def test_end_point(end_point):
    """
    Submit data as github would.
    """
    headers = {
        'Host': 'localhost: 4567',
        'User-Agent': 'GitHub-Hookshot/044aadd',
        'Content-Type': 'application/json',
        # prod Django to give plaintext errors
        'X_REQUESTED_WITH': 'XMLHttpRequest',
    }
    xheaders = {
        'X-Github-Delivery': '72d3162e-cc78-11e3-81ab-4c9367dc0958',
        'X-Github-Event': 'issues',
    }
    headers.update(xheaders)
    data = json.dumps({'repo': 'blog'})

    response = requests.post(end_point, data, headers=headers)
    assert response.status_code == 201, response.content


if __name__ == '__main__':
    pytest.main(['src/tests/functional_test.py', '-v', '-s'])

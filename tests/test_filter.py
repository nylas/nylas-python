import json
import random
import httpretty
from httpretty import Response


DEFAULT_BODY = {
    "busy": True,
    "calendar_id": "94rssh7bd3rmsxsp19kiocxze",
    "description": None,
    "id": "cv4ei7syx10uvsxbs21ccsezf",
    "location": "1 Infinite loop, Cupertino",
    "message_id": None,
    "namespace_id": "384uhp3aj8l7rpmv9s2y2rukn",
    "object": "event",
    "owner": None,
    "participants": [],
    "read_only": False,
    "status": "confirmed",
    "title": "The rain song",
    "when": {
        "end_time": 1441056790,
        "object": "timespan",
        "start_time": 1441053190
    }
}

BODY = [DEFAULT_BODY for i in range(1, 51)]
BODY2 = [DEFAULT_BODY for i in range(1, 23)]


def test_no_filter(api_client, api_url):
    httpretty.enable()

    # httpretty kind of sucks and strips & parameters from the URL
    values = [Response(status=200, body=json.dumps(BODY)),
              Response(status=200, body=json.dumps(BODY2))]
    httpretty.register_uri(
        httpretty.GET,
        api_url + '/events',
        responses=values,
    )

    events = api_client.events.all()
    assert len(events) == 72
    assert events[0].id == 'cv4ei7syx10uvsxbs21ccsezf'

    httpretty.disable()


def test_two_filters(api_client, api_url):
    httpretty.enable()

    values2 = [Response(status=200, body='[]')]
    httpretty.register_uri(
        httpretty.GET,
        api_url + '/events?param1=a&param2=b',
        responses=values2,
    )
    events = api_client.events.where(param1='a', param2='b').all()
    assert len(events) == 0  # pylint: disable=len-as-condition
    query = httpretty.last_request().querystring
    assert query['param1'][0] == 'a'
    assert query['param2'][0] == 'b'
    httpretty.disable()

def test_no_offset(api_client, api_url):
    httpretty.enable()

    values = [Response(status=200, body='[]')]
    httpretty.register_uri(
        httpretty.GET,
        api_url + '/events?in=Nylas',
        responses=values,
    )
    list(api_client.events.where({'in': 'Nylas'}).items())
    query = httpretty.last_request().querystring
    assert query['in'][0] == 'Nylas'
    assert query['offset'][0] == '0'
    httpretty.disable()

def test_zero_offset(api_client, api_url):
    httpretty.enable()

    values = [Response(status=200, body='[]')]
    httpretty.register_uri(
        httpretty.GET,
        api_url + '/events?in=Nylas&offset=0',
        responses=values,
    )
    list(api_client.events.where({'in': 'Nylas', 'offset': 0}).items())
    query = httpretty.last_request().querystring
    assert query['in'][0] == 'Nylas'
    assert query['offset'][0] == '0'
    httpretty.disable()

def test_non_zero_offset(api_client, api_url):
    httpretty.enable()

    offset = random.randint(1, 1000)
    values = [Response(status=200, body='[]')]
    httpretty.register_uri(
        httpretty.GET,
        api_url + '/events?in=Nylas&offset=' + str(offset),
        responses=values,
    )
    list(api_client.events.where({'in': 'Nylas', 'offset': offset}).items())
    query = httpretty.last_request().querystring
    assert query['in'][0] == 'Nylas'
    assert query['offset'][0] == str(offset)
    httpretty.disable()

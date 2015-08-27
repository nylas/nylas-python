import json
import pytest
import responses
import httpretty
from httpretty import Response
from conftest import API_URL
from nylas.client.errors import InvalidRequestError


url = API_URL + '/events/'
default_body = {
    "busy": True,
    "calendar_id": "94rssh7bd3rmsxsp19kiocxze",
    "description": None,
    "id": "cv4ei7syx10uvsxbs21ccsezf",
    "location": "1 Infinite loop, Cupertino",
    "message_id": None,
    "namespace_id": "384uhp3aj8l7rpmv9s2y2rukn",
    "object": "event",
    "owner": None,
    "participants": [ ],
    "read_only": False,
    "status": "confirmed",
    "title": "The rain song",
    "when": {
        "end_time": 1441056790,
        "object": "timespan",
        "start_time": 1441053190
    }
}

body = [default_body for i in range(1, 51)]
body2 = [default_body for i in range(1, 23)]


def test_no_filter(api_client):
    httpretty.enable()

    # httpretty kind of sucks and strips & parameters from the URL
    values = [Response(status=200, body=json.dumps(body)),
              Response(status=200, body=json.dumps(body2))]
    httpretty.register_uri(httpretty.GET, API_URL + '/events', responses=values)

    events = api_client.events.all()
    assert len(events) == 72
    assert events[0].id == 'cv4ei7syx10uvsxbs21ccsezf'

    httpretty.disable()


def test_two_filters(api_client):
    httpretty.enable()

    values2 = [Response(status=200, body='[]')]
    httpretty.register_uri(httpretty.GET, API_URL + '/events?param1=a&param2=b', responses=values2)
    events = api_client.events.where(param1='a', param2='b').all()
    assert len(events) == 0
    qs = httpretty.last_request().querystring
    assert qs['param1'][0] == 'a'
    assert qs['param2'][0] == 'b'
    httpretty.disable()

import json
import pytest
import responses
import httpretty
from httpretty import Response
from conftest import API_URL
from nylas.client.errors import InvalidRequestError


url = API_URL + '/events/'
body = {
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


@pytest.fixture
def mock_event_create_response():
    values = [Response(status=200, body=json.dumps(body)),
              Response(status=400, body='')]

    httpretty.register_uri(httpretty.POST, API_URL + '/events/', responses=values)
    put_values = [Response(status=200,
                           body=json.dumps({'title': 'loaded from JSON',
                                            'ignored': 'ignored'}))]
    httpretty.register_uri(httpretty.PUT, API_URL + '/events/cv4ei7syx10uvsxbs21ccsezf',
                           responses=put_values)


@pytest.fixture
def mock_event_create_notify_response():
    httpretty.register_uri(httpretty.POST, API_URL + '/events/?notify_participants=true&other_param=1',
                           body=json.dumps(body), status=200)


def blank_event(api_client):
    event = api_client.events.create()
    event.title = "Paris-Brest"
    event.calendar_id = 'calendar_id'
    event.when = {'start_time': 1409594400, 'end_time': 1409594400}
    return event


def test_event_crud(api_client, mock_event_create_response):
    httpretty.enable()

    e1 = blank_event(api_client)
    e1.save()
    assert e1.id == 'cv4ei7syx10uvsxbs21ccsezf'

    e1.title = 'blah'
    e1.save()
    assert e1.title == 'loaded from JSON'
    assert e1.get('ignored') is None

    # Third time should fail.
    e2 = blank_event(api_client)
    raised = False
    try:
        e2.save()
    except InvalidRequestError:
        raised = True

    assert raised is True

    httpretty.disable()


def test_event_notify(api_client, mock_event_create_notify_response):
    httpretty.enable()

    e1 = blank_event(api_client)
    e1.save(notify_participants='true', other_param='1')
    assert e1.id == 'cv4ei7syx10uvsxbs21ccsezf'

    qs = httpretty.last_request().querystring
    assert qs['notify_participants'][0] == 'true'
    assert qs['other_param'][0] == '1'

    httpretty.disable()

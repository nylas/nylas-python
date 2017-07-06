import json
import pytest
import httpretty
from httpretty import Response
from nylas.client.errors import InvalidRequestError


BODY = {
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


@pytest.fixture
def mock_event_create_response(api_url):
    values = [Response(status=200, body=json.dumps(BODY)),
              Response(status=400, body='')]

    httpretty.register_uri(httpretty.POST, api_url + '/events/', responses=values)
    put_values = [Response(status=200,
                           body=json.dumps({'title': 'loaded from JSON',
                                            'ignored': 'ignored'}))]
    httpretty.register_uri(httpretty.PUT, api_url + '/events/cv4ei7syx10uvsxbs21ccsezf',
                           responses=put_values)


@pytest.fixture
def mock_event_create_notify_response(api_url):
    httpretty.register_uri(
        httpretty.POST,
        api_url + '/events/?notify_participants=true&other_param=1',
        body=json.dumps(BODY),
        status=200
    )


def blank_event(api_client):
    event = api_client.events.create()
    event.title = "Paris-Brest"
    event.calendar_id = 'calendar_id'
    event.when = {'start_time': 1409594400, 'end_time': 1409594400}
    return event


@pytest.mark.usefixtures("mock_event_create_response")
def test_event_crud(api_client):
    httpretty.enable()

    event1 = blank_event(api_client)
    event1.save()
    assert event1.id == 'cv4ei7syx10uvsxbs21ccsezf'

    event1.title = 'blah'
    event1.save()
    assert event1.title == 'loaded from JSON'
    assert event1.get('ignored') is None

    # Third time should fail.
    event2 = blank_event(api_client)
    with pytest.raises(InvalidRequestError):
        event2.save()

    httpretty.disable()


@pytest.mark.usefixtures("mock_event_create_notify_response")
def test_event_notify(api_client):
    httpretty.enable()

    event1 = blank_event(api_client)
    event1.save(notify_participants='true', other_param='1')
    assert event1.id == 'cv4ei7syx10uvsxbs21ccsezf'

    query = httpretty.last_request().querystring
    assert query['notify_participants'][0] == 'true'
    assert query['other_param'][0] == '1'

    httpretty.disable()

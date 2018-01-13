import pytest
from urlobject import URLObject
from requests import RequestException
from nylas.client.restful_models import Event


def blank_event(api_client):
    event = api_client.events.create()
    event.title = "Paris-Brest"
    event.calendar_id = 'calendar_id'
    event.when = {'start_time': 1409594400, 'end_time': 1409594400}
    return event


@pytest.mark.usefixtures("mock_event_create_response")
def test_event_crud(api_client):
    event1 = blank_event(api_client)
    event1.save()
    assert event1.id == 'cv4ei7syx10uvsxbs21ccsezf'

    event1.title = 'blah'
    event1.save()
    assert event1.title == 'loaded from JSON'
    assert event1.get('ignored') is None

    # Third time should fail.
    event2 = blank_event(api_client)
    with pytest.raises(RequestException):
        event2.save()


@pytest.mark.usefixtures("mock_event_create_notify_response")
def test_event_notify(mocked_responses, api_client):
    event1 = blank_event(api_client)
    event1.save(notify_participants='true', other_param='1')
    assert event1.id == 'cv4ei7syx10uvsxbs21ccsezf'

    url = mocked_responses.calls[-1].request.url
    query = URLObject(url).query_dict
    assert query['notify_participants'] == 'true'
    assert query['other_param'] == '1'


@pytest.mark.usefixtures("mock_calendars", "mock_events")
def test_calendar_events(api_client):
    calendar = api_client.calendars.first()
    assert calendar.events
    assert all(isinstance(event, Event)
               for event in calendar.events)

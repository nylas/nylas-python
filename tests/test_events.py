import json
from datetime import datetime
import pytest
from urlobject import URLObject
from requests import RequestException
from nylas.client.restful_models import Event


def blank_event(api_client):
    event = api_client.events.create()
    event.title = "Paris-Brest"
    event.calendar_id = "calendar_id"
    event.when = {"start_time": 1409594400, "end_time": 1409594400}
    return event


@pytest.mark.usefixtures("mock_event_create_response")
def test_event_crud(api_client):
    event1 = blank_event(api_client)
    event1.save()
    assert event1.id == "cv4ei7syx10uvsxbs21ccsezf"

    event1.title = "blah"
    event1.save()
    assert event1.title == "loaded from JSON"
    assert event1.get("ignored") is None

    # Third time should fail.
    event2 = blank_event(api_client)
    with pytest.raises(RequestException):
        event2.save()


@pytest.mark.usefixtures("mock_event_create_notify_response")
def test_event_notify(mocked_responses, api_client):
    event1 = blank_event(api_client)
    event1.save(notify_participants="true", other_param="1")
    assert event1.id == "cv4ei7syx10uvsxbs21ccsezf"

    url = mocked_responses.calls[-1].request.url
    query = URLObject(url).query_dict
    assert query["notify_participants"] == "true"
    assert query["other_param"] == "1"


@pytest.mark.usefixtures("mock_calendars", "mock_events")
def test_calendar_events(api_client):
    calendar = api_client.calendars.first()
    assert calendar.events
    assert all(isinstance(event, Event) for event in calendar.events)


@pytest.mark.usefixtures("mock_events", "mock_send_rsvp")
def test_event(mocked_responses, api_client):
    event = api_client.events.first()
    event.rsvp("yes")

    request = mocked_responses.calls[-1].request
    assert URLObject(request.url).path == "/send-rsvp"
    data = json.loads(request.body)
    assert data["event_id"] == event.id
    assert data["status"] == "yes"
    assert data["comment"] == None


@pytest.mark.usefixtures("mock_events", "mock_send_rsvp")
def test_event_rsvp_with_comment(mocked_responses, api_client):
    event = api_client.events.first()
    event.rsvp("no", "I have a conflict")

    request = mocked_responses.calls[-1].request
    assert URLObject(request.url).path == "/send-rsvp"
    data = json.loads(request.body)
    assert data["event_id"] == event.id
    assert data["status"] == "no"
    assert data["comment"] == "I have a conflict"


@pytest.mark.usefixtures("mock_events")
def test_event_rsvp_invalid(api_client):
    event = api_client.events.first()
    with pytest.raises(ValueError) as excinfo:
        event.rsvp("purple")
    assert "invalid status" in str(excinfo)


@pytest.mark.usefixtures("mock_events")
def test_event_rsvp_no_message(api_client):
    event = api_client.events.all()[1]
    with pytest.raises(ValueError) as excinfo:
        event.rsvp("yes")
    assert "This event was not imported from an iCalendar invite" in str(excinfo)


@pytest.mark.usefixtures("mock_free_busy")
def test_free_busy_datetime(mocked_responses, api_client):
    email = "fake@example.com"
    start_at = datetime(2020, 1, 1)
    end_at = datetime(2020, 1, 2)
    free_busy = api_client.free_busy([email], start_at, end_at)

    assert isinstance(free_busy, list)
    assert isinstance(free_busy[0], dict)
    assert free_busy[0]["email"] == "fake@example.com"
    assert "time_slots" in free_busy[0]

    request = mocked_responses.calls[-1].request
    assert URLObject(request.url).path == "/calendars/free-busy"
    data = json.loads(request.body)
    assert data["emails"] == [email]
    assert data["start_time"] == 1577836800
    assert data["end_time"] == 1577923200


@pytest.mark.usefixtures("mock_free_busy")
def test_free_busy_timestamp(mocked_responses, api_client):
    email = "ron@example.com"
    start_time = 1580511600
    end_time = 1580598000
    free_busy = api_client.free_busy([email], start_time, end_time)

    assert isinstance(free_busy, list)
    assert isinstance(free_busy[0], dict)
    assert free_busy[0]["email"] == "ron@example.com"
    assert "time_slots" in free_busy[0]

    request = mocked_responses.calls[-1].request
    assert URLObject(request.url).path == "/calendars/free-busy"
    data = json.loads(request.body)
    assert data["emails"] == [email]
    assert data["start_time"] == 1580511600
    assert data["end_time"] == 1580598000


@pytest.mark.usefixtures("mock_free_busy")
def test_free_busy_single_email(mocked_responses, api_client):
    email = "ben@bitdiddle.com"
    start_at = datetime(2000, 1, 1)
    end_at = datetime(2000, 3, 1)
    free_busy = api_client.free_busy(email, start_at, end_at)

    assert isinstance(free_busy, list)
    assert isinstance(free_busy[0], dict)
    assert free_busy[0]["email"] == "ben@bitdiddle.com"
    assert "time_slots" in free_busy[0]

    request = mocked_responses.calls[-1].request
    assert URLObject(request.url).path == "/calendars/free-busy"
    data = json.loads(request.body)
    assert data["emails"] == [email]
    assert data["start_time"] == 946684800
    assert data["end_time"] == 951868800

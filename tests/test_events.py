import json
from datetime import datetime, timedelta
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


@pytest.mark.usefixtures("mock_event_create_notify_response")
def test_event_notify(mocked_responses, api_client):
    event1 = blank_event(api_client)
    event1.save(notify_participants="true", other_param="1")
    assert event1.id == "cv4ei7syx10uvsxbs21ccsezf"

    url = mocked_responses.calls[-1].request.url
    query = URLObject(url).query_dict
    assert query["notify_participants"] == "true"
    assert query["other_param"] == "1"


@pytest.mark.usefixtures("mock_event_create_response")
def test_event_conferencing_details(mocked_responses, api_client):
    event = blank_event(api_client)
    event.conferencing = {
        "provider": "Zoom Meeting",
        "details": {
            "url": "https://us02web.zoom.us/j/****************",
            "meeting_code": "213",
            "password": "xyz",
            "phone": ["+11234567890"],
        },
    }
    event.save()
    assert event.id == "cv4ei7syx10uvsxbs21ccsezf"
    assert event.conferencing["provider"] == "Zoom Meeting"
    assert (
        event.conferencing["details"]["url"]
        == "https://us02web.zoom.us/j/****************"
    )
    assert event.conferencing["details"]["meeting_code"] == "213"
    assert event.conferencing["details"]["password"] == "xyz"
    assert event.conferencing["details"]["phone"] == ["+11234567890"]

    body = json.loads(mocked_responses.calls[-1].request.body)
    assert body["conferencing"]["provider"] == "Zoom Meeting"
    assert (
        body["conferencing"]["details"]["url"]
        == "https://us02web.zoom.us/j/****************"
    )
    assert body["conferencing"]["details"]["meeting_code"] == "213"
    assert body["conferencing"]["details"]["password"] == "xyz"
    assert body["conferencing"]["details"]["phone"] == ["+11234567890"]


@pytest.mark.usefixtures("mock_event_create_response")
def test_event_conferencing_autocreate(mocked_responses, api_client):
    event = blank_event(api_client)
    event.conferencing = {
        "provider": "Zoom Meeting",
        "autocreate": {
            "settings": {},
        },
    }
    event.save()
    assert event.id == "cv4ei7syx10uvsxbs21ccsezf"
    assert event.conferencing["provider"] == "Zoom Meeting"
    assert event.conferencing["autocreate"]["settings"] == {}

    body = json.loads(mocked_responses.calls[-1].request.body)
    assert body["conferencing"]["provider"] == "Zoom Meeting"
    assert event.conferencing["autocreate"]["settings"] == {}


@pytest.mark.usefixtures("mock_event_create_response")
def test_event_conferencing_details_autocreate_error(mocked_responses, api_client):
    event = blank_event(api_client)
    event.conferencing = {
        "provider": "Zoom Meeting",
        "details": {
            "url": "https://us02web.zoom.us/j/****************",
            "meeting_code": "213",
            "password": "xyz",
            "phone": ["+11234567890"],
        },
        "autocreate": {
            "settings": {
                "password": "1234",
            },
        },
    }
    with pytest.raises(ValueError) as excinfo:
        event.save()
    assert "Cannot set both 'details' and 'autocreate' in conferencing object." in str(
        excinfo
    )


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


@pytest.mark.usefixtures("mock_availability")
def test_availability_datetime(mocked_responses, api_client):
    emails = ["one@example.com", "two@example.com", "three@example.com"]
    duration = timedelta(minutes=30)
    interval = timedelta(hours=1, minutes=30)
    start_at = datetime(2020, 1, 1)
    end_at = datetime(2020, 1, 2)
    availability = api_client.availability(emails, duration, interval, start_at, end_at)

    assert isinstance(availability, dict)
    assert "time_slots" in availability

    request = mocked_responses.calls[-1].request
    assert URLObject(request.url).path == "/calendars/availability"
    data = json.loads(request.body)
    assert data["emails"] == emails
    assert data["duration_minutes"] == 30
    assert isinstance(data["duration_minutes"], int)
    assert data["interval_minutes"] == 90
    assert isinstance(data["interval_minutes"], int)
    assert data["start_time"] == 1577836800
    assert data["end_time"] == 1577923200
    assert data["free_busy"] == []


@pytest.mark.usefixtures("mock_availability")
def test_availability_timestamp(mocked_responses, api_client):
    emails = ["one@example.com", "two@example.com", "three@example.com"]
    duration = 30
    interval = 60
    start_time = 1580511600
    end_time = 1580598000
    availability = api_client.availability(
        emails, duration, interval, start_time, end_time
    )

    assert isinstance(availability, dict)
    assert "time_slots" in availability

    request = mocked_responses.calls[-1].request
    assert URLObject(request.url).path == "/calendars/availability"
    data = json.loads(request.body)
    assert data["emails"] == emails
    assert data["duration_minutes"] == 30
    assert isinstance(data["duration_minutes"], int)
    assert data["interval_minutes"] == 60
    assert isinstance(data["interval_minutes"], int)
    assert data["start_time"] == 1580511600
    assert data["end_time"] == 1580598000
    assert data["free_busy"] == []


@pytest.mark.usefixtures("mock_availability")
def test_availability_single_email(mocked_responses, api_client):
    email = "ben@bitdiddle.com"
    duration = timedelta(minutes=60)
    interval = 5
    start_at = datetime(2000, 1, 1)
    end_at = datetime(2000, 3, 1)
    availability = api_client.availability(email, duration, interval, start_at, end_at)

    assert isinstance(availability, dict)
    assert "time_slots" in availability

    request = mocked_responses.calls[-1].request
    assert URLObject(request.url).path == "/calendars/availability"
    data = json.loads(request.body)
    assert data["emails"] == [email]
    assert data["duration_minutes"] == 60
    assert isinstance(data["duration_minutes"], int)
    assert data["interval_minutes"] == 5
    assert isinstance(data["interval_minutes"], int)
    assert data["start_time"] == 946684800
    assert data["end_time"] == 951868800
    assert data["free_busy"] == []


@pytest.mark.usefixtures("mock_availability")
def test_availability_with_free_busy(mocked_responses, api_client):
    emails = [
        "one@example.com",
        "two@example.com",
        "three@example.com",
        "visitor@external.net",
    ]
    duration = 48
    interval = timedelta(minutes=18)
    start_at = datetime(2020, 1, 1)
    end_at = datetime(2020, 1, 2)
    free_busy = [
        {
            "email": "visitor@external.net",
            "time_slots": [
                {
                    "object": "time_slot",
                    "status": "busy",
                    "start_time": 1584377898,
                    "end_time": 1584379800,
                }
            ],
            "object": "free_busy",
        }
    ]
    availability = api_client.availability(
        emails, duration, interval, start_at, end_at, free_busy=free_busy
    )

    assert isinstance(availability, dict)
    assert "time_slots" in availability

    request = mocked_responses.calls[-1].request
    assert URLObject(request.url).path == "/calendars/availability"
    data = json.loads(request.body)
    assert data["emails"] == emails
    assert data["duration_minutes"] == 48
    assert isinstance(data["duration_minutes"], int)
    assert data["interval_minutes"] == 18
    assert isinstance(data["interval_minutes"], int)
    assert data["start_time"] == 1577836800
    assert data["end_time"] == 1577923200
    assert data["free_busy"] == free_busy


@pytest.mark.usefixtures("mock_availability")
def test_consecutive_availability(mocked_responses, api_client):
    emails = [["one@example.com"], ["two@example.com", "three@example.com"]]
    duration = timedelta(minutes=30)
    interval = timedelta(hours=1, minutes=30)
    start_at = datetime(2020, 1, 1)
    end_at = datetime(2020, 1, 2)
    open_hours = api_client.open_hours(
        ["one@example.com", "two@example.com", "three@example.com"],
        [0],
        "America/Chicago",
        "10:00",
        "14:00",
    )
    api_client.consecutive_availability(
        emails, duration, interval, start_at, end_at, open_hours=[open_hours]
    )

    request = mocked_responses.calls[-1].request
    assert URLObject(request.url).path == "/calendars/availability/consecutive"
    data = json.loads(request.body)
    assert data["emails"] == emails
    assert data["duration_minutes"] == 30
    assert isinstance(data["duration_minutes"], int)
    assert data["interval_minutes"] == 90
    assert isinstance(data["interval_minutes"], int)
    assert data["start_time"] == 1577836800
    assert data["end_time"] == 1577923200
    assert data["free_busy"] == []
    assert data["open_hours"][0]["emails"] == [
        "one@example.com",
        "two@example.com",
        "three@example.com",
    ]
    assert data["open_hours"][0]["days"] == [0]
    assert data["open_hours"][0]["timezone"] == "America/Chicago"
    assert data["open_hours"][0]["start"] == "10:00"
    assert data["open_hours"][0]["end"] == "14:00"


@pytest.mark.usefixtures("mock_availability")
def test_consecutive_availability_free_busy(mocked_responses, api_client):
    emails = [["one@example.com"], ["two@example.com", "three@example.com"]]
    duration = timedelta(minutes=30)
    interval = timedelta(hours=1, minutes=30)
    start_at = datetime(2020, 1, 1)
    end_at = datetime(2020, 1, 2)
    open_hours = api_client.open_hours(
        [
            "one@example.com",
            "two@example.com",
            "three@example.com",
            "visitor@external.net",
        ],
        [0],
        "America/Chicago",
        "10:00",
        "14:00",
    )
    free_busy = [
        {
            "email": "visitor@external.net",
            "time_slots": [
                {
                    "object": "time_slot",
                    "status": "busy",
                    "start_time": 1584377898,
                    "end_time": 1584379800,
                }
            ],
            "object": "free_busy",
        }
    ]
    api_client.consecutive_availability(
        emails,
        duration,
        interval,
        start_at,
        end_at,
        free_busy=free_busy,
        open_hours=[open_hours],
    )

    request = mocked_responses.calls[-1].request
    assert URLObject(request.url).path == "/calendars/availability/consecutive"
    data = json.loads(request.body)
    assert data["emails"] == emails
    assert data["duration_minutes"] == 30
    assert isinstance(data["duration_minutes"], int)
    assert data["interval_minutes"] == 90
    assert isinstance(data["interval_minutes"], int)
    assert data["start_time"] == 1577836800
    assert data["end_time"] == 1577923200
    assert data["free_busy"] == free_busy
    assert data["open_hours"][0]["emails"] == [
        "one@example.com",
        "two@example.com",
        "three@example.com",
        "visitor@external.net",
    ]
    assert data["open_hours"][0]["days"] == [0]
    assert data["open_hours"][0]["timezone"] == "America/Chicago"
    assert data["open_hours"][0]["start"] == "10:00"
    assert data["open_hours"][0]["end"] == "14:00"


@pytest.mark.usefixtures("mock_availability")
def test_consecutive_availability_invalid_open_hours_email(
    mocked_responses, api_client
):
    emails = [["one@example.com"], ["two@example.com", "three@example.com"]]
    duration = timedelta(minutes=30)
    interval = timedelta(hours=1, minutes=30)
    start_at = datetime(2020, 1, 1)
    end_at = datetime(2020, 1, 2)
    open_hours = api_client.open_hours(
        [
            "one@example.com",
            "two@example.com",
            "three@example.com",
            "visitor@external.net",
            "four@example.com",
        ],
        [0],
        "America/Chicago",
        "10:00",
        "14:00",
    )
    free_busy = [
        {
            "email": "visitor@external.net",
            "time_slots": [
                {
                    "object": "time_slot",
                    "status": "busy",
                    "start_time": 1584377898,
                    "end_time": 1584379800,
                }
            ],
            "object": "free_busy",
        }
    ]
    with pytest.raises(ValueError):
        api_client.consecutive_availability(
            emails,
            duration,
            interval,
            start_at,
            end_at,
            free_busy=free_busy,
            open_hours=[open_hours],
        )


@pytest.mark.usefixtures("mock_events")
def test_metadata_filtering(api_client):
    events_filtered_by_key = api_client.events.where(metadata_key="platform")
    assert len(events_filtered_by_key.all()) > 0
    for event in events_filtered_by_key:
        assert "platform" in event["metadata"]

    events_filtered_by_value = api_client.events.where(
        metadata_value=["meeting", "java"]
    )
    assert len(events_filtered_by_value.all()) > 0
    for event in events_filtered_by_value:
        assert event["metadata"]["event_type"] == "meeting"

    events_filtered_by_pair = api_client.events.where(
        metadata_pair={"platform": "python", "bla": "blablabla"}
    )
    assert len(events_filtered_by_pair.all()) > 0
    for event in events_filtered_by_pair:
        assert "platform" in event["metadata"]
        assert event["metadata"]["platform"] == "python"

    non_existant_event = api_client.events.where(metadata_pair={"bla": "blablabla"})
    assert len(non_existant_event.all()) == 0


@pytest.mark.usefixtures("mock_event_create_response")
def test_event_notifications(mocked_responses, api_client):
    event = blank_event(api_client)
    event.notifications = [
        {
            "type": "email",
            "minutes_before_event": 60,
            "subject": "Test Event Notification",
            "body": "Reminding you about our meeting.",
        }
    ]
    event.save()
    assert event.id == "cv4ei7syx10uvsxbs21ccsezf"
    assert len(event.notifications) == 1
    assert event.notifications[0]["type"] == "email"
    assert event.notifications[0]["minutes_before_event"] == 60
    assert event.notifications[0]["subject"] == "Test Event Notification"
    assert event.notifications[0]["body"] == "Reminding you about our meeting."


@pytest.mark.usefixtures("mock_event_create_response", "mock_event_generate_ics")
def test_generate_ics_existing_event(mocked_responses, api_client):
    event = blank_event(api_client)
    event.save()
    ics = event.generate_ics()
    ics_request = mocked_responses.calls[1].request
    assert len(mocked_responses.calls) == 2
    assert event.id == "cv4ei7syx10uvsxbs21ccsezf"
    assert ics_request.path_url == "/events/to-ics"
    assert ics_request.method == "POST"
    assert json.loads(ics_request.body) == {"event_id": "cv4ei7syx10uvsxbs21ccsezf"}


@pytest.mark.usefixtures("mock_event_create_response", "mock_event_generate_ics")
def test_generate_ics_no_event_id(mocked_responses, api_client):
    event = blank_event(api_client)
    ics = event.generate_ics()
    ics_request = mocked_responses.calls[0].request
    assert len(mocked_responses.calls) == 1
    assert event.id is None
    assert ics_request.path_url == "/events/to-ics"
    assert ics_request.method == "POST"
    assert json.loads(ics_request.body) == {
        "calendar_id": "calendar_id",
        "title": "Paris-Brest",
        "when": {"end_time": 1409594400, "start_time": 1409594400},
    }


@pytest.mark.usefixtures("mock_event_create_response", "mock_event_generate_ics")
def test_generate_ics_options(mocked_responses, api_client):
    event = blank_event(api_client)
    event.save()
    ics = event.generate_ics(
        ical_uid="test_uuid", method="request", prodid="test_prodid"
    )
    ics_request = mocked_responses.calls[1].request
    assert len(mocked_responses.calls) == 2
    assert event.id == "cv4ei7syx10uvsxbs21ccsezf"
    assert ics_request.path_url == "/events/to-ics"
    assert ics_request.method == "POST"
    assert json.loads(ics_request.body) == {
        "event_id": "cv4ei7syx10uvsxbs21ccsezf",
        "ics_options": {
            "ical_uid": "test_uuid",
            "method": "request",
            "prodid": "test_prodid",
        },
    }


@pytest.mark.usefixtures("mock_event_create_response", "mock_event_generate_ics")
def test_generate_ics_no_calendar_id_throws(mocked_responses, api_client):
    event = blank_event(api_client)
    del event.calendar_id
    with pytest.raises(ValueError) as exc:
        event.generate_ics()

    assert str(exc.value) == (
        "Cannot generate an ICS file for an event without a Calendar ID or when set"
    )


@pytest.mark.usefixtures("mock_event_create_response", "mock_event_generate_ics")
def test_generate_ics_no_when_throws(mocked_responses, api_client):
    event = blank_event(api_client)
    del event.when
    with pytest.raises(ValueError) as exc:
        event.generate_ics()

    assert str(exc.value) == (
        "Cannot generate an ICS file for an event without a Calendar ID or when set"
    )

import json
from datetime import datetime
import pytest
import responses

from nylas.client.restful_models import Scheduler, Calendar
from nylas.client.scheduler_models import SchedulerTimeSlot, SchedulerBookingRequest


def blank_scheduler_page(api_client):
    scheduler = api_client.scheduler.create()
    scheduler.access_tokens = ["test-access-token"]
    scheduler.name = "Python SDK Example"
    scheduler.slug = "py_example_1"
    return scheduler


def test_scheduler_endpoint(api_client):
    scheduler = api_client.scheduler
    assert scheduler.api.api_server == "https://api.schedule.nylas.com"


@pytest.mark.usefixtures("mock_schedulers")
def test_scheduler(api_client):
    scheduler = api_client.scheduler.first()
    assert isinstance(scheduler, Scheduler)
    assert scheduler.id == 90210
    assert scheduler.app_client_id == "test-client-id"
    assert scheduler.app_organization_id == 12345
    assert len(scheduler.config) == 4
    assert isinstance(scheduler.config, dict)
    assert scheduler.config["locale"] == "en"
    assert len(scheduler.config["reminders"]) == 0
    assert scheduler.config["timezone"] == "America/Los_Angeles"
    assert scheduler.edit_token == "test-edit-token-1"
    assert scheduler.name == "test-1"
    assert scheduler.slug == "test1"
    assert scheduler.created_at == datetime.strptime("2021-10-22", "%Y-%m-%d").date()
    assert scheduler.modified_at == datetime.strptime("2021-10-22", "%Y-%m-%d").date()


@pytest.mark.usefixtures("mock_scheduler_create_response")
def test_create_scheduler(api_client):
    scheduler = blank_scheduler_page(api_client)
    scheduler.save()
    assert scheduler.id == "cv4ei7syx10uvsxbs21ccsezf"


@pytest.mark.usefixtures("mock_scheduler_create_response")
def test_modify_scheduler(api_client):
    scheduler = blank_scheduler_page(api_client)
    scheduler.id = "cv4ei7syx10uvsxbs21ccsezf"
    scheduler.name = "Updated Name"
    scheduler.save()
    assert scheduler.name == "Updated Name"


@pytest.mark.usefixtures("mock_scheduler_get_available_calendars")
def test_scheduler_get_available_calendars(api_client):
    scheduler = blank_scheduler_page(api_client)
    scheduler.id = "cv4ei7syx10uvsxbs21ccsezf"
    calendars = scheduler.get_available_calendars()
    assert len(calendars) == 1
    calendar = calendars[0]
    assert len(calendar["calendars"]) == 1
    assert isinstance(calendar["calendars"][0], Calendar)
    assert calendar["calendars"][0].id == "calendar-id"
    assert calendar["calendars"][0].name == "Emailed events"
    assert calendar["calendars"][0].read_only
    assert calendar["email"] == "swag@nylas.com"
    assert calendar["id"] == "scheduler-id"
    assert calendar["name"] == "Python Tester"


@pytest.mark.usefixtures("mock_scheduler_get_available_calendars")
def test_scheduler_get_available_calendars_no_id_throws_error(api_client):
    scheduler = blank_scheduler_page(api_client)
    with pytest.raises(ValueError):
        scheduler.get_available_calendars()


@pytest.mark.usefixtures("mock_scheduler_upload_image")
def test_scheduler_upload_image(api_client):
    scheduler = blank_scheduler_page(api_client)
    scheduler.id = "cv4ei7syx10uvsxbs21ccsezf"
    upload = scheduler.upload_image("image/png", "test.png")
    assert upload["filename"] == "test.png"
    assert upload["originalFilename"] == "test.png"
    assert upload["publicUrl"] == "https://public.nylas.com/test.png"
    assert upload["signedUrl"] == "https://signed.nylas.com/test.png"


@pytest.mark.usefixtures("mock_scheduler_get_available_calendars")
def test_scheduler_get_available_calendars_no_id_throws_error(api_client):
    scheduler = blank_scheduler_page(api_client)
    with pytest.raises(ValueError):
        scheduler.upload_image("image/png", "test.png")


@pytest.mark.usefixtures("mock_scheduler_provider_availability")
def test_scheduler_get_google_availability(mocked_responses, api_client):
    api_client.scheduler.get_google_availability()
    request = mocked_responses.calls[0].request
    assert request.url == "https://api.schedule.nylas.com/schedule/availability/google"
    assert request.method == responses.GET


@pytest.mark.usefixtures("mock_scheduler_provider_availability")
def test_scheduler_get_o365_availability(mocked_responses, api_client):
    api_client.scheduler.get_office_365_availability()
    request = mocked_responses.calls[0].request
    assert request.url == "https://api.schedule.nylas.com/schedule/availability/o365"
    assert request.method == responses.GET


@pytest.mark.usefixtures("mock_schedulers")
def test_scheduler_get_page_slug(mocked_responses, api_client):
    scheduler = api_client.scheduler.get_page_slug("test1")
    request = mocked_responses.calls[0].request
    assert request.url == "https://api.schedule.nylas.com/schedule/test1/info"
    assert request.method == responses.GET
    assert isinstance(scheduler, Scheduler)
    assert scheduler.id == 90210
    assert scheduler.app_client_id == "test-client-id"
    assert scheduler.app_organization_id == 12345
    assert len(scheduler.config) == 4
    assert isinstance(scheduler.config, dict)
    assert scheduler.config["locale"] == "en"
    assert len(scheduler.config["reminders"]) == 0
    assert scheduler.config["timezone"] == "America/Los_Angeles"
    assert scheduler.edit_token == "test-edit-token-1"
    assert scheduler.name == "test-1"
    assert scheduler.slug == "test1"
    assert scheduler.created_at == datetime.strptime("2021-10-22", "%Y-%m-%d").date()
    assert scheduler.modified_at == datetime.strptime("2021-10-22", "%Y-%m-%d").date()


@pytest.mark.usefixtures("mock_scheduler_timeslots")
def test_scheduler_get_available_time_slots(mocked_responses, api_client):
    scheduler = blank_scheduler_page(api_client)
    timeslots = api_client.scheduler.get_available_time_slots(scheduler.slug)
    request = mocked_responses.calls[0].request
    assert (
        request.url == "https://api.schedule.nylas.com/schedule/py_example_1/timeslots"
    )
    assert request.method == responses.GET
    assert len(timeslots) == 1
    assert timeslots[0]
    assert timeslots[0].account_id == "test-account-id"
    assert timeslots[0].calendar_id == "test-calendar-id"
    assert timeslots[0].emails[0] == "test@example.com"
    assert timeslots[0].host_name == "www.hostname.com"
    assert timeslots[0].end == datetime.utcfromtimestamp(1636731958)
    assert timeslots[0].start == datetime.utcfromtimestamp(1636728347)


@pytest.mark.usefixtures("mock_scheduler_timeslots")
def test_scheduler_get_available_time_slots(mocked_responses, api_client):
    scheduler = blank_scheduler_page(api_client)
    timeslots = api_client.scheduler.get_available_time_slots(scheduler.slug)
    request = mocked_responses.calls[0].request
    assert (
        request.url == "https://api.schedule.nylas.com/schedule/py_example_1/timeslots"
    )
    assert request.method == responses.GET
    assert len(timeslots) == 1
    assert timeslots[0]
    assert timeslots[0].account_id == "test-account-id"
    assert timeslots[0].calendar_id == "test-calendar-id"
    assert timeslots[0].emails[0] == "test@example.com"
    assert timeslots[0].host_name == "www.hostname.com"
    assert timeslots[0].end == datetime.utcfromtimestamp(1636731958)
    assert timeslots[0].start == datetime.utcfromtimestamp(1636728347)


@pytest.mark.usefixtures("mock_scheduler_timeslots")
def test_scheduler_book_time_slot(mocked_responses, api_client):
    scheduler = blank_scheduler_page(api_client)
    slot = SchedulerTimeSlot.create(api_client)
    slot.account_id = "test-account-id"
    slot.calendar_id = "test-calendar-id"
    slot.emails = ["recipient@example.com"]
    slot.host_name = "www.nylas.com"
    slot.start = datetime.utcfromtimestamp(1636728347)
    slot.end = datetime.utcfromtimestamp(1636731958)
    timeslot_to_book = SchedulerBookingRequest.create(api_client)
    timeslot_to_book.additional_values = {
        "test": "yes",
    }
    timeslot_to_book.email = "recipient@example.com"
    timeslot_to_book.locale = "en_US"
    timeslot_to_book.name = "Recipient Doe"
    timeslot_to_book.timezone = "America/New_York"
    timeslot_to_book.slot = slot
    booking_response = api_client.scheduler.book_time_slot(
        scheduler.slug, timeslot_to_book
    )
    request = mocked_responses.calls[0].request
    assert (
        request.url == "https://api.schedule.nylas.com/schedule/py_example_1/timeslots"
    )
    assert request.method == responses.POST
    assert json.loads(request.body) == {
        "additional_emails": [],
        "additional_values": {
            "test": "yes",
        },
        "email": "recipient@example.com",
        "locale": "en_US",
        "name": "Recipient Doe",
        "timezone": "America/New_York",
        "slot": {
            "account_id": "test-account-id",
            "calendar_id": "test-calendar-id",
            "emails": ["recipient@example.com"],
            "host_name": "www.nylas.com",
            "start": 1636728347,
            "end": 1636731958,
        },
    }
    assert booking_response.account_id == "test-account-id"
    assert booking_response.calendar_id == "test-calendar-id"
    assert booking_response.additional_field_values == {
        "test": "yes",
    }
    assert booking_response.calendar_event_id == "test-event-id"
    assert booking_response.calendar_id == "test-calendar-id"
    assert booking_response.calendar_event_id == "test-event-id"
    assert booking_response.edit_hash == "test-edit-hash"
    assert booking_response.id == 123
    assert booking_response.is_confirmed is False
    assert booking_response.location == "Earth"
    assert booking_response.title == "Test Booking"
    assert booking_response.recipient_email == "recipient@example.com"
    assert booking_response.recipient_locale == "en_US"
    assert booking_response.recipient_name == "Recipient Doe"
    assert booking_response.recipient_tz == "America/New_York"
    assert booking_response.end_time == datetime.utcfromtimestamp(1636731958)
    assert booking_response.start_time == datetime.utcfromtimestamp(1636728347)


@pytest.mark.usefixtures("mock_scheduler_timeslots")
def test_scheduler_confirm_booking(mocked_responses, api_client):
    scheduler = blank_scheduler_page(api_client)
    booking_confirmation = api_client.scheduler.confirm_booking(
        scheduler.slug, "test-edit-hash"
    )
    request = mocked_responses.calls[0].request
    assert (
        request.url
        == "https://api.schedule.nylas.com/schedule/py_example_1/test-edit-hash/confirm"
    )
    assert request.method == responses.POST
    assert booking_confirmation.account_id == "test-account-id"
    assert booking_confirmation.calendar_id == "test-calendar-id"
    assert booking_confirmation.additional_field_values == {
        "test": "yes",
    }
    assert booking_confirmation.calendar_event_id == "test-event-id"
    assert booking_confirmation.calendar_id == "test-calendar-id"
    assert booking_confirmation.calendar_event_id == "test-event-id"
    assert booking_confirmation.edit_hash == "test-edit-hash"
    assert booking_confirmation.id == 123
    assert booking_confirmation.is_confirmed is True
    assert booking_confirmation.location == "Earth"
    assert booking_confirmation.title == "Test Booking"
    assert booking_confirmation.recipient_email == "recipient@example.com"
    assert booking_confirmation.recipient_locale == "en_US"
    assert booking_confirmation.recipient_name == "Recipient Doe"
    assert booking_confirmation.recipient_tz == "America/New_York"
    assert booking_confirmation.end_time == datetime.utcfromtimestamp(1636731958)
    assert booking_confirmation.start_time == datetime.utcfromtimestamp(1636728347)


@pytest.mark.usefixtures("mock_scheduler_timeslots")
def test_scheduler_cancel_booking(mocked_responses, api_client):
    scheduler = blank_scheduler_page(api_client)
    timeslots = api_client.scheduler.cancel_booking(
        scheduler.slug, "test-edit-hash", "It was a test."
    )
    request = mocked_responses.calls[0].request
    assert (
        request.url
        == "https://api.schedule.nylas.com/schedule/py_example_1/test-edit-hash/cancel"
    )
    assert request.method == responses.POST
    assert json.loads(request.body) == {"reason": "It was a test."}

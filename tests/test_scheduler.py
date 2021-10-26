from datetime import datetime, timedelta
import pytest
from nylas.client.restful_models import Event, Scheduler, Calendar


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

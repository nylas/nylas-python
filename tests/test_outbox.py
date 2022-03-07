from datetime import datetime, timedelta
import json

import pytest
from urlobject import URLObject

from nylas.utils import timestamp_from_dt


@pytest.mark.usefixtures("mock_outbox")
def test_outbox_send(mocked_responses, api_client):
    draft, tomorrow, day_after = prepare_outbox_request(api_client)

    job_status = api_client.outbox.send(draft, tomorrow, retry_limit_datetime=day_after)

    request = mocked_responses.calls[0].request
    assert URLObject(request.url).path == "/v2/outbox"
    assert request.method == "POST"
    body = json.loads(request.body)
    evaluate_message(body, tomorrow, day_after)
    assert job_status["job_status_id"] == "job-status-id"
    assert job_status["status"] == "pending"
    assert job_status["account_id"] == "account-id"
    original_data = job_status["original_data"]
    evaluate_message(original_data, tomorrow, day_after)
    assert original_data["original_send_at"] == timestamp_from_dt(tomorrow)


@pytest.mark.usefixtures("mock_outbox")
def test_outbox_update(mocked_responses, api_client):
    draft, tomorrow, day_after = prepare_outbox_request(api_client)

    api_client.outbox.update(
        "job-status-id", draft=draft, send_at=tomorrow, retry_limit_datetime=day_after
    )

    request = mocked_responses.calls[0].request
    assert URLObject(request.url).path == "/v2/outbox/job-status-id"
    assert request.method == "PATCH"
    body = json.loads(request.body)
    evaluate_message(body, tomorrow, day_after)


@pytest.mark.usefixtures("mock_outbox")
def test_outbox_send_at_before_today_should_raise(mocked_responses, api_client):
    with pytest.raises(ValueError) as excinfo:
        api_client.outbox._validate_and_format_datetime(636309514, None)
    assert "Cannot set message to be sent at a time before the current time." in str(
        excinfo
    )


@pytest.mark.usefixtures("mock_outbox")
def test_outbox_retry_limit_datetime_before_send_at_should_raise(
    mocked_responses, api_client
):
    tomorrow = datetime.today() + timedelta(days=1)
    day_after = tomorrow + timedelta(days=1)
    with pytest.raises(ValueError) as excinfo:
        api_client.outbox._validate_and_format_datetime(
            send_at=day_after, retry_limit_datetime=tomorrow
        )
    assert "Cannot set message to stop retrying before time to send at." in str(excinfo)


@pytest.mark.usefixtures("mock_outbox")
def test_outbox_retry_limit_datetime_before_today_should_raise(
    mocked_responses, api_client
):
    with pytest.raises(ValueError) as excinfo:
        api_client.outbox._validate_and_format_datetime(None, 636309514)
    assert "Cannot set message to stop retrying before time to send at." in str(excinfo)


@pytest.mark.usefixtures("mock_outbox")
def test_outbox_delete(mocked_responses, api_client):
    api_client.outbox.delete("job-status-id")

    request = mocked_responses.calls[0].request
    assert URLObject(request.url).path == "/v2/outbox/job-status-id"
    assert request.method == "DELETE"


@pytest.mark.usefixtures("mock_outbox_send_grid")
def test_outbox_send_grid_verification(mocked_responses, api_client):
    verification_status = api_client.outbox.send_grid_verification_status()

    request = mocked_responses.calls[0].request
    assert URLObject(request.url).path == "/v2/outbox/onboard/verified_status"
    assert request.method == "GET"
    assert verification_status.domain_verified is True
    assert verification_status.sender_verified is True


@pytest.mark.usefixtures("mock_outbox_send_grid")
def test_outbox_send_grid_verification(mocked_responses, api_client):
    api_client.outbox.delete_send_grid_sub_user("test@email.com")

    request = mocked_responses.calls[0].request
    assert URLObject(request.url).path == "/v2/outbox/onboard/subuser"
    assert request.method == "DELETE"


# Test helpers


def prepare_outbox_request(api_client):
    draft = api_client.drafts.create()
    draft.subject = "With Love, from Nylas"
    draft.to = [{"email": "test@email.com", "name": "Me"}]
    draft.body = "This email was sent using the Nylas email API. Visit https://nylas.com for details."
    tomorrow = datetime.today() + timedelta(days=1)
    day_after = tomorrow + timedelta(days=1)

    return draft, tomorrow, day_after


def evaluate_message(message, send_at, retry_limit_datetime):
    assert message["to"] == [{"email": "test@email.com", "name": "Me"}]
    assert message["subject"] == "With Love, from Nylas"
    assert (
        message["body"]
        == "This email was sent using the Nylas email API. Visit https://nylas.com for details."
    )
    assert message["send_at"] == timestamp_from_dt(send_at)
    assert message["retry_limit_datetime"] == timestamp_from_dt(retry_limit_datetime)

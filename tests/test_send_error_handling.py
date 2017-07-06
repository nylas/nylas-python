import json
import re
import pytest
import responses
from nylas.client.errors import (
    MessageRejectedError, SendingQuotaExceededError, ServiceUnavailableError,
)


def mock_sending_error(http_code, message, api_url, server_error=None):
    send_endpoint = re.compile(api_url + '/send')
    response_body = {
        "type": "api_error",
        "message": message
    }

    if server_error is not None:
        response_body['server_error'] = server_error

    response_body = json.dumps(response_body)
    responses.add(responses.POST, send_endpoint,
                  content_type='application/json', status=http_code,
                  body=response_body)


@responses.activate
@pytest.mark.usefixtures("mock_account", "mock_save_draft")
def test_handle_message_rejected(api_client, api_url):
    draft = api_client.drafts.create()
    error_message = 'Sending to all recipients failed'
    mock_sending_error(402, error_message, api_url=api_url)
    with pytest.raises(MessageRejectedError) as exc:
        draft.send()
    assert exc.value.message == error_message


@responses.activate
@pytest.mark.usefixtures("mock_account", "mock_save_draft")
def test_handle_quota_exceeded(api_client, api_url):
    draft = api_client.drafts.create()
    error_message = 'Daily sending quota exceeded'
    mock_sending_error(429, error_message, api_url=api_url)
    with pytest.raises(SendingQuotaExceededError) as exc:
        draft.send()
    assert exc.value.message == error_message


@responses.activate
@pytest.mark.usefixtures("mock_account", "mock_save_draft")
def test_handle_service_unavailable(api_client, api_url):
    draft = api_client.drafts.create()
    error_message = 'The server unexpectedly closed the connection'
    mock_sending_error(503, error_message, api_url=api_url)
    with pytest.raises(ServiceUnavailableError) as exc:
        draft.send()
    assert exc.value.message == error_message


@responses.activate
@pytest.mark.usefixtures("mock_account", "mock_save_draft")
def test_returns_server_error(api_client, api_url):
    draft = api_client.drafts.create()
    error_message = 'The server unexpectedly closed the connection'
    reason = 'Rejected potential SPAM'
    mock_sending_error(503, error_message, api_url=api_url,
                       server_error=reason)
    with pytest.raises(ServiceUnavailableError) as exc:
        draft.send()

    assert exc.value.message == error_message
    assert exc.value.server_error == reason


@responses.activate
@pytest.mark.usefixtures("mock_account", "mock_save_draft")
def test_doesnt_return_server_error_if_not_defined(api_client, api_url):
    draft = api_client.drafts.create()
    error_message = 'The server unexpectedly closed the connection'
    mock_sending_error(503, error_message, api_url=api_url)
    with pytest.raises(ServiceUnavailableError) as exc:
        draft.send()
    assert exc.value.message == error_message
    assert not hasattr(exc.value, 'server_error')

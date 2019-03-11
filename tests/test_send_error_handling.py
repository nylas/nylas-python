import json
import re
import pytest
import responses
import six
from requests import RequestException
from nylas.client.errors import MessageRejectedError


def mock_sending_error(
    http_code, message, mocked_responses, api_url, server_error=None
):
    send_endpoint = re.compile(api_url + "/send")
    response_body = {"type": "api_error", "message": message}

    if six.PY2 and http_code == 429:
        # Python 2 `httplib` doesn't know about status code 429
        six.moves.http_client.responses[429] = "Too Many Requests"

    if server_error is not None:
        response_body["server_error"] = server_error

    response_body = json.dumps(response_body)
    mocked_responses.add(
        responses.POST,
        send_endpoint,
        content_type="application/json",
        status=http_code,
        body=response_body,
    )


@pytest.mark.usefixtures("mock_account", "mock_save_draft")
def test_handle_message_rejected(mocked_responses, api_client, api_url):
    draft = api_client.drafts.create()
    error_message = "Sending to all recipients failed"
    mock_sending_error(402, error_message, mocked_responses, api_url=api_url)
    with pytest.raises(MessageRejectedError):
        draft.send()


@pytest.mark.usefixtures("mock_account", "mock_save_draft")
def test_handle_quota_exceeded(mocked_responses, api_client, api_url):
    draft = api_client.drafts.create()
    error_message = "Daily sending quota exceeded"
    mock_sending_error(429, error_message, mocked_responses, api_url=api_url)
    with pytest.raises(RequestException) as exc:
        draft.send()
    assert "Too Many Requests" in str(exc.value)


@pytest.mark.usefixtures("mock_account", "mock_save_draft")
def test_handle_service_unavailable(mocked_responses, api_client, api_url):
    draft = api_client.drafts.create()
    error_message = "The server unexpectedly closed the connection"
    mock_sending_error(503, error_message, mocked_responses, api_url=api_url)
    with pytest.raises(RequestException) as exc:
        draft.send()
    assert "Service Unavailable" in str(exc.value)


@pytest.mark.usefixtures("mock_account", "mock_save_draft")
def test_returns_server_error(mocked_responses, api_client, api_url):
    draft = api_client.drafts.create()
    error_message = "The server unexpectedly closed the connection"
    reason = "Rejected potential SPAM"
    mock_sending_error(
        503, error_message, mocked_responses, api_url=api_url, server_error=reason
    )
    with pytest.raises(RequestException) as exc:
        draft.send()

    assert "Service Unavailable" in str(exc.value)


@pytest.mark.usefixtures("mock_account", "mock_save_draft")
def test_doesnt_return_server_error_if_not_defined(
    mocked_responses, api_client, api_url
):
    draft = api_client.drafts.create()
    error_message = "The server unexpectedly closed the connection"
    mock_sending_error(503, error_message, mocked_responses, api_url=api_url)
    with pytest.raises(RequestException) as exc:
        draft.send()
    assert "Service Unavailable" in str(exc.value)

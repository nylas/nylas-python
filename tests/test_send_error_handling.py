import json
import re
import pytest
import responses
from nylas import APIClient
from nylas.client.errors import *

API_URL = 'http://localhost:2222'


def mock_sending_error(http_code, message):
    send_endpoint = re.compile(API_URL + '/send')
    response_body = json.dumps({
        "type": "api_error",
        "message": message
    })
    responses.add(responses.POST, send_endpoint,
                  content_type='application/json', status=http_code,
                  body=response_body)


@responses.activate
def test_handle_message_rejected(api_client, mock_account, mock_save_draft):
    draft = api_client.drafts.create()
    error_message = 'Sending to all recipients failed'
    mock_sending_error(402, error_message)
    with pytest.raises(MessageRejectedError) as exc:
        draft.send()
    assert exc.value.message == error_message


@responses.activate
def test_handle_quota_exceeded(api_client, mock_account, mock_save_draft):
    draft = api_client.drafts.create()
    error_message = 'Daily sending quota exceeded'
    mock_sending_error(429, error_message)
    with pytest.raises(SendingQuotaExceededError) as exc:
        draft.send()
    assert exc.value.message == error_message


@responses.activate
def test_handle_service_unavailable(api_client, mock_account,
                                    mock_save_draft):
    draft = api_client.drafts.create()
    error_message = 'The server unexpectedly closed the connection'
    mock_sending_error(503, error_message)
    with pytest.raises(ServiceUnavailableError) as exc:
        draft.send()
    assert exc.value.message == error_message

import json
import re
import pytest
import responses
from nylas import APIClient
from nylas.client.errors import *

API_URL = 'http://localhost:2222'


@pytest.fixture
def api_client():
    return APIClient(None, None, None, API_URL)


@pytest.fixture
def mock_namespace():
    response_body = json.dumps([
        {
            "account_id": "4ennivvrcgsqytgybfk912dto",
            "email_address": "ben.bitdiddle1861@gmail.com",
            "id": "4dl0ni6vxomazo73r5ozdo16j",
            "name": "Ben Bitdiddle",
            "namespace_id": "4dl0ni6vxomazo73r5ozdo16j",
            "object": "namespace",
            "provider": "gmail"
        }
    ])
    responses.add(responses.GET, API_URL + '/n?limit=1&offset=0',
                  content_type='application/json', status=200,
                  body=response_body, match_querystring=True)


@pytest.fixture
def mock_save_draft():
    save_endpoint = re.compile(API_URL + '/n/[(a-z)|(0-9)]+/drafts/')
    response_body = json.dumps({
        "id": "4dl0ni6vxomazo73r5oydo16k",
        "version": "4dw0ni6txomazo33r5ozdo16j"
    })
    responses.add(responses.POST, save_endpoint,
                  content_type='application/json', status=200,
                  body=response_body, match_querystring=True)


def mock_sending_error(http_code, message):
    send_endpoint = re.compile(API_URL + '/n/[(a-z)|(0-9)]+/send')
    response_body = json.dumps({
        "type": "api_error",
        "message": message
    })
    responses.add(responses.POST, send_endpoint,
                  content_type='application/json', status=http_code,
                  body=response_body)


@responses.activate
def test_handle_message_rejected(api_client, mock_namespace, mock_save_draft):
    namespace = api_client.namespaces.first()
    draft = namespace.drafts.create()
    error_message = 'Sending to all recipients failed'
    mock_sending_error(402, error_message)
    with pytest.raises(MessageRejectedError) as exc:
        draft.send()
    assert exc.value.message == error_message


@responses.activate
def test_handle_quota_exceeded(api_client, mock_namespace, mock_save_draft):
    namespace = api_client.namespaces.first()
    draft = namespace.drafts.create()
    error_message = 'Daily sending quota exceeded'
    mock_sending_error(429, error_message)
    with pytest.raises(SendingQuotaExceededError) as exc:
        draft.send()
    assert exc.value.message == error_message


@responses.activate
def test_handle_service_unavailable(api_client, mock_namespace,
                                    mock_save_draft):
    namespace = api_client.namespaces.first()
    draft = namespace.drafts.create()
    error_message = 'The server unexpectedly closed the connection'
    mock_sending_error(503, error_message)
    with pytest.raises(ServiceUnavailableError) as exc:
        draft.send()
    assert exc.value.message == error_message

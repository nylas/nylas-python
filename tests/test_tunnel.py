import json

import pytest
from urlobject import URLObject

from nylas.config import Region
from nylas.services import tunnel
from nylas.client.restful_models import Webhook


@pytest.mark.usefixtures("mock_create_webhook")
def test_build_webhook_tunnel(mocker, api_client_with_client_id):
    mocker.patch("websocket.WebSocketApp", mock_websocket)
    mocker.patch("uuid.uuid4", return_value="uuid")
    ws = tunnel._build_webhook_tunnel(
        api_client_with_client_id,
        {
            "region": Region.IRELAND,
            "triggers": [Webhook.Trigger.MESSAGE_CREATED],
            "on_open": on_open,
            "on_error": on_error,
            "on_close": on_close,
            "on_ping": on_ping,
            "on_pong": on_pong,
            "on_cont_message": on_cont_message,
            "on_data": on_data,
        },
    )
    assert ws["domain"] == "wss://tunnel.nylas.com"
    assert ws["header"] == {
        "Client-Id": "fake-client-id",
        "Client-Secret": "nyl4n4ut",
        "Tunnel-Id": "uuid",
        "Region": "ireland",
    }
    assert ws["on_open"] == on_open
    assert ws["on_error"] == on_error
    assert ws["on_close"] == on_close
    assert ws["on_ping"] == on_ping
    assert ws["on_pong"] == on_pong
    assert ws["on_cont_message"] == on_cont_message
    assert ws["on_data"] == on_data


@pytest.mark.usefixtures("mock_create_webhook")
def test_build_webhook_tunnel_defaults(mocker, api_client_with_client_id):
    mocker.patch("websocket.WebSocketApp", mock_websocket)
    mocker.patch("uuid.uuid4", return_value="uuid")
    ws = tunnel._build_webhook_tunnel(api_client_with_client_id, {})
    assert ws["domain"] == "wss://tunnel.nylas.com"
    assert ws["header"] == {
        "Client-Id": "fake-client-id",
        "Client-Secret": "nyl4n4ut",
        "Tunnel-Id": "uuid",
        "Region": "us",
    }
    assert ws["on_open"] is None
    assert ws["on_error"] is None
    assert ws["on_close"] is None
    assert ws["on_ping"] is None
    assert ws["on_pong"] is None
    assert ws["on_cont_message"] is None
    assert ws["on_data"] is None


@pytest.mark.usefixtures("mock_create_webhook")
def test_register_webhook(mocked_responses, api_client_with_client_id):
    tunnel._register_webhook(
        api_client_with_client_id,
        "domain.com",
        "tunnel_id",
        [Webhook.Trigger.MESSAGE_CREATED],
    )
    request = mocked_responses.calls[0].request
    assert URLObject(request.url).path == "/a/fake-client-id/webhooks"
    assert request.method == "POST"
    assert json.loads(request.body) == {
        "callback_url": "https://domain.com/tunnel_id",
        "triggers": ["message.created"],
        "state": "active",
    }


# ============================================================================
# Mock functions for websocket callback
# ============================================================================


# This function mocks websocket implementation and returns a list of params as a dict
def mock_websocket(
    domain,
    header,
    on_open,
    on_message,
    on_error,
    on_close,
    on_ping,
    on_pong,
    on_cont_message,
    on_data,
):
    return locals()


def on_open():
    print("on_open")


def on_error():
    print("on_error")


def on_close():
    print("on_close")


def on_ping():
    print("on_ping")


def on_pong():
    print("on_pong")


def on_cont_message():
    print("on_cont_message")


def on_data():
    print("on_data")

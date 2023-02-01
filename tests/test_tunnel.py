import json
import sys

if sys.version_info >= (3, 3):
    from unittest.mock import Mock
else:
    from mock import Mock

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
    assert ws["on_message"] is None
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


@pytest.mark.usefixtures("mock_create_webhook")
def test_open_webhook_tunnel(mocker, api_client_with_client_id):
    mock_build = Mock()
    mock_run = Mock()
    mocker.patch("nylas.services.tunnel._build_webhook_tunnel", mock_build)
    mocker.patch("nylas.services.tunnel._run_webhook_tunnel", mock_run)

    tunnel.open_webhook_tunnel(api_client_with_client_id, {"region": Region.IRELAND})

    mock_build_calls = mock_build.call_args_list
    assert len(mock_build_calls) == 1
    assert len(mock_build_calls[0].args) == 2
    assert mock_build_calls[0].args == (
        api_client_with_client_id,
        {"region": Region.IRELAND},
    )

    mock_run_calls = mock_run.call_args_list
    assert len(mock_run_calls) == 1


def test_run_webhook_tunnel():
    mock = Mock()
    tunnel._run_webhook_tunnel(mock)
    mock_method_calls = mock.method_calls
    assert len(mock_method_calls) == 1
    assert mock_method_calls[0][0] == "run_forever"


def test_parse_deltas():
    message = '{"body": "{\\"deltas\\": [{\\"date\\": 1675098465, \\"object\\": \\"message\\", \\"type\\": \\"message.created\\", \\"object_data\\": {\\"namespace_id\\": \\"namespace_123\\", \\"account_id\\": \\"account_123\\", \\"object\\": \\"message\\", \\"attributes\\": {\\"thread_id\\": \\"thread_123\\", \\"received_date\\": 1675098459}, \\"id\\": \\"123\\", \\"metadata\\": null}}]}"}'
    deltas = tunnel._parse_deltas(message)
    assert len(deltas) == 1
    delta = deltas[0]
    assert delta["date"] == 1675098465
    assert delta["object"] == "message"
    assert delta["type"] == Webhook.Trigger.MESSAGE_CREATED
    assert delta["object_data"] is not None


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


def on_message():
    print("on_message")


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

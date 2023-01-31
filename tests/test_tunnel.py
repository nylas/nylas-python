import json

import pytest
from urlobject import URLObject
import services.tunnel
from client.restful_models import Webhook


@pytest.mark.usefixtures("mock_create_webhook")
def test_register_webhook(mocked_responses, api_client_with_client_id):
    services.tunnel._register_webhook(
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

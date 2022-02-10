import json

import pytest
from urlobject import URLObject

from nylas.client.restful_models import Webhook


@pytest.mark.usefixtures("mock_webhooks")
def test_webhooks(mocked_responses, api_client_with_client_id):
    webhook = api_client_with_client_id.webhooks.first()
    request = mocked_responses.calls[0].request
    assert URLObject(request.url).path == "/a/fake-client-id/webhooks"
    assert request.method == "GET"
    assert isinstance(webhook, Webhook)
    assert webhook.id == "webhook-id"
    assert webhook.application_id == "application-id"
    assert webhook.callback_url == "https://your-server.com/webhook"
    assert webhook.state == "active"
    assert webhook.triggers == ["message.created"]
    assert webhook.version == "2.0"


@pytest.mark.usefixtures("mock_webhooks")
def test_single_webhook(mocked_responses, api_client_with_client_id):
    webhook = api_client_with_client_id.webhooks.get("abc123")
    request = mocked_responses.calls[0].request
    assert URLObject(request.url).path == "/a/fake-client-id/webhooks/abc123"
    assert request.method == "GET"
    assert isinstance(webhook, Webhook)
    assert webhook.id == "abc123"


@pytest.mark.usefixtures("mock_webhooks")
def test_update_webhook(mocked_responses, api_client_with_client_id):
    webhook = api_client_with_client_id.webhooks.get("abc123")
    webhook.state = Webhook.State.INACTIVE
    webhook.save()
    assert len(mocked_responses.calls) == 2
    request = mocked_responses.calls[1].request
    assert URLObject(request.url).path == "/a/fake-client-id/webhooks/abc123"
    assert request.method == "PUT"
    assert json.loads(request.body) == {"state": "inactive"}
    assert isinstance(webhook, Webhook)
    assert webhook.id == "abc123"
    assert webhook.state == "inactive"


@pytest.mark.usefixtures("mock_webhooks")
def test_delete_webhook(mocked_responses, api_client_with_client_id):
    api_client_with_client_id.webhooks.delete("abc123")
    request = mocked_responses.calls[0].request
    assert URLObject(request.url).path == "/a/fake-client-id/webhooks/abc123"
    assert request.method == "DELETE"


@pytest.mark.usefixtures("mock_create_webhook")
def test_create_webhook(mocked_responses, api_client_with_client_id):
    webhook = api_client_with_client_id.webhooks.create()
    webhook.callback_url = "https://your-server.com/webhook"
    webhook.triggers = [Webhook.Trigger.MESSAGE_CREATED]
    webhook.state = Webhook.State.ACTIVE
    webhook.application_id = "should-not-send"
    webhook.version = "should-not-send"
    webhook.save()
    request = mocked_responses.calls[0].request
    assert URLObject(request.url).path == "/a/fake-client-id/webhooks"
    assert request.method == "POST"
    assert json.loads(request.body) == {
        "callback_url": "https://your-server.com/webhook",
        "triggers": ["message.created"],
        "state": "active",
    }
    assert isinstance(webhook, Webhook)
    assert webhook.id == "webhook-id"
    assert webhook.application_id == "application-id"
    assert webhook.callback_url == "https://your-server.com/webhook"
    assert webhook.state == "active"
    assert webhook.triggers == ["message.created"]
    assert webhook.version == "1.0"

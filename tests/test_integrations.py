import json

import pytest
from urlobject import URLObject

from nylas.client.integration_models import Integration


@pytest.mark.usefixtures("mock_integrations")
def test_integration(mocked_responses, api_client):
    integration = api_client.integrations.first()
    request = mocked_responses.calls[0].request
    assert URLObject(request.url).path == "/connect/integrations"
    assert request.method == "GET"
    assert isinstance(integration, Integration)
    assert integration.name == "Nylas Playground"
    assert integration.id == "zoom"
    assert integration.provider == "zoom"
    assert integration.settings["client_id"] == "test_client_id"
    assert integration.settings["client_secret"] == "test_client_secret"
    assert integration.redirect_uris[0] == "https://www.nylas.com"
    assert integration.expires_in == 12000


@pytest.mark.usefixtures("mock_integrations")
def test_integration_api_url(mocked_responses, api_client):
    integrations = api_client.integrations
    integrations.first()
    request = mocked_responses.calls[0].request
    assert URLObject(request.url).hostname == "beta.us.nylas.com"
    integrations.app_name = "test_app"
    integrations.first()
    request = mocked_responses.calls[1].request
    assert URLObject(request.url).hostname == "test_app.us.nylas.com"
    integrations.region = Integration.Region.EU
    integrations.first()
    request = mocked_responses.calls[2].request
    assert URLObject(request.url).hostname == "test_app.eu.nylas.com"


@pytest.mark.usefixtures("mock_integrations")
def test_single_integration(mocked_responses, api_client):
    integration = api_client.integrations.get(Integration.Provider.ZOOM)
    request = mocked_responses.calls[0].request
    assert URLObject(request.url).path == "/connect/integrations/zoom"
    assert request.method == "GET"
    assert isinstance(integration, Integration)
    assert integration.id == "zoom"
    assert integration.provider == "zoom"


@pytest.mark.usefixtures("mock_integrations")
def test_update_integration(mocked_responses, api_client):
    integration = api_client.integrations.get(Integration.Provider.ZOOM)
    integration.name = "Updated Integration Name"
    integration.save()
    assert len(mocked_responses.calls) == 2
    request = mocked_responses.calls[1].request
    assert URLObject(request.url).path == "/connect/integrations/zoom"
    assert request.method == "PATCH"
    assert json.loads(request.body) == {
        "name": "Updated Integration Name",
        "settings": {
            "client_id": "test_client_id",
            "client_secret": "test_client_secret",
        },
        "redirect_uris": ["https://www.nylas.com"],
        "expires_in": 12000,
        "scope": [],
    }
    assert isinstance(integration, Integration)
    assert integration.id == "zoom"
    assert integration.provider == "zoom"
    assert integration.name == "Updated Integration Name"


@pytest.mark.usefixtures("mock_integrations")
def test_delete_integration(mocked_responses, api_client):
    api_client.integrations.delete(Integration.Provider.ZOOM)
    request = mocked_responses.calls[0].request
    assert URLObject(request.url).path == "/connect/integrations/zoom"
    assert request.method == "DELETE"


@pytest.mark.usefixtures("mock_integrations")
def test_create_integration(mocked_responses, api_client):
    integration = api_client.integrations.create()
    integration.name = "Nylas Playground"
    integration.provider = Integration.Provider.ZOOM
    integration.settings["client_id"] = "test_client_id"
    integration.settings["client_secret"] = "test_client_secret"
    integration.redirect_uris = ["https://www.nylas.com"]
    integration.expires_in = 12000
    integration.scope = ["test.scope"]
    integration.save()
    request = mocked_responses.calls[0].request
    assert URLObject(request.url).path == "/connect/integrations"
    assert request.method == "POST"
    assert json.loads(request.body) == {
        "name": "Nylas Playground",
        "provider": "zoom",
        "settings": {
            "client_id": "test_client_id",
            "client_secret": "test_client_secret",
        },
        "redirect_uris": ["https://www.nylas.com"],
        "expires_in": 12000,
        "scope": ["test.scope"],
    }
    assert isinstance(integration, Integration)
    assert integration.name == "Nylas Playground"
    assert integration.id == "zoom"
    assert integration.provider == "zoom"
    assert integration.settings["client_id"] == "test_client_id"
    assert integration.settings["client_secret"] == "test_client_secret"
    assert integration.redirect_uris[0] == "https://www.nylas.com"
    assert integration.expires_in == 12000
    assert integration.scope == ["test.scope"]

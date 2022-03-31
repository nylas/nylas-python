import json

import pytest
from urlobject import URLObject

from nylas.client.authentication_models import Authentication, Integration, Grant


@pytest.mark.usefixtures("mock_integrations")
def test_authentication_api_url(mocked_responses, api_client):
    authentication = api_client.authentication
    integrations = authentication.integrations
    integrations.first()
    request = mocked_responses.calls[0].request
    assert URLObject(request.url).hostname == "beta.us.nylas.com"
    authentication.app_name = "test_app"
    integrations.first()
    request = mocked_responses.calls[1].request
    assert URLObject(request.url).hostname == "test_app.us.nylas.com"
    authentication.region = Authentication.Region.EU
    integrations.first()
    request = mocked_responses.calls[2].request
    assert URLObject(request.url).hostname == "test_app.eu.nylas.com"


@pytest.mark.usefixtures("mock_integrations")
def test_integration(mocked_responses, api_client):
    integration = api_client.authentication.integrations.first()
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
def test_single_integration(mocked_responses, api_client):
    integration = api_client.authentication.integrations.get(
        Authentication.Provider.ZOOM
    )
    request = mocked_responses.calls[0].request
    assert URLObject(request.url).path == "/connect/integrations/zoom"
    assert request.method == "GET"
    assert isinstance(integration, Integration)
    assert integration.id == "zoom"
    assert integration.provider == "zoom"


@pytest.mark.usefixtures("mock_integrations")
def test_update_integration(mocked_responses, api_client):
    integration = api_client.authentication.integrations.get(
        Authentication.Provider.ZOOM
    )
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
    api_client.authentication.integrations.delete(Authentication.Provider.ZOOM)
    request = mocked_responses.calls[0].request
    assert URLObject(request.url).path == "/connect/integrations/zoom"
    assert request.method == "DELETE"


@pytest.mark.usefixtures("mock_integrations")
def test_create_integration(mocked_responses, api_client):
    integration = api_client.authentication.integrations.create()
    integration.name = "Nylas Playground"
    integration.provider = Authentication.Provider.ZOOM
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


@pytest.mark.usefixtures("mock_grants")
def test_grant(mocked_responses, api_client):
    grant = api_client.authentication.grants.first()
    request = mocked_responses.calls[0].request
    assert URLObject(request.url).path == "/connect/grants"
    assert request.method == "GET"
    assert isinstance(grant, Grant)
    assert grant.id == "grant-id"
    assert grant.provider == "zoom"
    assert grant.grant_status == "valid"
    assert grant.email == "email@example.com"
    assert grant.metadata == {"isAdmin": True}
    assert grant.scope[0] == "meeting:write"
    assert grant.user_agent == "string"
    assert grant.ip == "string"
    assert grant.created_at == 1617817109
    assert grant.updated_at == 1617817109


@pytest.mark.usefixtures("mock_grants")
def test_single_grant(mocked_responses, api_client):
    grant = api_client.authentication.grants.get("grant-id")
    request = mocked_responses.calls[0].request
    assert URLObject(request.url).path == "/connect/grants/grant-id"
    assert request.method == "GET"
    assert isinstance(grant, Grant)
    assert grant.id == "grant-id"


@pytest.mark.usefixtures("mock_grants")
def test_update_grant(mocked_responses, api_client):
    grant = api_client.authentication.grants.get("grant-id")
    grant.settings = {"refresh_token": "test_token"}
    grant.save()
    assert len(mocked_responses.calls) == 2
    request = mocked_responses.calls[1].request
    assert URLObject(request.url).path == "/connect/grants/grant-id"
    assert request.method == "PATCH"
    assert json.loads(request.body) == {
        "settings": {"refresh_token": "test_token"},
        "metadata": {"isAdmin": True},
        "scope": ["meeting:write"],
    }
    assert isinstance(grant, Grant)
    assert grant.id == "grant-id"
    assert grant.settings == {"refresh_token": "test_token"}


@pytest.mark.usefixtures("mock_grants")
def test_delete_grant(mocked_responses, api_client):
    api_client.authentication.grants.delete("grant-id")
    request = mocked_responses.calls[0].request
    assert URLObject(request.url).path == "/connect/grants/grant-id"
    assert request.method == "DELETE"


@pytest.mark.usefixtures("mock_grants")
def test_create_grant(mocked_responses, api_client):
    grant = api_client.authentication.grants.create()
    grant.provider = Authentication.Provider.ZOOM
    grant.settings = {"refresh_token": "test-refresh-token"}
    grant.metadata = {"isAdmin": True}
    grant.scope = ["meeting:write"]
    grant.save()
    request = mocked_responses.calls[0].request
    assert URLObject(request.url).path == "/connect/grants"
    assert request.method == "POST"
    assert json.loads(request.body) == {
        "provider": "zoom",
        "settings": {"refresh_token": "test-refresh-token"},
        "scope": ["meeting:write"],
        "metadata": {"isAdmin": True},
    }
    assert isinstance(grant, Grant)


@pytest.mark.usefixtures("mock_grants")
def test_grant_on_demand_sync(mocked_responses, api_client):
    grant = api_client.authentication.grants.on_demand_sync("grant-id", sync_from=12000)
    request = mocked_responses.calls[0].request
    assert request.path_url == "/connect/grants/grant-id/sync?sync_from=12000"
    assert request.method == "POST"
    assert request.body is None
    assert isinstance(grant, Grant)


@pytest.mark.usefixtures("mock_authentication_hosted_auth")
def test_grant_authentication_hosted_auth(mocked_responses, api_client):
    api_client.authentication.hosted_authentication(
        provider=Authentication.Provider.ZOOM,
        redirect_uri="https://myapp.com/callback-handler",
        grant_id="test-grant-id",
        login_hint="example@email.com",
        state="test-state",
        expires_in=60,
        settings={"refresh_token": "test-refresh-token"},
        metadata={"isAdmin": True},
        scope=["meeting:write"],
    )
    request = mocked_responses.calls[0].request
    assert URLObject(request.url).path == "/connect/auth"
    assert request.method == "POST"
    assert json.loads(request.body) == {
        "provider": "zoom",
        "redirect_uri": "https://myapp.com/callback-handler",
        "grant_id": "test-grant-id",
        "login_hint": "example@email.com",
        "state": "test-state",
        "expires_in": 60,
        "settings": {"refresh_token": "test-refresh-token"},
        "scope": ["meeting:write"],
        "metadata": {"isAdmin": True},
    }

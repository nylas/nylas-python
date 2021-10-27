from datetime import datetime

import pytest

from nylas.client.restful_models import Component


def blank_component(api_client):
    component = api_client.components.create()
    component.name = "Python Component Test"
    component.type = "agenda"
    component.public_account_id = "test-account-id"
    component.access_token = "test-access-token"
    return component


@pytest.mark.usefixtures("mock_components")
def test_components(api_client):
    component = api_client.components.first()
    assert isinstance(component, Component)
    assert component.id == "component-id"
    assert component.active is True
    assert component.name == "PyTest Component"
    assert component.public_account_id == "account-id"
    assert component.public_application_id == "application-id"
    assert component.type == "agenda"
    assert component.created_at == datetime.strptime(
        "2021-10-22T18:02:10.000Z", "%Y-%m-%dT%H:%M:%S.%fZ"
    )
    assert component.updated_at == datetime.strptime(
        "2021-10-22T18:02:10.000Z", "%Y-%m-%dT%H:%M:%S.%fZ"
    )
    assert component.public_token_id == "token-id"


@pytest.mark.usefixtures("mock_components")
def test_components(api_client):
    component = api_client.components.first()
    assert isinstance(component, Component)
    assert component.id == "component-id"
    assert component.active is True
    assert component.name == "PyTest Component"
    assert component.public_account_id == "account-id"
    assert component.public_application_id == "application-id"
    assert component.type == "agenda"
    assert component.created_at == datetime.strptime(
        "2021-10-22T18:02:10.000Z", "%Y-%m-%dT%H:%M:%S.%fZ"
    )
    assert component.updated_at == datetime.strptime(
        "2021-10-22T18:02:10.000Z", "%Y-%m-%dT%H:%M:%S.%fZ"
    )
    assert component.public_token_id == "token-id"


@pytest.mark.usefixtures("mock_components_create_response")
def test_create_components(api_client):
    component = blank_component(api_client)
    component.save()
    assert component.id == "cv4ei7syx10uvsxbs21ccsezf"


@pytest.mark.usefixtures("mock_components_create_response")
def test_modify_components(api_client):
    component = blank_component(api_client)
    component.id = "cv4ei7syx10uvsxbs21ccsezf"
    component.name = "Updated Name"
    component.save()
    assert component.name == "Updated Name"


@pytest.mark.usefixtures("mock_components_create_response")
def test_components_as_json_read_only(api_client):
    component = blank_component(api_client)
    component.id = "test-id"
    json = component.as_json()
    assert "id" not in json
    assert "public_application_id" not in json
    assert "created_at" not in json
    assert "updated_at" not in json

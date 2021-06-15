import pytest
from nylas.client.restful_models import RoomResource


@pytest.mark.usefixtures("mock_resources")
def test_first_resource(api_client):
    resource = api_client.room_resources.first()
    assert isinstance(resource, RoomResource)


@pytest.mark.usefixtures("mock_resources")
def test_all_resources(api_client):
    resources = api_client.room_resources.all()
    assert len(resources) == 2
    for resource in resources:
        assert isinstance(resource, RoomResource)


@pytest.mark.usefixtures("mock_resources")
def test_resource(api_client):
    resource = api_client.room_resources.first()
    assert resource["object"] == "room_resource"
    assert resource["email"] == "training-room-1A@google.com"
    assert resource["name"] == "Google Training Room"
    assert resource["building"] == "San Francisco"
    assert resource["capacity"] == "10"
    assert resource["floor_name"] == "7"
    assert resource["floor_number"] is None

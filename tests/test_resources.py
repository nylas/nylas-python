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

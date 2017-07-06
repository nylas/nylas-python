import pytest
import responses
from nylas.client.restful_models import Folder


@responses.activate
@pytest.mark.usefixtures("mock_folder")
def test_get_change_folder(api_client):
    folder = api_client.folders.find('anuep8pe5ug3xrupchwzba2o8')
    assert folder is not None
    assert isinstance(folder, Folder)
    assert folder.display_name == 'My Folder'
    folder.display_name = 'My New Folder'
    folder.save()
    assert folder.display_name == 'My New Folder'

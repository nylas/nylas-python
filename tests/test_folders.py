import pytest
from nylas.client.restful_models import Folder, Thread, Message


@pytest.mark.usefixtures("mock_folder")
def test_get_change_folder(api_client):
    folder = api_client.folders.get("anuep8pe5ug3xrupchwzba2o8")
    assert folder is not None
    assert isinstance(folder, Folder)
    assert folder.display_name == "My Folder"
    folder.display_name = "My New Folder"
    folder.save()
    assert folder.display_name == "My New Folder"


@pytest.mark.usefixtures("mock_folder", "mock_threads")
def test_folder_threads(api_client):
    folder = api_client.folders.get("anuep8pe5ug3xrupchwzba2o8")
    assert folder.threads
    assert all(isinstance(thread, Thread) for thread in folder.threads)


@pytest.mark.usefixtures("mock_folder", "mock_messages")
def test_folder_messages(api_client):
    folder = api_client.folders.get("anuep8pe5ug3xrupchwzba2o8")
    assert folder.messages
    assert all(isinstance(message, Message) for message in folder.messages)

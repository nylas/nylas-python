import json
import re
import pytest
import responses
from nylas.client.restful_models import Label, Folder


@responses.activate
@pytest.mark.usefixtures("mock_labels")
def test_list_labels(api_client):
    labels = api_client.labels
    labels = [l for l in labels]
    assert len(labels) == 5
    assert all(isinstance(x, Label) for x in labels)


@responses.activate
@pytest.mark.usefixtures("mock_label")
def test_get_label(api_client):
    label = api_client.labels.find('anuep8pe5ugmxrucchrzba2o8')
    assert label is not None
    assert isinstance(label, Label)
    assert label.display_name == 'Important'


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


@responses.activate
@pytest.mark.usefixtures("mock_messages")
def test_messages(api_client):
    message = api_client.messages.first()
    assert len(message.labels) == 1
    assert message.labels[0].display_name == 'Inbox'
    assert message.folder is None
    assert message.unread
    assert not message.starred


@responses.activate
@pytest.mark.usefixtures("mock_account", "mock_messages", "mock_message")
def test_message_change(api_client):
    message = api_client.messages.first()
    message.star()
    assert message.starred is True
    message.unstar()
    assert message.starred is False
    message.mark_as_read()
    assert message

    message.add_label('fghj')
    msg_labels = [l.id for l in message.labels]
    assert 'abcd' in msg_labels
    assert 'fghj' in msg_labels
    message.remove_label('fghj')
    msg_labels = [l.id for l in message.labels]
    assert 'abcd' in msg_labels
    assert 'fghj' not in msg_labels

    # Test that folders don't do anything when labels are in effect
    message.update_folder('zxcv')
    assert message.folder is None


@responses.activate
@pytest.mark.usefixtures("mock_threads")
def test_thread_folder(api_client):
    thread = api_client.threads.first()
    assert len(thread.labels) == 0  # pylint: disable=len-as-condition
    assert len(thread.folders) == 1
    assert thread.folders[0].display_name == 'Inbox'
    assert not thread.unread
    assert thread.starred


@responses.activate
@pytest.mark.usefixtures("mock_folder_account", "mock_threads", "mock_thread")
def test_thread_change(api_client):
    thread = api_client.threads.first()

    assert thread.starred
    thread.unstar()
    assert not thread.starred

    thread.update_folder('qwer')
    assert len(thread.folders) == 1
    assert thread.folders[0].id == 'qwer'

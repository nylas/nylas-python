import pytest
import responses
from nylas.client.restful_models import Message, Draft


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


@responses.activate
@pytest.mark.usefixtures("mock_threads", "mock_messages")
def test_thread_messages(api_client):
    thread = api_client.threads.first()
    assert thread.messages
    assert all(isinstance(message, Message)
               for message in thread.messages)


@responses.activate
@pytest.mark.usefixtures("mock_threads", "mock_drafts")
def test_thread_drafts(api_client):
    thread = api_client.threads.first()
    assert thread.drafts
    assert all(isinstance(draft, Draft)
               for draft in thread.drafts)

import pytest
import responses
from nylas.client.restful_models import Message, Draft, Label


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


@responses.activate
@pytest.mark.usefixtures("mock_labelled_thread", "mock_labels")
def test_thread_labels(api_client):
    thread = api_client.threads.find(111)
    assert len(thread.labels) == 2
    assert all(isinstance(label, Label)
               for label in thread.labels)

    returned = thread.add_labels(["fake1", "fake2"])
    assert len(thread.labels) == 4
    assert thread.labels == returned

    label_ids = [l.id for l in thread.labels]
    returned = thread.remove_labels(label_ids)
    assert len(thread.labels) == 0  # pylint: disable=len-as-condition
    assert thread.labels == returned

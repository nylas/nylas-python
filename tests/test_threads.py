import pytest
from nylas.client.restful_models import Message, Draft, Label


@pytest.mark.usefixtures("mock_threads")
def test_thread_folder(api_client):
    thread = api_client.threads.first()
    assert len(thread.labels) == 0  # pylint: disable=len-as-condition
    assert len(thread.folders) == 1
    assert thread.folders[0].display_name == 'Inbox'
    assert not thread.unread
    assert thread.starred


@pytest.mark.usefixtures("mock_folder_account", "mock_threads", "mock_thread")
def test_thread_change(api_client):
    thread = api_client.threads.first()

    assert thread.starred
    thread.unstar()
    assert not thread.starred
    thread.star()
    assert thread.starred

    thread.update_folder('qwer')
    assert len(thread.folders) == 1
    assert thread.folders[0].id == 'qwer'


@pytest.mark.usefixtures("mock_threads", "mock_messages")
def test_thread_messages(api_client):
    thread = api_client.threads.first()
    assert thread.messages
    assert all(isinstance(message, Message)
               for message in thread.messages)


@pytest.mark.usefixtures("mock_threads", "mock_drafts")
def test_thread_drafts(api_client):
    thread = api_client.threads.first()
    assert thread.drafts
    assert all(isinstance(draft, Draft)
               for draft in thread.drafts)


@pytest.mark.usefixtures("mock_labelled_thread", "mock_labels")
def test_thread_label(api_client):
    thread = api_client.threads.find(111)
    assert len(thread.labels) == 2
    assert all(isinstance(label, Label)
               for label in thread.labels)

    returned = thread.add_label("fake1")
    assert len(thread.labels) == 3
    assert thread.labels == returned

    returned = thread.remove_label("fake1")
    assert len(thread.labels) == 2  # pylint: disable=len-as-condition
    assert thread.labels == returned


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


@pytest.mark.usefixtures("mock_threads", "mock_thread")
def test_thread_read(api_client):
    thread = api_client.threads.first()
    assert thread.unread is False
    thread.mark_as_unread()
    assert thread.unread is True
    thread.mark_as_read()
    assert thread.unread is False
    # mark_as_seen() is a synonym for mark_as_read()
    thread.mark_as_unread()
    assert thread.unread is True
    thread.mark_as_seen()
    assert thread.unread is False


@pytest.mark.usefixtures("mock_threads")
def test_thread_reply(api_client):
    thread = api_client.threads.first()
    draft = thread.create_reply()
    assert isinstance(draft, Draft)
    assert draft.thread_id == thread.id
    assert draft.subject == thread.subject

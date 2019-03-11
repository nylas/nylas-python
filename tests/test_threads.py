from datetime import datetime

import pytest
from urlobject import URLObject
from nylas.client.restful_models import Message, Draft, Label
from nylas.utils import timestamp_from_dt


@pytest.mark.usefixtures("mock_threads")
def test_thread_attrs(api_client):
    thread = api_client.threads.first()
    expected_first = datetime(2016, 1, 2, 3, 4, 5)
    expected_last = datetime(2017, 1, 2, 3, 4, 5)
    expected_last_received = datetime(2017, 1, 2, 3, 4, 5)
    expected_last_sent = datetime(2017, 1, 1, 1, 1, 1)

    assert thread.first_message_timestamp == timestamp_from_dt(expected_first)
    assert thread.first_message_at == expected_first
    assert thread.last_message_timestamp == timestamp_from_dt(expected_last)
    assert thread.last_message_at == expected_last
    assert thread.last_message_received_timestamp == timestamp_from_dt(
        expected_last_received
    )
    assert thread.last_message_received_at == expected_last_received
    assert thread.last_message_sent_timestamp == timestamp_from_dt(expected_last_sent)
    assert thread.last_message_sent_at == expected_last_sent


def test_update_thread_attrs(api_client):
    thread = api_client.threads.create()
    first = datetime(2017, 2, 3, 10, 0, 0)
    second = datetime(2016, 10, 5, 14, 30, 0)
    # timestamps and datetimes are handled totally separately
    thread.last_message_at = first
    thread.last_message_timestamp = timestamp_from_dt(second)
    assert thread.last_message_at == first
    assert thread.last_message_timestamp == timestamp_from_dt(second)
    # but datetimes overwrite timestamps when serializing to JSON
    assert thread.as_json()["last_message_timestamp"] == timestamp_from_dt(first)


@pytest.mark.usefixtures("mock_threads")
def test_thread_folder(api_client):
    thread = api_client.threads.first()
    assert len(thread.labels) == 0  # pylint: disable=len-as-condition
    assert len(thread.folders) == 1
    assert thread.folders[0].display_name == "Inbox"
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

    thread.update_folder("qwer")
    assert len(thread.folders) == 1
    assert thread.folders[0].id == "qwer"


@pytest.mark.usefixtures("mock_threads", "mock_messages")
def test_thread_messages(api_client):
    thread = api_client.threads.first()
    assert thread.messages
    assert all(isinstance(message, Message) for message in thread.messages)


@pytest.mark.usefixtures("mock_threads", "mock_drafts")
def test_thread_drafts(api_client):
    thread = api_client.threads.first()
    assert thread.drafts
    assert all(isinstance(draft, Draft) for draft in thread.drafts)


@pytest.mark.usefixtures("mock_labelled_thread", "mock_labels")
def test_thread_label(api_client):
    thread = api_client.threads.get(111)
    assert len(thread.labels) == 2
    assert all(isinstance(label, Label) for label in thread.labels)

    returned = thread.add_label("fake1")
    assert len(thread.labels) == 3
    assert thread.labels == returned

    returned = thread.remove_label("fake1")
    assert len(thread.labels) == 2  # pylint: disable=len-as-condition
    assert thread.labels == returned


@pytest.mark.usefixtures("mock_labelled_thread", "mock_labels")
def test_thread_labels(api_client):
    thread = api_client.threads.get(111)
    assert len(thread.labels) == 2
    assert all(isinstance(label, Label) for label in thread.labels)

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


@pytest.mark.usefixtures("mock_threads")
def test_filter_threads_dt(mocked_responses, api_client):
    api_client.threads.where(started_before=datetime(2010, 6, 1)).all()
    assert len(mocked_responses.calls) == 1
    request = mocked_responses.calls[0].request
    url = URLObject(request.url)
    assert url.query_dict["started_before"] == "1275350400"


@pytest.mark.usefixtures("mock_threads")
def test_filter_threads_ts(mocked_responses, api_client):
    api_client.threads.where(started_before=1275350400).all()
    assert len(mocked_responses.calls) == 1
    request = mocked_responses.calls[0].request
    url = URLObject(request.url)
    assert url.query_dict["started_before"] == "1275350400"

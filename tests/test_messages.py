from datetime import datetime
import json

import six
import pytest
from urlobject import URLObject
from nylas.client.restful_models import Message
from nylas.utils import timestamp_from_dt
import pytz


@pytest.mark.usefixtures("mock_messages")
def test_messages(api_client):
    message = api_client.messages.first()
    assert len(message.labels) == 1
    assert message.labels[0].display_name == "Inbox"
    assert message.folder is None
    assert message.unread
    assert not message.starred


@pytest.mark.usefixtures("mock_messages")
def test_message_attrs(api_client):
    message = api_client.messages.first()
    expected_received = datetime(2010, 2, 2, 2, 22, 22)
    assert message.received_at == expected_received
    assert message.date == timestamp_from_dt(expected_received)


@pytest.mark.usefixtures("mock_account", "mock_messages", "mock_message")
def test_message_stars(api_client):
    message = api_client.messages.first()
    assert message.starred is False
    message.star()
    assert message.starred is True
    message.unstar()
    assert message.starred is False


@pytest.mark.usefixtures("mock_account", "mock_messages", "mock_message")
def test_message_read(api_client):
    message = api_client.messages.first()
    assert message.unread is True
    message.mark_as_read()
    assert message.unread is False
    message.mark_as_unread()
    assert message.unread is True
    # mark_as_seen() is a synonym for mark_as_read()
    message.mark_as_seen()
    assert message.unread is False


@pytest.mark.usefixtures("mock_account", "mock_messages", "mock_message")
def test_message_labels(api_client):
    message = api_client.messages.first()
    message.add_label("fghj")
    msg_labels = [l.id for l in message.labels]
    assert "abcd" in msg_labels
    assert "fghj" in msg_labels
    message.remove_label("fghj")
    msg_labels = [l.id for l in message.labels]
    assert "abcd" in msg_labels
    assert "fghj" not in msg_labels

    # Test that folders don't do anything when labels are in effect
    message.update_folder("zxcv")
    assert message.folder is None


@pytest.mark.usefixtures("mock_account", "mock_message", "mock_messages")
def test_message_raw(api_client, account_id):
    message = api_client.messages.first()
    raw = message.raw
    assert isinstance(raw, six.binary_type)
    parsed = json.loads(raw)
    assert parsed == {
        "object": "message",
        "to": [{"email": "foo@yahoo.com", "name": "Foo"}],
        "from": [{"email": "bar@gmail.com", "name": "Bar"}],
        "account_id": account_id,
        "labels": [{"display_name": "Inbox", "name": "inbox", "id": "abcd"}],
        "starred": False,
        "unread": True,
        "id": "1234",
        "subject": "Test Message",
    }


@pytest.mark.usefixtures("mock_message")
def test_message_delete_by_id(mocked_responses, api_client):
    api_client.messages.delete(1234, forceful=True)
    assert len(mocked_responses.calls) == 1
    request = mocked_responses.calls[0].request
    url = URLObject(request.url)
    assert url.query_dict["forceful"] == "True"


@pytest.mark.usefixtures("mock_message")
def test_message_resolution(mocked_responses, api_client, account_id):
    message = api_client.messages.get(1234)
    assert message.object == "message"
    assert message.to == [{"email": "foo@yahoo.com", "name": "Foo"}]
    assert message.from_ == [{"email": "bar@gmail.com", "name": "Bar"}]
    assert message["from"] == [{"email": "bar@gmail.com", "name": "Bar"}]
    assert message.account_id == account_id
    assert message._labels == [{"display_name": "Inbox", "name": "inbox", "id": "abcd"}]
    assert message.id == "1234"
    assert message.subject == "Test Message"
    assert message.starred is False
    assert message.unread is True


@pytest.mark.usefixtures("mock_messages")
def test_slice_messages(api_client):
    messages = api_client.messages[0:2]
    assert len(messages) == 3
    assert all(isinstance(message, Message) for message in messages)


@pytest.mark.usefixtures("mock_messages")
def test_filter_messages_dt(mocked_responses, api_client):
    api_client.messages.where(received_before=datetime(2010, 6, 1)).all()
    assert len(mocked_responses.calls) == 1
    request = mocked_responses.calls[0].request
    url = URLObject(request.url)
    assert url.query_dict["received_before"] == "1275350400"


@pytest.mark.usefixtures("mock_messages")
def test_filter_messages_dt_with_timezone(mocked_responses, api_client):
    api_client.messages.where(
        received_before=datetime(2010, 6, 1, tzinfo=pytz.utc)
    ).all()
    assert len(mocked_responses.calls) == 1
    request = mocked_responses.calls[0].request
    url = URLObject(request.url)
    assert url.query_dict["received_before"] == "1275350400"


@pytest.mark.usefixtures("mock_messages")
def test_filter_messages_ts(mocked_responses, api_client):
    api_client.messages.where(received_before=1275350400).all()
    assert len(mocked_responses.calls) == 1
    request = mocked_responses.calls[0].request
    url = URLObject(request.url)
    assert url.query_dict["received_before"] == "1275350400"


@pytest.mark.usefixtures("mock_message", "mock_messages")
def test_message_metadata(mocked_responses, api_client):
    message = api_client.messages.first()
    message["metadata"] = {"test": "value"}
    message.save()
    assert message.metadata == {"test": "value"}

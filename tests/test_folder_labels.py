import json
import re
import pytest
import responses
import httpretty
from nylas import APIClient
from nylas.client.restful_models import Label, Folder
from nylas.client.errors import *

API_URL = 'http://localhost:2222'

MOCK_ACCOUNT_ID = '4ennivvrcgsqytgybfk912dto'


@pytest.fixture
def api_client():
    return APIClient(None, None, None, API_URL)


@pytest.fixture
def mock_account():
    response_body = json.dumps(
        {
            "account_id": MOCK_ACCOUNT_ID,
            "email_address": "ben.bitdiddle1861@gmail.com",
            "id": MOCK_ACCOUNT_ID,
            "name": "Ben Bitdiddle",
            "object": "account",
            "provider": "gmail",
            "organization_unit": "label"
        }
    )
    responses.add(responses.GET, API_URL + '/account',
                  content_type='application/json', status=200,
                  body=response_body, match_querystring=True)


@pytest.fixture
def mock_folder_account():
    response_body = json.dumps(
        {
            "email_address": "ben.bitdiddle1861@office365.com",
            "id": MOCK_ACCOUNT_ID,
            "name": "Ben Bitdiddle",
            "account_id": MOCK_ACCOUNT_ID,
            "object": "account",
            "provider": "eas",
            "organization_unit": "folder"
        }
    )
    responses.add(responses.GET, API_URL + '/account',
                  content_type='application/json', status=200,
                  body=response_body, match_querystring=True)


@pytest.fixture
def mock_labels():
    response_body = json.dumps([
        {
            "display_name": "Important",
            "id": "anuep8pe5ugmxrucchrzba2o8",
            "name": "important",
            "account_id": MOCK_ACCOUNT_ID,
            "object": "label"
        },
        {
            "display_name": "Trash",
            "id": "f1xgowbgcehk235xiy3c3ek42",
            "name": "trash",
            "account_id": MOCK_ACCOUNT_ID,
            "object": "label"
        },
        {
            "display_name": "Sent Mail",
            "id": "ah14wp5fvypvjjnplh7nxgb4h",
            "name": "sent",
            "account_id": MOCK_ACCOUNT_ID,
            "object": "label"
        },
        {
            "display_name": "All Mail",
            "id": "ah14wp5fvypvjjnplh7nxgb4h",
            "name": "all",
            "account_id": MOCK_ACCOUNT_ID,
            "object": "label"
        },
        {
            "display_name": "Inbox",
            "id": "dc11kl3s9lj4760g6zb36spms",
            "name": "inbox",
            "account_id": MOCK_ACCOUNT_ID,
            "object": "label"
        }
    ])
    endpoint = re.compile(API_URL + '/labels.*')
    responses.add(responses.GET, endpoint,
                  content_type='application/json', status=200,
                  body=response_body)


@pytest.fixture
def mock_label():
    response_body = json.dumps(
        {
            "display_name": "Important",
            "id": "anuep8pe5ugmxrucchrzba2o8",
            "name": "important",
            "account_id": MOCK_ACCOUNT_ID,
            "object": "label"
        }
    )
    endpoint = re.compile(API_URL + '/labels/anuep8pe5ugmxrucchrzba2o8')
    responses.add(responses.GET, endpoint,
                  content_type='application/json', status=200,
                  body=response_body)


@pytest.fixture
def mock_folder():
    folder = {
        "display_name": "My Folder",
        "id": "anuep8pe5ug3xrupchwzba2o8",
        "name": None,
        "account_id": MOCK_ACCOUNT_ID,
        "object": "folder"
        }
    response_body = json.dumps(folder)
    endpoint = re.compile(API_URL + '/folders/anuep8pe5ug3xrupchwzba2o8')
    responses.add(responses.GET, endpoint,
                  content_type='application/json', status=200,
                  body=response_body)

    def request_callback(request):
        payload = json.loads(request.body)
        if 'display_name' in payload:
            folder.update(payload)
        return (200, {}, json.dumps(folder))
    responses.add_callback(responses.PUT, endpoint,
                           content_type='application/json',
                           callback=request_callback)



@pytest.fixture
def mock_messages():
    response_body = json.dumps([
        {
            "id": "1234",
            "subject": "Test Message",
            "account_id": MOCK_ACCOUNT_ID,
            "object": "message",
            "labels": [
                {
                    "name": "inbox",
                    "display_name": "Inbox",
                    "id": "abcd"
                }
            ],
            "starred": False,
            "unread": True
        }
    ])
    endpoint = re.compile(API_URL + '/messages')
    responses.add(responses.GET, endpoint,
                  content_type='application/json', status=200,
                  body=response_body)


@pytest.fixture
def mock_message():
    base_msg = {
        "id": "1234",
        "subject": "Test Message",
        "account_id": MOCK_ACCOUNT_ID,
        "object": "message",
        "labels": [
            {
                "name": "inbox",
                "display_name": "Inbox",
                "id": "abcd"
            }
        ],
        "starred": False,
        "unread": True
    }
    response_body = json.dumps(base_msg)

    def request_callback(request):
        payload = json.loads(request.body)
        if 'labels' in payload:
            labels = [{'name': 'test', 'display_name': 'test', 'id': l}
                      for l in payload['labels']]
            base_msg['labels'] = labels
        return (200, {}, json.dumps(base_msg))

    endpoint = re.compile(API_URL + '/messages/1234')
    responses.add(responses.GET, endpoint,
                  content_type='application/json', status=200,
                  body=response_body)
    responses.add_callback(responses.PUT, endpoint,
                           content_type='application/json',
                           callback=request_callback)


@pytest.fixture
def mock_threads():
    response_body = json.dumps([
        {
            "id": "5678",
            "subject": "Test Thread",
            "account_id": MOCK_ACCOUNT_ID,
            "object": "thread",
            "folders": [{
                "name": "inbox",
                "display_name": "Inbox",
                "id": "abcd"
            }],
            "starred": True,
            "unread": False
        }
    ])
    endpoint = re.compile(API_URL + '/threads')
    responses.add(responses.GET, endpoint,
                  content_type='application/json', status=200,
                  body=response_body)


@pytest.fixture
def mock_thread():
    base_thrd = {
        "id": "5678",
        "subject": "Test Thread",
        "account_id": MOCK_ACCOUNT_ID,
        "object": "thread",
        "folders": [{
            "name": "inbox",
            "display_name": "Inbox",
            "id": "abcd"
        }],
        "starred": True,
        "unread": False
    }
    response_body = json.dumps(base_thrd)

    def request_callback(request):
        payload = json.loads(request.body)
        if 'folder' in payload:
            folder = {'name': 'test', 'display_name': 'test',
                      'id': payload['folder']}
            base_thrd['folders'] = [folder]
        return (200, {}, json.dumps(base_thrd))

    endpoint = re.compile(API_URL + '/threads/5678')
    responses.add(responses.GET, endpoint,
                  content_type='application/json', status=200,
                  body=response_body)
    responses.add_callback(responses.PUT, endpoint,
                           content_type='application/json',
                           callback=request_callback)


@responses.activate
def test_list_labels(api_client, mock_labels):
    labels = api_client.labels
    labels = [l for l in labels]
    assert len(labels) == 5
    assert all(isinstance(x, Label) for x in labels)


@responses.activate
def test_get_label(api_client, mock_label):
    label = api_client.labels.find('anuep8pe5ugmxrucchrzba2o8')
    assert label is not None
    assert isinstance(label, Label)
    assert label.display_name == 'Important'


@responses.activate
def test_get_change_folder(api_client, mock_folder):
    folder = api_client.folders.find('anuep8pe5ug3xrupchwzba2o8')
    assert folder is not None
    assert isinstance(folder, Folder)
    assert folder.display_name == 'My Folder'
    folder.display_name = 'My New Folder'
    folder.save()
    assert folder.display_name == 'My New Folder'


@responses.activate
def test_messages(api_client, mock_messages):
    message = api_client.messages.first()
    assert len(message.labels) == 1
    assert message.labels[0].display_name == 'Inbox'
    assert message.folder is None
    assert message.unread
    assert not message.starred


@responses.activate
def test_message_change(api_client, mock_account, mock_messages,
                        mock_message):
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
def test_thread_folder(api_client, mock_threads):
    thread = api_client.threads.first()
    assert len(thread.labels) == 0
    assert len(thread.folders) == 1
    assert thread.folders[0].display_name == 'Inbox'
    assert not thread.unread
    assert thread.starred


@responses.activate
def test_thread_change(api_client, mock_folder_account,
                       mock_threads, mock_thread):
    thread = api_client.threads.first()

    assert thread.starred
    thread.unstar()
    assert not thread.starred

    thread.update_folder('qwer')
    assert len(thread.folders) == 1
    assert thread.folders[0].id == 'qwer'

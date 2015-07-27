import json
import re
import pytest
import responses
from nylas import APIClient
from nylas.client.restful_models import Label, Folder
from nylas.client.errors import *

API_URL = 'http://localhost:2222'

MOCK_NS_ID = 'asdf'


@pytest.fixture
def api_client():
    return APIClient(None, None, None, API_URL)


@pytest.fixture
def mock_namespace():
    response_body = json.dumps([
        {
            "account_id": "4ennivvrcgsqytgybfk912dto",
            "email_address": "ben.bitdiddle1861@gmail.com",
            "id": MOCK_NS_ID,
            "name": "Ben Bitdiddle",
            "namespace_id": MOCK_NS_ID,
            "object": "namespace",
            "provider": "gmail",
            "organization_unit": "label"
        }
    ])
    responses.add(responses.GET, API_URL + '/n?limit=1&offset=0',
                  content_type='application/json', status=200,
                  body=response_body, match_querystring=True)


@pytest.fixture
def mock_folder_namespace():
    response_body = json.dumps([
        {
            "account_id": "1e3niqvrcgsqytgybfk912dto",
            "email_address": "ben.bitdiddle1861@office365.com",
            "id": 'asdg',
            "name": "Ben Bitdiddle",
            "namespace_id": 'asdg',
            "object": "namespace",
            "provider": "eas",
            "organization_unit": "folder"
        }
    ])
    responses.add(responses.GET, API_URL + '/n?limit=1&offset=0',
                  content_type='application/json', status=200,
                  body=response_body, match_querystring=True)


@pytest.fixture
def mock_labels():
    response_body = json.dumps([
        {
            "display_name": "Important",
            "id": "anuep8pe5ugmxrucchrzba2o8",
            "name": "important",
            "namespace_id": "asdf",
            "object": "label"
        },
        {
            "display_name": "Trash",
            "id": "f1xgowbgcehk235xiy3c3ek42",
            "name": "trash",
            "namespace_id": "asdf",
            "object": "label"
        },
        {
            "display_name": "Sent Mail",
            "id": "ah14wp5fvypvjjnplh7nxgb4h",
            "name": "sent",
            "namespace_id": "asdf",
            "object": "label"
        },
        {
            "display_name": "All Mail",
            "id": "ah14wp5fvypvjjnplh7nxgb4h",
            "name": "all",
            "namespace_id": "asdf",
            "object": "label"
        },
        {
            "display_name": "Inbox",
            "id": "dc11kl3s9lj4760g6zb36spms",
            "name": "inbox",
            "namespace_id": "asdf",
            "object": "label"
        }
    ])
    endpoint = re.compile(API_URL + '/n/asdf/labels.*')
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
            "namespace_id": "asdf",
            "object": "label"
        }
    )
    endpoint = re.compile(API_URL + '/n/asdf/labels/anuep8pe5ugmxrucchrzba2o8')
    responses.add(responses.GET, endpoint,
                  content_type='application/json', status=200,
                  body=response_body)


@pytest.fixture
def mock_folder():
    folder = {
        "display_name": "My Folder",
        "id": "anuep8pe5ug3xrupchwzba2o8",
        "name": None,
        "namespace_id": "asdg",
        "object": "folder"
        }
    response_body = json.dumps(folder)
    endpoint = re.compile(API_URL + '/n/asdg/folders/anuep8pe5ug3xrupchwzba2o8')
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
            "namespace_id": "asdf",
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
    endpoint = re.compile(API_URL + '/n/asdf/messages')
    responses.add(responses.GET, endpoint,
                  content_type='application/json', status=200,
                  body=response_body)


@pytest.fixture
def mock_message():
    base_msg = {
        "id": "1234",
        "subject": "Test Message",
        "namespace_id": "asdf",
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

    endpoint = re.compile(API_URL + '/n/asdf/messages/1234')
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
            "namespace_id": "asdg",
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
    endpoint = re.compile(API_URL + '/n/asdg/threads')
    responses.add(responses.GET, endpoint,
                  content_type='application/json', status=200,
                  body=response_body)


@pytest.fixture
def mock_thread():
    base_thrd = {
        "id": "5678",
        "subject": "Test Thread",
        "namespace_id": "asdg",
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

    endpoint = re.compile(API_URL + '/n/asdg/threads/5678')
    responses.add(responses.GET, endpoint,
                  content_type='application/json', status=200,
                  body=response_body)
    responses.add_callback(responses.PUT, endpoint,
                           content_type='application/json',
                           callback=request_callback)


@responses.activate
def test_list_labels(api_client, mock_namespace, mock_labels):
    namespace = api_client.namespaces.first()
    labels = namespace.labels
    labels = [l for l in labels]
    assert len(labels) == 5
    assert all(isinstance(x, Label) for x in labels)


@responses.activate
def test_get_label(api_client, mock_namespace, mock_label):
    namespace = api_client.namespaces.first()
    label = namespace.labels.find('anuep8pe5ugmxrucchrzba2o8')
    assert label is not None
    assert isinstance(label, Label)
    assert label.display_name == 'Important'


@responses.activate
def test_get_change_folder(api_client, mock_folder_namespace, mock_folder):
    namespace = api_client.namespaces.first()
    folder = namespace.folders.find('anuep8pe5ug3xrupchwzba2o8')
    assert folder is not None
    assert isinstance(folder, Folder)
    assert folder.display_name == 'My Folder'
    folder.display_name = 'My New Folder'
    folder.save()
    assert folder.display_name == 'My New Folder'


@responses.activate
def test_messages(api_client, mock_namespace, mock_messages):
    namespace = api_client.namespaces.first()
    message = namespace.messages.first()
    assert len(message.labels) == 1
    assert message.labels[0].display_name == 'Inbox'
    assert message.folder is None
    assert message.unread
    assert not message.starred


@responses.activate
def test_message_change(api_client, mock_namespace, mock_messages,
                        mock_message):
    message = api_client.namespaces.first().messages.first()
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
def test_thread_folder(api_client, mock_folder_namespace, mock_threads):
    namespace = api_client.namespaces.first()
    thread = namespace.threads.first()
    assert len(thread.labels) == 0
    assert len(thread.folders) == 1
    assert thread.folders[0].display_name == 'Inbox'
    assert not thread.unread
    assert thread.starred


@responses.activate
def test_thread_change(api_client, mock_folder_namespace,
                       mock_threads, mock_thread):
    namespace = api_client.namespaces.first()
    thread = namespace.threads.first()

    assert thread.starred
    thread.unstar()
    assert not thread.starred

    thread.update_folder('qwer')
    assert len(thread.folders) == 1
    assert thread.folders[0].id == 'qwer'

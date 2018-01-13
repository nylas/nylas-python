import os
import re
import json
import copy
import cgi
import random
import string
import pytest
import responses
from nylas import APIClient

# pylint: disable=redefined-outer-name,too-many-lines


def generate_id(size=25, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


@pytest.fixture
def message_body():
    return {
        "busy": True,
        "calendar_id": "94rssh7bd3rmsxsp19kiocxze",
        "description": None,
        "id": "cv4ei7syx10uvsxbs21ccsezf",
        "location": "1 Infinite loop, Cupertino",
        "message_id": None,
        "namespace_id": "384uhp3aj8l7rpmv9s2y2rukn",
        "object": "event",
        "owner": None,
        "participants": [],
        "read_only": False,
        "status": "confirmed",
        "title": "The rain song",
        "when": {
            "end_time": 1441056790,
            "object": "timespan",
            "start_time": 1441053190
        }
    }

@pytest.fixture
def api_url():
    return 'https://localhost:2222'


@pytest.fixture
def account_id():
    return '4ennivvrcgsqytgybfk912dto'


@pytest.fixture
def app_id():
    return 'fake-app-id'


@pytest.fixture
def api_client(api_url):
    return APIClient(None, None, None, api_url)


@pytest.fixture
def mocked_responses():
    rmock = responses.RequestsMock(assert_all_requests_are_fired=False)
    with rmock:
        yield rmock


@pytest.fixture
def mock_save_draft(mocked_responses, api_url):
    save_endpoint = re.compile(api_url + '/drafts/')
    response_body = json.dumps({
        "id": "4dl0ni6vxomazo73r5oydo16k",
        "version": "4dw0ni6txomazo33r5ozdo16j"
    })
    mocked_responses.add(
        responses.POST,
        save_endpoint,
        content_type='application/json',
        status=200,
        body=response_body,
        match_querystring=True
    )


@pytest.fixture
def mock_account(mocked_responses, api_url, account_id):
    response_body = json.dumps(
        {
            "account_id": account_id,
            "email_address": "ben.bitdiddle1861@gmail.com",
            "id": account_id,
            "name": "Ben Bitdiddle",
            "object": "account",
            "provider": "gmail",
            "organization_unit": "label",
            "billing_state": "paid",
        }
    )
    mocked_responses.add(
        responses.GET,
        re.compile(api_url + '/account/?'),
        content_type='application/json',
        status=200,
        body=response_body,
    )


@pytest.fixture
def mock_accounts(mocked_responses, api_url, account_id, app_id):
    response_body = json.dumps([
        {
            "account_id": account_id,
            "email_address": "ben.bitdiddle1861@gmail.com",
            "id": account_id,
            "name": "Ben Bitdiddle",
            "object": "account",
            "provider": "gmail",
            "organization_unit": "label",
            "billing_state": "paid",
        }
    ])
    url_re = "{base}(/a/{app_id})?/accounts/?".format(base=api_url, app_id=app_id)
    mocked_responses.add(
        responses.GET,
        re.compile(url_re),
        content_type='application/json',
        status=200,
        body=response_body,
    )


@pytest.fixture
def mock_folder_account(mocked_responses, api_url, account_id):
    response_body = json.dumps(
        {
            "email_address": "ben.bitdiddle1861@office365.com",
            "id": account_id,
            "name": "Ben Bitdiddle",
            "account_id": account_id,
            "object": "account",
            "provider": "eas",
            "organization_unit": "folder"
        }
    )
    mocked_responses.add(
        responses.GET,
        api_url + '/account',
        content_type='application/json',
        status=200,
        body=response_body,
        match_querystring=True
    )


@pytest.fixture
def mock_labels(mocked_responses, api_url, account_id):
    response_body = json.dumps([
        {
            "display_name": "Important",
            "id": "anuep8pe5ugmxrucchrzba2o8",
            "name": "important",
            "account_id": account_id,
            "object": "label"
        },
        {
            "display_name": "Trash",
            "id": "f1xgowbgcehk235xiy3c3ek42",
            "name": "trash",
            "account_id": account_id,
            "object": "label"
        },
        {
            "display_name": "Sent Mail",
            "id": "ah14wp5fvypvjjnplh7nxgb4h",
            "name": "sent",
            "account_id": account_id,
            "object": "label"
        },
        {
            "display_name": "All Mail",
            "id": "ah14wp5fvypvjjnplh7nxgb4h",
            "name": "all",
            "account_id": account_id,
            "object": "label"
        },
        {
            "display_name": "Inbox",
            "id": "dc11kl3s9lj4760g6zb36spms",
            "name": "inbox",
            "account_id": account_id,
            "object": "label"
        }
    ])
    endpoint = re.compile(api_url + '/labels.*')
    mocked_responses.add(
        responses.GET,
        endpoint,
        content_type='application/json',
        status=200,
        body=response_body,
    )


@pytest.fixture
def mock_label(mocked_responses, api_url, account_id):
    response_body = json.dumps(
        {
            "display_name": "Important",
            "id": "anuep8pe5ugmxrucchrzba2o8",
            "name": "important",
            "account_id": account_id,
            "object": "label"
        }
    )
    url = api_url + '/labels/anuep8pe5ugmxrucchrzba2o8'
    mocked_responses.add(
        responses.GET,
        url,
        content_type='application/json',
        status=200,
        body=response_body,
    )


@pytest.fixture
def mock_folder(mocked_responses, api_url, account_id):
    folder = {
        "display_name": "My Folder",
        "id": "anuep8pe5ug3xrupchwzba2o8",
        "name": None,
        "account_id": account_id,
        "object": "folder"
        }
    response_body = json.dumps(folder)
    url = api_url + '/folders/anuep8pe5ug3xrupchwzba2o8'
    mocked_responses.add(
        responses.GET,
        url,
        content_type='application/json',
        status=200,
        body=response_body,
    )

    def request_callback(request):
        payload = json.loads(request.body)
        if 'display_name' in payload:
            folder.update(payload)
        return (200, {}, json.dumps(folder))

    mocked_responses.add_callback(
        responses.PUT,
        url,
        content_type='application/json',
        callback=request_callback,
    )


@pytest.fixture
def mock_messages(mocked_responses, api_url, account_id):
    response_body = json.dumps([
        {
            "id": "1234",
            "subject": "Test Message",
            "account_id": account_id,
            "object": "message",
            "labels": [
                {
                    "name": "inbox",
                    "display_name": "Inbox",
                    "id": "abcd"
                }
            ],
            "starred": False,
            "unread": True,
            "date": 1265077342,
        }, {
            "id": "1238",
            "subject": "Test Message 2",
            "account_id": account_id,
            "object": "message",
            "labels": [
                {
                    "name": "inbox",
                    "display_name": "Inbox",
                    "id": "abcd"
                }
            ],
            "starred": False,
            "unread": True,
            "date": 1265085342,
        }, {
            "id": "12",
            "subject": "Test Message 3",
            "account_id": account_id,
            "object": "message",
            "labels": [
                {
                    "name": "archive",
                    "display_name": "Archive",
                    "id": "gone"
                }
            ],
            "starred": False,
            "unread": False,
            "date": 1265093842,
        }
    ])
    endpoint = re.compile(api_url + '/messages')
    mocked_responses.add(
        responses.GET,
        endpoint,
        content_type='application/json',
        status=200,
        body=response_body
    )


@pytest.fixture
def mock_message(mocked_responses, api_url, account_id):
    base_msg = {
        "id": "1234",
        "subject": "Test Message",
        "account_id": account_id,
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

    endpoint = re.compile(api_url + '/messages/1234')
    mocked_responses.add(
        responses.GET,
        endpoint,
        content_type='application/json',
        status=200,
        body=response_body
    )
    mocked_responses.add_callback(
        responses.PUT,
        endpoint,
        content_type='application/json',
        callback=request_callback
    )
    mocked_responses.add(
        responses.DELETE,
        endpoint,
        content_type='application/json',
        status=200,
        body="",
    )


@pytest.fixture
def mock_threads(mocked_responses, api_url, account_id):
    response_body = json.dumps([
        {
            "id": "5678",
            "subject": "Test Thread",
            "account_id": account_id,
            "object": "thread",
            "folders": [{
                "name": "inbox",
                "display_name": "Inbox",
                "id": "abcd"
            }],
            "starred": True,
            "unread": False,
            "first_message_timestamp": 1451703845,
            "last_message_timestamp": 1483326245,
            "last_message_received_timestamp": 1483326245,
            "last_message_sent_timestamp": 1483232461,
        }
    ])
    endpoint = re.compile(api_url + '/threads')
    mocked_responses.add(
        responses.GET,
        endpoint,
        content_type='application/json',
        status=200,
        body=response_body
    )


@pytest.fixture
def mock_thread(mocked_responses, api_url, account_id):
    base_thrd = {
        "id": "5678",
        "subject": "Test Thread",
        "account_id": account_id,
        "object": "thread",
        "folders": [{
            "name": "inbox",
            "display_name": "Inbox",
            "id": "abcd"
        }],
        "starred": True,
        "unread": False,
        "first_message_timestamp": 1451703845,
        "last_message_timestamp": 1483326245,
        "last_message_received_timestamp": 1483326245,
        "last_message_sent_timestamp": 1483232461,
    }
    response_body = json.dumps(base_thrd)

    def request_callback(request):
        payload = json.loads(request.body)
        if 'folder' in payload:
            folder = {'name': 'test', 'display_name': 'test',
                      'id': payload['folder']}
            base_thrd['folders'] = [folder]
        return (200, {}, json.dumps(base_thrd))

    endpoint = re.compile(api_url + '/threads/5678')
    mocked_responses.add(
        responses.GET,
        endpoint,
        content_type='application/json',
        status=200,
        body=response_body
    )
    mocked_responses.add_callback(
        responses.PUT,
        endpoint,
        content_type='application/json',
        callback=request_callback,
    )


@pytest.fixture
def mock_labelled_thread(mocked_responses, api_url, account_id):
    base_thread = {
        "id": "111",
        "subject": "Labelled Thread",
        "account_id": account_id,
        "object": "thread",
        "folders": [{
            "name": "inbox",
            "display_name": "Inbox",
            "id": "abcd"
        }],
        "starred": True,
        "unread": False,
        "labels": [
            {
                "display_name": "Important",
                "id": "anuep8pe5ugmxrucchrzba2o8",
                "name": "important",
                "account_id": account_id,
                "object": "label"
            }, {
                "display_name": "Existing",
                "id": "dfslhgy3rlijfhlsujnchefs3",
                "name": "existing",
                "account_id": account_id,
                "object": "label"
            }
        ],
        "first_message_timestamp": 1451703845,
        "last_message_timestamp": 1483326245,
        "last_message_received_timestamp": 1483326245,
        "last_message_sent_timestamp": 1483232461,
    }
    response_body = json.dumps(base_thread)

    def request_callback(request):
        payload = json.loads(request.body)
        if 'labels' in payload:
            existing_labels = {
                label["id"]: label
                for label in base_thread["labels"]
            }
            new_labels = []
            for label_id in payload['labels']:
                if label_id in existing_labels:
                    new_labels.append(existing_labels[label_id])
                else:
                    new_labels.append({
                        "name": "updated",
                        "display_name": "Updated",
                        "id": label_id,
                        "account_id": account_id,
                        "object": "label",
                    })
            copied = copy.copy(base_thread)
            copied["labels"] = new_labels
        return (200, {}, json.dumps(copied))

    endpoint = re.compile(api_url + '/threads/111')
    mocked_responses.add(
        responses.GET,
        endpoint,
        content_type='application/json',
        status=200,
        body=response_body
    )
    mocked_responses.add_callback(
        responses.PUT,
        endpoint,
        content_type='application/json',
        callback=request_callback,
    )


@pytest.fixture
def mock_drafts(mocked_responses, api_url):
    response_body = json.dumps([{
        "bcc": [],
        "body": "Cheers mate!",
        "cc": [],
        "date": 1438684486,
        "events": [],
        "files": [],
        "folder": None,
        "from": [],
        "id": "2h111aefv8pzwzfykrn7hercj",
        "namespace_id": "384uhp3aj8l7rpmv9s2y2rukn",
        "object": "draft",
        "reply_to": [],
        "reply_to_message_id": None,
        "snippet": "",
        "starred": False,
        "subject": "Here's an attachment",
        "thread_id": "clm33kapdxkposgltof845v9s",
        "to": [
            {
                "email": "helena@nylas.com",
                "name": "Helena Handbasket"
            }
        ],
        "unread": False,
        "version": 0
    }])

    mocked_responses.add(
        responses.GET,
        api_url + '/drafts',
        content_type='application/json',
        status=200,
        body=response_body,
    )


@pytest.fixture
def mock_draft_saved_response(mocked_responses, api_url):
    draft_json = {
        "bcc": [],
        "body": "Cheers mate!",
        "cc": [],
        "date": 1438684486,
        "events": [],
        "files": [],
        "folder": None,
        "from": [],
        "id": "2h111aefv8pzwzfykrn7hercj",
        "namespace_id": "384uhp3aj8l7rpmv9s2y2rukn",
        "object": "draft",
        "reply_to": [],
        "reply_to_message_id": None,
        "snippet": "",
        "starred": False,
        "subject": "Here's an attachment",
        "thread_id": "clm33kapdxkposgltof845v9s",
        "to": [
            {
                "email": "helena@nylas.com",
                "name": "Helena Handbasket"
            }
        ],
        "unread": False,
        "version": 0,
    }

    def create_callback(_request):
        return (200, {}, json.dumps(draft_json))

    def update_callback(request):
        try:
            payload = json.loads(request.body)
        except ValueError:
            return (200, {}, json.dumps(draft_json))

        stripped_payload = {
            key: value for key, value in payload.items() if value
        }
        updated_draft_json = copy.copy(draft_json)
        updated_draft_json.update(stripped_payload)
        updated_draft_json["version"] += 1
        return (200, {}, json.dumps(updated_draft_json))

    mocked_responses.add_callback(
        responses.POST,
        api_url + '/drafts/',
        content_type='application/json',
        callback=create_callback,
    )

    mocked_responses.add_callback(
        responses.PUT,
        api_url + '/drafts/2h111aefv8pzwzfykrn7hercj',
        content_type='application/json',
        callback=update_callback,
    )


@pytest.fixture
def mock_draft_deleted_response(mocked_responses, api_url):
    mocked_responses.add(
        responses.DELETE,
        api_url + '/drafts/2h111aefv8pzwzfykrn7hercj',
        content_type='application/json',
        status=200,
        body="",
    )


@pytest.fixture
def mock_draft_sent_response(mocked_responses, api_url):
    body = {
        "bcc": [],
        "body": "",
        "cc": [],
        "date": 1438684486,
        "events": [],
        "files": [],
        "folder": None,
        "from": [{'email': 'benb@nylas.com'}],
        "id": "2h111aefv8pzwzfykrn7hercj",
        "namespace_id": "384uhp3aj8l7rpmv9s2y2rukn",
        "object": "draft",
        "reply_to": [],
        "reply_to_message_id": None,
        "snippet": "",
        "starred": False,
        "subject": "Stay polish, stay hungary",
        "thread_id": "clm33kapdxkposgltof845v9s",
        "to": [
            {
                "email": "helena@nylas.com",
                "name": "Helena Handbasket"
            }
        ],
        "unread": False,
        "version": 0,
    }

    values = [(400, {}, "Couldn't send email"),
              (200, {}, json.dumps(body))]

    def callback(request):
        payload = json.loads(request.body)
        assert payload['draft_id'] == '2h111aefv8pzwzfykrn7hercj'
        return values.pop()

    mocked_responses.add_callback(
        responses.POST,
        api_url + '/send/',
        callback=callback,
        content_type='application/json'
    )


@pytest.fixture
def mock_files(mocked_responses, api_url, account_id):
    files_content = {
        "3qfe4k3siosfjtjpfdnon8zbn": b"Hello, World!",
    }
    files_metadata = {
        "3qfe4k3siosfjtjpfdnon8zbn": {
            "id": "3qfe4k3siosfjtjpfdnon8zbn",
            "content_type": "text/plain",
            "filename": "hello.txt",
            "account_id": account_id,
            "object": "file",
            "size": len(files_content["3qfe4k3siosfjtjpfdnon8zbn"])
        }
    }
    mocked_responses.add(
        responses.GET,
        api_url + '/files',
        body=json.dumps(list(files_metadata.values())),
    )
    for file_id in files_content:
        mocked_responses.add(
            responses.POST,
            "{base}/files/{file_id}".format(base=api_url, file_id=file_id),
            body=json.dumps(files_metadata[file_id]),
        )
        mocked_responses.add(
            responses.GET,
            "{base}/files/{file_id}/download".format(base=api_url, file_id=file_id),
            body=files_content[file_id],
        )

    def create_callback(request):
        uploaded_lines = request.body.decode('utf8').splitlines()
        content_disposition = uploaded_lines[1]
        _, params = cgi.parse_header(content_disposition)
        filename = params.get("filename", None)
        content = "".join(uploaded_lines[3:-1])
        size = len(content.encode('utf8'))

        body = [{
            "id": generate_id(),
            "content_type": "text/plain",
            "filename": filename,
            "account_id": account_id,
            "object": "file",
            "size": size,
        }]
        return (200, {}, json.dumps(body))

    mocked_responses.add_callback(
        responses.POST,
        api_url + '/files/',
        callback=create_callback,
    )


@pytest.fixture
def mock_event_create_response(mocked_responses, api_url, message_body):
    values = [(400, {}, ""),
              (200, {}, json.dumps(message_body))]

    def callback(_request):
        return values.pop()

    mocked_responses.add_callback(
        responses.POST,
        api_url + '/events/',
        callback=callback,
    )

    put_body = {'title': 'loaded from JSON', 'ignored': 'ignored'}
    mocked_responses.add(
        responses.PUT,
        api_url + '/events/cv4ei7syx10uvsxbs21ccsezf',
        body=json.dumps(put_body)
    )


@pytest.fixture
def mock_event_create_notify_response(mocked_responses, api_url, message_body):
    mocked_responses.add(
        responses.POST,
        api_url + '/events/?notify_participants=true&other_param=1',
        body=json.dumps(message_body),
    )



@pytest.fixture
def mock_thread_search_response(mocked_responses, api_url):
    snippet = (
        "Hey Helena, Looking forward to getting together for dinner on Friday. "
        "What can I bring? I have a couple bottles of wine or could put together"
    )
    response_body = json.dumps([
        {
            "id": "evh5uy0shhpm5d0le89goor17",
            "object": "thread",
            "account_id": "awa6ltos76vz5hvphkp8k17nt",
            "subject": "Dinner Party on Friday",
            "unread": False,
            "starred": False,
            "last_message_timestamp": 1398229259,
            "last_message_received_timestamp": 1398229259,
            "first_message_timestamp": 1298229259,
            "participants": [
                {
                    "name": "Ben Bitdiddle",
                    "email": "ben.bitdiddle@gmail.com"
                },
            ],
            "snippet": snippet,
            "folders": [
                {
                    "name": "inbox",
                    "display_name": "INBOX",
                    "id": "f0idlvozkrpj3ihxze7obpivh"
                },
            ],
            "message_ids": [
                "251r594smznew6yhiocht2v29",
                "7upzl8ss738iz8xf48lm84q3e",
                "ah5wuphj3t83j260jqucm9a28"
            ],
            "draft_ids": [
                "251r594smznew6yhi12312saq"
            ],
            "version": 2
        }
    ])

    mocked_responses.add(
        responses.GET,
        api_url + '/threads/search?q=Helena',
        body=response_body,
        status=200,
        content_type='application/json',
        match_querystring=True
    )

@pytest.fixture
def mock_message_search_response(mocked_responses, api_url):
    snippet = (
        "Sounds good--that bottle of Pinot should go well with the meal. "
        "I'll also bring a surprise for dessert. :) "
        "Do you have ice cream? Looking fo"
    )
    response_body = json.dumps([
        {
            "id": "84umizq7c4jtrew491brpa6iu",
            "object": "message",
            "account_id": "14e5bn96uizyuhidhcw5rfrb0",
            "thread_id": "5vryyrki4fqt7am31uso27t3f",
            "subject": "Re: Dinner on Friday?",
            "from": [
                {
                    "name": "Ben Bitdiddle",
                    "email": "ben.bitdiddle@gmail.com"
                }
            ],
            "to": [
                {
                    "name": "Bill Rogers",
                    "email": "wbrogers@mit.edu"
                }
            ],
            "cc": [],
            "bcc": [],
            "reply_to": [],
            "date": 1370084645,
            "unread": True,
            "starred": False,
            "folder": {
                "name": "inbox",
                "display_name": "INBOX",
                "id": "f0idlvozkrpj3ihxze7obpivh"
            },
            "snippet": snippet,
            "body": "<html><body>....</body></html>",
            "files": [],
            "events": []
        },
        {
            "id": "84umizq7asdf3aw491brpa6iu",
            "object": "message",
            "account_id": "14e5bakdsfljskidhcw5rfrb0",
            "thread_id": "5vryyralskdjfwlj1uso27t3f",
            "subject": "Re: Dinner on Friday?",
            "from": [
                {
                    "name": "Ben Bitdiddle",
                    "email": "ben.bitdiddle@gmail.com"
                }
            ],
            "to": [
                {
                    "name": "Bill Rogers",
                    "email": "wbrogers@mit.edu"
                }
            ],
            "cc": [],
            "bcc": [],
            "reply_to": [],
            "date": 1370084645,
            "unread": True,
            "starred": False,
            "folder": {
                "name": "inbox",
                "display_name": "INBOX",
                "id": "f0idlvozkrpj3ihxze7obpivh"
            },
            "snippet": snippet,
            "body": "<html><body>....</body></html>",
            "files": [],
            "events": []
        }
    ])

    mocked_responses.add(
        responses.GET,
        api_url + '/messages/search?q=Pinot',
        body=response_body,
        status=200,
        content_type='application/json',
        match_querystring=True
    )


@pytest.fixture
def mock_calendars(mocked_responses, api_url):
    response_body = json.dumps([
        {
            "id": "8765",
            "events": [
                {
                    "title": "Pool party",
                    "location": "Local Community Pool",
                    "participants": [
                        "Alice",
                        "Bob",
                        "Claire",
                        "Dot",
                    ]
                }
            ],
        }
    ])
    endpoint = re.compile(api_url + '/calendars')
    mocked_responses.add(
        responses.GET,
        endpoint,
        content_type='application/json',
        status=200,
        body=response_body
    )



@pytest.fixture
def mock_contacts(mocked_responses, account_id, api_url):
    contact1 = {
        'id': '5x6b54whvcz1j22ggiyorhk9v',
        'object': 'contact',
        'account_id': account_id,
        'given_name': 'Charlie',
        'middle_name': None,
        'surname': 'Bucket',
        'birthday': "1964-10-05",
        'suffix': None,
        'nickname': None,
        'company_name': None,
        'job_title': "Student",
        'manager_name': None,
        'office_location': None,
        'notes': None,
        'picture_url': "{base}/contacts/{id}/picture".format(
            base=api_url, id='5x6b54whvcz1j22ggiyorhk9v'
        ),
        'email_addresses': [{'email': 'charlie@gmail.com', 'type': None}],
        'im_addresses': [],
        'physical_addresses': [],
        'phone_numbers': [],
        'web_pages': [],
    }
    contact2 = {
        'id': '4zqkfw8k1d12h0k784ipeh498',
        'object': 'contact',
        'account_id': account_id,
        'given_name': 'William',
        'middle_name': 'J',
        'surname': 'Wonka',
        'birthday': "1955-02-28",
        'suffix': None,
        'nickname': None,
        'company_name': None,
        'job_title': "Chocolate Artist",
        'manager_name': None,
        'office_location': "Willy Wonka Factory",
        'notes': None,
        'picture_url': None,
        'email_addresses': [{'email': 'scrumptious@wonka.com', 'type': None}],
        'im_addresses': [],
        'physical_addresses': [],
        'phone_numbers': [],
        'web_pages': [{"type": "work", "url": "http://www.wonka.com"}],
    }
    contact3 = {
        'id': '9fn1aoi2i00qv6h1zpag6b26w',
        'object': 'contact',
        'account_id': account_id,
        'given_name': 'Oompa',
        'middle_name': None,
        'surname': 'Loompa',
        'birthday': None,
        'suffix': None,
        'nickname': None,
        'company_name': None,
        'job_title': None,
        'manager_name': None,
        'office_location': "Willy Wonka Factory",
        'notes': None,
        'picture_url': None,
        'email_addresses': [],
        'im_addresses': [],
        'physical_addresses': [],
        'phone_numbers': [],
        'web_pages': [],
    }
    contacts = [contact1, contact2, contact3]

    def create_callback(request):
        payload = json.loads(request.body)
        payload["id"] = generate_id()
        return (200, {}, json.dumps(payload))

    for contact in contacts:
        mocked_responses.add(
            responses.GET,
            re.compile(api_url + '/contacts/' + contact["id"]),
            content_type='application/json',
            status=200,
            body=json.dumps(contact)
        )
        if contact.get("picture_url"):
            mocked_responses.add(
                responses.GET,
                contact["picture_url"],
                content_type='image/jpeg',
                status=200,
                body=os.urandom(50),
                stream=True,
            )
        else:
            mocked_responses.add(
                responses.GET,
                "{base}/contacts/{id}/picture".format(
                    base=api_url, id=contact["id"],
                ),
                status=404,
                body=""
            )
    mocked_responses.add(
        responses.GET,
        re.compile(api_url + '/contacts'),
        content_type='application/json',
        status=200,
        body=json.dumps(contacts)
    )
    mocked_responses.add_callback(
        responses.POST,
        api_url + '/contacts/',
        content_type='application/json',
        callback=create_callback,
    )


@pytest.fixture
def mock_contact(mocked_responses, account_id, api_url):
    contact = {
        'id': '9hga75n6mdvq4zgcmhcn7hpys',
        'object': 'contact',
        'account_id': account_id,
        'given_name': 'Given',
        'middle_name': 'Middle',
        'surname': 'Sur',
        'birthday': "1964-10-05",
        'suffix': 'Jr',
        'nickname': 'Testy',
        'company_name': "Test Data Inc",
        'job_title': "QA Tester",
        'manager_name': "George",
        'office_location': "Over the Rainbow",
        'notes': "This is a note",
        'picture_url': "{base}/contacts/{id}/picture".format(
            base=api_url, id='9hga75n6mdvq4zgcmhcn7hpys'
        ),
        'email_addresses': [
            {"type": "first", "email": "one@example.com"},
            {"type": "second", "email": "two@example.com"},
            {"type": "primary", "email": "abc@example.com"},
            {"type": "primary", "email": "xyz@example.com"},
            {"type": None, "email": "unknown@example.com"},
        ],
        'im_addresses': [
            {"type": "aim", "im_address": "SmarterChild"},
            {"type": "gtalk", "im_address": "fake@gmail.com"},
            {"type": "gtalk", "im_address": "fake2@gmail.com"},
        ],
        'physical_addresses': [
            {
                "type": "home",
                "format": "structured",
                "street_address": "123 Awesome Street",
                "postal_code": "99989",
                "state": "CA",
                "country": "America",
            }
        ],
        'phone_numbers': [
            {"type": "home", "number": "555-555-5555"},
            {"type": "mobile", "number": "555-555-5555"},
            {"type": "mobile", "number": "987654321"},
        ],
        'web_pages': [
            {"type": "profile", "url": "http://www.facebook.com/abc"},
            {"type": "profile", "url": "http://www.twitter.com/abc"},
            {"type": None, "url": "http://example.com"},
        ],
    }

    def update_callback(request):
        try:
            payload = json.loads(request.body)
        except ValueError:
            return (200, {}, json.dumps(contact))

        stripped_payload = {
            key: value for key, value in payload.items() if value
        }
        updated_contact_json = copy.copy(contact)
        updated_contact_json.update(stripped_payload)
        return (200, {}, json.dumps(updated_contact_json))

    mocked_responses.add(
        responses.GET,
        "{base}/contacts/{id}".format(
            base=api_url, id=contact["id"]
        ),
        content_type='application/json',
        status=200,
        body=json.dumps(contact)
    )
    mocked_responses.add(
        responses.GET,
        contact["picture_url"],
        content_type='image/jpeg',
        status=200,
        body=os.urandom(50),
        stream=True,
    )

    mocked_responses.add_callback(
        responses.PUT,
        "{base}/contacts/{id}".format(
            base=api_url, id=contact["id"]
        ),
        content_type='application/json',
        callback=update_callback,
    )


@pytest.fixture
def mock_events(mocked_responses, api_url):
    response_body = json.dumps([
        {
            "title": "Pool party",
            "location": "Local Community Pool",
            "participants": [
                {
                    "comment": None,
                    "email": "kelly@nylas.com",
                    "name": "Kelly Nylanaut",
                    "status": "noreply",
                }, {
                    "comment": None,
                    "email": "sarah@nylas.com",
                    "name": "Sarah Nylanaut",
                    "status": "no",
                },
            ]
        }
    ])
    endpoint = re.compile(api_url + '/events')
    mocked_responses.add(
        responses.GET,
        endpoint,
        content_type='application/json',
        status=200,
        body=response_body
    )


@pytest.fixture
def mock_account_management(mocked_responses, api_url, account_id, app_id):
    account = {
        "account_id": account_id,
        "email_address": "ben.bitdiddle1861@gmail.com",
        "id": account_id,
        "name": "Ben Bitdiddle",
        "object": "account",
        "provider": "gmail",
        "organization_unit": "label",
        "billing_state": "paid",
    }
    paid_response = json.dumps(account)
    account["billing_state"] = "cancelled"
    cancelled_response = json.dumps(account)

    upgrade_url = "{base}/a/{app_id}/accounts/{id}/upgrade".format(
        base=api_url, id=account_id, app_id=app_id,
    )
    downgrade_url = "{base}/a/{app_id}/accounts/{id}/downgrade".format(
        base=api_url, id=account_id, app_id=app_id,
    )
    mocked_responses.add(
        responses.POST,
        upgrade_url,
        content_type='application/json',
        status=200,
        body=paid_response,
    )
    mocked_responses.add(
        responses.POST,
        downgrade_url,
        content_type='application/json',
        status=200,
        body=cancelled_response,
    )

import re
import json
import copy
import pytest
import responses
import httpretty
from nylas import APIClient

# pylint: disable=redefined-outer-name


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
    return 'http://localhost:2222'


@pytest.fixture
def account_id():
    return '4ennivvrcgsqytgybfk912dto'


@pytest.fixture
def api_client(api_url):
    return APIClient(None, None, None, api_url)


@pytest.fixture
def mock_save_draft(api_url):
    save_endpoint = re.compile(api_url + '/drafts/')
    response_body = json.dumps({
        "id": "4dl0ni6vxomazo73r5oydo16k",
        "version": "4dw0ni6txomazo33r5ozdo16j"
    })
    responses.add(
        responses.POST,
        save_endpoint,
        content_type='application/json',
        status=200,
        body=response_body,
        match_querystring=True
    )


@pytest.fixture
def mock_account(api_url, account_id):
    response_body = json.dumps(
        {
            "account_id": account_id,
            "email_address": "ben.bitdiddle1861@gmail.com",
            "id": account_id,
            "name": "Ben Bitdiddle",
            "object": "account",
            "provider": "gmail",
            "organization_unit": "label"
        }
    )
    responses.add(
        responses.GET,
        api_url + '/account',
        content_type='application/json',
        status=200,
        body=response_body,
        match_querystring=True
    )


@pytest.fixture
def mock_folder_account(api_url, account_id):
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
    responses.add(
        responses.GET,
        api_url + '/account',
        content_type='application/json',
        status=200,
        body=response_body,
        match_querystring=True
    )


@pytest.fixture
def mock_labels(api_url, account_id):
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
    responses.add(
        responses.GET,
        endpoint,
        content_type='application/json',
        status=200,
        body=response_body,
    )


@pytest.fixture
def mock_label(api_url, account_id):
    response_body = json.dumps(
        {
            "display_name": "Important",
            "id": "anuep8pe5ugmxrucchrzba2o8",
            "name": "important",
            "account_id": account_id,
            "object": "label"
        }
    )
    endpoint = re.compile(api_url + '/labels/anuep8pe5ugmxrucchrzba2o8')
    responses.add(
        responses.GET,
        endpoint,
        content_type='application/json',
        status=200,
        body=response_body,
    )


@pytest.fixture
def mock_folder(api_url, account_id):
    folder = {
        "display_name": "My Folder",
        "id": "anuep8pe5ug3xrupchwzba2o8",
        "name": None,
        "account_id": account_id,
        "object": "folder"
        }
    response_body = json.dumps(folder)
    endpoint = re.compile(api_url + '/folders/anuep8pe5ug3xrupchwzba2o8')
    responses.add(
        responses.GET,
        endpoint,
        content_type='application/json',
        status=200,
        body=response_body,
    )

    def request_callback(request):
        payload = json.loads(request.body)
        if 'display_name' in payload:
            folder.update(payload)
        return (200, {}, json.dumps(folder))

    responses.add_callback(
        responses.PUT,
        endpoint,
        content_type='application/json',
        callback=request_callback,
    )



@pytest.fixture
def mock_messages(api_url, account_id):
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
            "unread": True
        }
    ])
    endpoint = re.compile(api_url + '/messages')
    responses.add(
        responses.GET,
        endpoint,
        content_type='application/json',
        status=200,
        body=response_body)


@pytest.fixture
def mock_message(api_url, account_id):
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
    responses.add(
        responses.GET,
        endpoint,
        content_type='application/json',
        status=200,
        body=response_body
    )
    responses.add_callback(
        responses.PUT,
        endpoint,
        content_type='application/json',
        callback=request_callback
    )


@pytest.fixture
def mock_threads(api_url, account_id):
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
            "unread": False
        }
    ])
    endpoint = re.compile(api_url + '/threads')
    responses.add(
        responses.GET,
        endpoint,
        content_type='application/json',
        status=200,
        body=response_body
    )


@pytest.fixture
def mock_thread(api_url, account_id):
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

    endpoint = re.compile(api_url + '/threads/5678')
    responses.add(
        responses.GET,
        endpoint,
        content_type='application/json',
        status=200,
        body=response_body
    )
    responses.add_callback(
        responses.PUT,
        endpoint,
        content_type='application/json',
        callback=request_callback,
    )


@pytest.fixture
def mock_labelled_thread(api_url, account_id):
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
        ]
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
    responses.add(
        responses.GET,
        endpoint,
        content_type='application/json',
        status=200,
        body=response_body
    )
    responses.add_callback(
        responses.PUT,
        endpoint,
        content_type='application/json',
        callback=request_callback,
    )


@pytest.fixture
def mock_drafts(api_url):
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

    responses.add(
        responses.GET,
        api_url + '/drafts',
        content_type='application/json',
        status=200,
        body=response_body,
    )


@pytest.fixture
def mock_draft_saved_response(api_url):
    response_body = json.dumps({
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
    })

    responses.add(
        responses.POST,
        api_url + '/drafts/',
        content_type='application/json',
        status=200,
        body=response_body,
        match_querystring=True
    )


@pytest.fixture
def mock_draft_updated_response(api_url):
    body = {
        "bcc": [],
        "body": "",
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
        "subject": "Stay polish, stay hungary",
        "thread_id": "clm33kapdxkposgltof845v9s",
        "to": [
            {
                "email": "helena@nylas.com",
                "name": "Helena Handbasket"
            }
        ],
        "unread": False,
        "version": 0
    }

    responses.add(
        responses.PUT,
        api_url + '/drafts/2h111aefv8pzwzfykrn7hercj',
        content_type='application/json',
        status=200,
        body=json.dumps(body),
        match_querystring=True
    )

    body['subject'] = 'Update #2'
    url = api_url + '/drafts/2h111aefv8pzwzfykrn7hercj?random_query=true&param2=param'
    responses.add(
        responses.PUT,
        url,
        content_type='application/json',
        status=200,
        body=json.dumps(body),
        match_querystring=True
    )


@pytest.fixture
def mock_draft_sent_response(api_url):
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
        "version": 0
    }

    values = [(400, {}, "Couldn't send email"),
              (200, {}, json.dumps(body))]

    def callback(request):
        payload = json.loads(request.body)
        assert payload['draft_id'] == '2h111aefv8pzwzfykrn7hercj'
        assert payload['version'] == 0
        return values.pop()

    responses.add_callback(
        responses.POST,
        api_url + '/send/',
        callback=callback,
        content_type='application/json'
    )


@pytest.fixture
def mock_files(api_url):
    httpretty.enable()
    body = [{
        "content_type": "text/plain",
        "filename": "a.txt",
        "id": "3qfe4k3siosfjtjpfdnon8zbn",
        "account_id": "6aakaxzi4j5gn6f7kbb9e0fxs",
        "object": "file",
        "size": 762878
    }]

    values = [httpretty.Response(status=200, body=json.dumps(body))]
    httpretty.register_uri(httpretty.POST, api_url + '/files/', responses=values)
    httpretty.register_uri(httpretty.GET, api_url + '/files/3qfe4k3siosfjtjpfdnon8zbn/download',
                           body='test body')

@pytest.fixture
def mock_event_create_response(api_url, message_body):
    httpretty.enable()
    values = [
        httpretty.Response(status=200, body=json.dumps(message_body)),
        httpretty.Response(status=400, body=''),
    ]

    httpretty.register_uri(httpretty.POST, api_url + '/events/', responses=values)

    body = json.dumps({'title': 'loaded from JSON', 'ignored': 'ignored'})
    put_values = [
        httpretty.Response(status=200, body=body)
    ]
    httpretty.register_uri(
        httpretty.PUT,
        api_url + '/events/cv4ei7syx10uvsxbs21ccsezf',
        responses=put_values,
    )


@pytest.fixture
def mock_event_create_notify_response(api_url, message_body):
    httpretty.enable()
    httpretty.register_uri(
        httpretty.POST,
        api_url + '/events/?notify_participants=true&other_param=1',
        body=json.dumps(message_body),
        status=200
    )



@pytest.fixture
def mock_thread_search_response(api_url):
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

    responses.add(
        responses.GET,
        api_url + '/threads/search?q=Helena',
        body=response_body,
        status=200,
        content_type='application/json',
        match_querystring=True
    )

@pytest.fixture
def mock_message_search_response(api_url):
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

    responses.add(
        responses.GET,
        api_url + '/messages/search?q=Pinot',
        body=response_body,
        status=200,
        content_type='application/json',
        match_querystring=True
    )

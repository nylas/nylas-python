import os
import re
import json
import copy
import cgi
import random
import string
import pytest
import responses
from urlobject import URLObject
from nylas import APIClient

# pylint: disable=redefined-outer-name,too-many-lines

#### HANDLING PAGINATION ####
# Currently, the Nylas API handles pagination poorly: API responses do not expose
# any information about pagination, so the client does not know whether there is
# another page of data or not. For example, if the client sends an API request
# without a limit specified, and the response contains 100 items, how can it tell
# if there are 100 items in total, or if there more items to fetch on the next page?
# It can't! The only way to know is to ask for the next page (by repeating the API
# request with `offset=100`), and see if you get more items or not.
# If it does not receive more items, it can assume that it has retrieved all the data.
#
# This file contains mocks for several API endpoints, including "list" endpoints
# like `/messages` and `/events`. The mocks for these list endpoints must be smart
# enough to check for an `offset` query param, and return an empty list if the
# client requests more data than the first page. If the mock does not
# check for this `offset` query param, and returns the same mock data over and over,
# any SDK method that tries to fetch *all* of a certain type of data
# (like `client.messages.all()`) will never complete.


def generate_id(size=25, chars=string.ascii_letters + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


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
            "start_time": 1441053190,
        },
    }


@pytest.fixture
def access_token():
    return "l3m0n_w4ter"


@pytest.fixture
def account_id():
    return "4ennivvrcgsqytgybfk912dto"


@pytest.fixture
def api_url():
    return "https://localhost:2222"


@pytest.fixture
def client_id():
    return "fake-client-id"


@pytest.fixture
def client_secret():
    return "nyl4n4ut"


@pytest.fixture
def api_client(api_url):
    return APIClient(
        client_id=None, client_secret=None, access_token=None, api_server=api_url
    )


@pytest.fixture
def api_client_with_client_id(access_token, api_url, client_id, client_secret):
    return APIClient(
        client_id=client_id,
        client_secret=client_secret,
        access_token=access_token,
        api_server=api_url,
    )


@pytest.fixture
def mocked_responses():
    rmock = responses.RequestsMock(assert_all_requests_are_fired=False)
    with rmock:
        yield rmock


@pytest.fixture
def mock_save_draft(mocked_responses, api_url):
    save_endpoint = re.compile(api_url + "/drafts")
    response_body = json.dumps(
        {"id": "4dl0ni6vxomazo73r5oydo16k", "version": "4dw0ni6txomazo33r5ozdo16j"}
    )
    mocked_responses.add(
        responses.POST,
        save_endpoint,
        content_type="application/json",
        status=200,
        body=response_body,
        match_querystring=True,
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
            "linked_at": 1500920299,
            "sync_state": "running",
        }
    )
    mocked_responses.add(
        responses.GET,
        re.compile(api_url + "/account(?!s)/?"),
        content_type="application/json",
        status=200,
        body=response_body,
    )


@pytest.fixture
def mock_accounts(mocked_responses, api_url, account_id, client_id):
    accounts = [
        {
            "account_id": account_id,
            "email_address": "ben.bitdiddle1861@gmail.com",
            "id": account_id,
            "name": "Ben Bitdiddle",
            "object": "account",
            "provider": "gmail",
            "organization_unit": "label",
            "billing_state": "paid",
            "linked_at": 1500920299,
            "sync_state": "running",
        }
    ]

    def list_callback(request):
        url = URLObject(request.url)
        offset = int(url.query_dict.get("offset") or 0)
        if offset:
            return (200, {}, json.dumps([]))
        return (200, {}, json.dumps(accounts))

    def update_callback(request):
        response = accounts[0]
        payload = json.loads(request.body)
        if payload["metadata"]:
            response["metadata"] = payload["metadata"]
        return 200, {}, json.dumps(response)

    def delete_callback(request):
        response = {"success": True}
        return 200, {}, json.dumps(response)

    url_re = "{base}(/a/{client_id})?/accounts/?".format(
        base=api_url, client_id=client_id
    )
    mocked_responses.add_callback(
        responses.GET,
        re.compile(url_re),
        content_type="application/json",
        callback=list_callback,
    )
    mocked_responses.add_callback(
        responses.PUT,
        re.compile(url_re),
        content_type="application/json",
        callback=update_callback,
    )
    mocked_responses.add_callback(
        responses.DELETE,
        re.compile(url_re),
        content_type="application/json",
        callback=delete_callback,
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
            "organization_unit": "folder",
        }
    )
    mocked_responses.add(
        responses.GET,
        api_url + "/account",
        content_type="application/json",
        status=200,
        body=response_body,
        match_querystring=True,
    )


@pytest.fixture
def mock_labels(mocked_responses, api_url, account_id):
    labels = [
        {
            "display_name": "Important",
            "id": "anuep8pe5ugmxrucchrzba2o8",
            "name": "important",
            "account_id": account_id,
            "object": "label",
        },
        {
            "display_name": "Trash",
            "id": "f1xgowbgcehk235xiy3c3ek42",
            "name": "trash",
            "account_id": account_id,
            "object": "label",
        },
        {
            "display_name": "Sent Mail",
            "id": "ah14wp5fvypvjjnplh7nxgb4h",
            "name": "sent",
            "account_id": account_id,
            "object": "label",
        },
        {
            "display_name": "All Mail",
            "id": "ah14wp5fvypvjjnplh7nxgb4h",
            "name": "all",
            "account_id": account_id,
            "object": "label",
        },
        {
            "display_name": "Inbox",
            "id": "dc11kl3s9lj4760g6zb36spms",
            "name": "inbox",
            "account_id": account_id,
            "object": "label",
        },
    ]

    def list_callback(request):
        url = URLObject(request.url)
        offset = int(url.query_dict.get("offset") or 0)
        if offset:
            return (200, {}, json.dumps([]))
        return (200, {}, json.dumps(labels))

    endpoint = re.compile(api_url + "/labels.*")
    mocked_responses.add_callback(
        responses.GET,
        endpoint,
        content_type="application/json",
        callback=list_callback,
    )


@pytest.fixture
def mock_label(mocked_responses, api_url, account_id):
    response_body = json.dumps(
        {
            "display_name": "Important",
            "id": "anuep8pe5ugmxrucchrzba2o8",
            "name": "important",
            "account_id": account_id,
            "object": "label",
        }
    )
    url = api_url + "/labels/anuep8pe5ugmxrucchrzba2o8"
    mocked_responses.add(
        responses.GET,
        url,
        content_type="application/json",
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
        "object": "folder",
    }
    response_body = json.dumps(folder)
    url = api_url + "/folders/anuep8pe5ug3xrupchwzba2o8"
    mocked_responses.add(
        responses.GET,
        url,
        content_type="application/json",
        status=200,
        body=response_body,
    )

    def request_callback(request):
        payload = json.loads(request.body)
        if "display_name" in payload:
            folder.update(payload)
        return (200, {}, json.dumps(folder))

    def delete_callback(request):
        payload = {"successful": True}
        return 200, {}, json.dumps(payload)

    mocked_responses.add_callback(
        responses.PUT, url, content_type="application/json", callback=request_callback
    )

    mocked_responses.add_callback(
        responses.DELETE, url, content_type="application/json", callback=delete_callback
    )


@pytest.fixture
def mock_messages(mocked_responses, api_url, account_id):
    messages = [
        {
            "id": "1234",
            "to": [{"email": "foo@yahoo.com", "name": "Foo"}],
            "from": [{"email": "bar@gmail.com", "name": "Bar"}],
            "subject": "Test Message",
            "account_id": account_id,
            "object": "message",
            "labels": [{"name": "inbox", "display_name": "Inbox", "id": "abcd"}],
            "starred": False,
            "unread": True,
            "date": 1265077342,
        },
        {
            "id": "1238",
            "to": [{"email": "foo2@yahoo.com", "name": "Foo Two"}],
            "from": [{"email": "bar2@gmail.com", "name": "Bar Two"}],
            "subject": "Test Message 2",
            "account_id": account_id,
            "object": "message",
            "labels": [{"name": "inbox", "display_name": "Inbox", "id": "abcd"}],
            "starred": False,
            "unread": True,
            "date": 1265085342,
        },
        {
            "id": "12",
            "to": [{"email": "foo3@yahoo.com", "name": "Foo Three"}],
            "from": [{"email": "bar3@gmail.com", "name": "Bar Three"}],
            "subject": "Test Message 3",
            "account_id": account_id,
            "object": "message",
            "labels": [{"name": "archive", "display_name": "Archive", "id": "gone"}],
            "starred": False,
            "unread": False,
            "date": 1265093842,
        },
    ]

    def list_callback(request):
        url = URLObject(request.url)
        offset = int(url.query_dict.get("offset") or 0)
        if offset:
            return (200, {}, json.dumps([]))
        return (200, {}, json.dumps(messages))

    endpoint = re.compile(api_url + "/messages")
    mocked_responses.add_callback(
        responses.GET, endpoint, content_type="application/json", callback=list_callback
    )


@pytest.fixture
def mock_message(mocked_responses, api_url, account_id):
    base_msg = {
        "id": "1234",
        "to": [{"email": "foo@yahoo.com", "name": "Foo"}],
        "from": [{"email": "bar@gmail.com", "name": "Bar"}],
        "subject": "Test Message",
        "account_id": account_id,
        "object": "message",
        "labels": [{"name": "inbox", "display_name": "Inbox", "id": "abcd"}],
        "starred": False,
        "unread": True,
    }
    response_body = json.dumps(base_msg)

    def request_callback(request):
        payload = json.loads(request.body)
        if "labels" in payload:
            labels = [
                {"name": "test", "display_name": "test", "id": l}
                for l in payload["labels"]
            ]
            base_msg["labels"] = labels
        if "metadata" in payload:
            base_msg["metadata"] = payload["metadata"]
        return (200, {}, json.dumps(base_msg))

    endpoint = re.compile(api_url + "/messages/1234")
    mocked_responses.add(
        responses.GET,
        endpoint,
        content_type="application/json",
        status=200,
        body=response_body,
    )
    mocked_responses.add_callback(
        responses.PUT,
        endpoint,
        content_type="application/json",
        callback=request_callback,
    )
    mocked_responses.add(
        responses.DELETE, endpoint, content_type="application/json", status=200, body=""
    )


@pytest.fixture
def mock_threads(mocked_responses, api_url, account_id):
    threads = [
        {
            "id": "5678",
            "subject": "Test Thread",
            "account_id": account_id,
            "object": "thread",
            "folders": [{"name": "inbox", "display_name": "Inbox", "id": "abcd"}],
            "starred": True,
            "unread": False,
            "first_message_timestamp": 1451703845,
            "last_message_timestamp": 1483326245,
            "last_message_received_timestamp": 1483326245,
            "last_message_sent_timestamp": 1483232461,
        }
    ]

    def list_callback(request):
        url = URLObject(request.url)
        offset = int(url.query_dict.get("offset") or 0)
        if offset:
            return (200, {}, json.dumps([]))
        return (200, {}, json.dumps(threads))

    endpoint = re.compile(api_url + "/threads")
    mocked_responses.add_callback(
        responses.GET,
        endpoint,
        content_type="application/json",
        callback=list_callback,
    )


@pytest.fixture
def mock_thread(mocked_responses, api_url, account_id):
    base_thrd = {
        "id": "5678",
        "subject": "Test Thread",
        "account_id": account_id,
        "object": "thread",
        "folders": [{"name": "inbox", "display_name": "Inbox", "id": "abcd"}],
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
        if "folder" in payload:
            folder = {"name": "test", "display_name": "test", "id": payload["folder"]}
            base_thrd["folders"] = [folder]
        return (200, {}, json.dumps(base_thrd))

    endpoint = re.compile(api_url + "/threads/5678")
    mocked_responses.add(
        responses.GET,
        endpoint,
        content_type="application/json",
        status=200,
        body=response_body,
    )
    mocked_responses.add_callback(
        responses.PUT,
        endpoint,
        content_type="application/json",
        callback=request_callback,
    )


@pytest.fixture
def mock_labelled_thread(mocked_responses, api_url, account_id):
    base_thread = {
        "id": "111",
        "subject": "Labelled Thread",
        "account_id": account_id,
        "object": "thread",
        "folders": [{"name": "inbox", "display_name": "Inbox", "id": "abcd"}],
        "starred": True,
        "unread": False,
        "labels": [
            {
                "display_name": "Important",
                "id": "anuep8pe5ugmxrucchrzba2o8",
                "name": "important",
                "account_id": account_id,
                "object": "label",
            },
            {
                "display_name": "Existing",
                "id": "dfslhgy3rlijfhlsujnchefs3",
                "name": "existing",
                "account_id": account_id,
                "object": "label",
            },
        ],
        "first_message_timestamp": 1451703845,
        "last_message_timestamp": 1483326245,
        "last_message_received_timestamp": 1483326245,
        "last_message_sent_timestamp": 1483232461,
    }
    response_body = json.dumps(base_thread)

    def request_callback(request):
        payload = json.loads(request.body)
        if "labels" in payload:
            existing_labels = {label["id"]: label for label in base_thread["labels"]}
            new_labels = []
            for label_id in payload["labels"]:
                if label_id in existing_labels:
                    new_labels.append(existing_labels[label_id])
                else:
                    new_labels.append(
                        {
                            "name": "updated",
                            "display_name": "Updated",
                            "id": label_id,
                            "account_id": account_id,
                            "object": "label",
                        }
                    )
            copied = copy.copy(base_thread)
            copied["labels"] = new_labels
        return (200, {}, json.dumps(copied))

    endpoint = re.compile(api_url + "/threads/111")
    mocked_responses.add(
        responses.GET,
        endpoint,
        content_type="application/json",
        status=200,
        body=response_body,
    )
    mocked_responses.add_callback(
        responses.PUT,
        endpoint,
        content_type="application/json",
        callback=request_callback,
    )


@pytest.fixture
def mock_drafts(mocked_responses, api_url):
    drafts = [
        {
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
            "to": [{"email": "helena@nylas.com", "name": "Helena Handbasket"}],
            "unread": False,
            "version": 0,
        }
    ]

    def list_callback(request):
        url = URLObject(request.url)
        offset = int(url.query_dict.get("offset") or 0)
        if offset:
            return (200, {}, json.dumps([]))
        return (200, {}, json.dumps(drafts))

    mocked_responses.add_callback(
        responses.GET,
        api_url + "/drafts",
        content_type="application/json",
        callback=list_callback,
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
        "to": [{"email": "helena@nylas.com", "name": "Helena Handbasket"}],
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

        stripped_payload = {key: value for key, value in payload.items() if value}
        updated_draft_json = copy.copy(draft_json)
        updated_draft_json.update(stripped_payload)
        updated_draft_json["version"] += 1
        return (200, {}, json.dumps(updated_draft_json))

    mocked_responses.add_callback(
        responses.POST,
        api_url + "/drafts",
        content_type="application/json",
        callback=create_callback,
    )

    mocked_responses.add_callback(
        responses.PUT,
        api_url + "/drafts/2h111aefv8pzwzfykrn7hercj",
        content_type="application/json",
        callback=update_callback,
    )


@pytest.fixture
def mock_draft_deleted_response(mocked_responses, api_url):
    mocked_responses.add(
        responses.DELETE,
        api_url + "/drafts/2h111aefv8pzwzfykrn7hercj",
        content_type="application/json",
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
        "from": [{"email": "benb@nylas.com"}],
        "id": "2h111aefv8pzwzfykrn7hercj",
        "namespace_id": "384uhp3aj8l7rpmv9s2y2rukn",
        "object": "draft",
        "reply_to": [],
        "reply_to_message_id": None,
        "snippet": "",
        "starred": False,
        "subject": "Stay polish, stay hungary",
        "thread_id": "clm33kapdxkposgltof845v9s",
        "to": [{"email": "helena@nylas.com", "name": "Helena Handbasket"}],
        "unread": False,
        "version": 0,
    }

    values = [(400, {}, "Couldn't send email"), (200, {}, json.dumps(body))]

    def callback(request):
        payload = json.loads(request.body)
        assert payload["draft_id"] == "2h111aefv8pzwzfykrn7hercj"
        return values.pop()

    mocked_responses.add_callback(
        responses.POST,
        api_url + "/send",
        callback=callback,
        content_type="application/json",
    )


@pytest.fixture
def mock_draft_send_unsaved_response(mocked_responses, api_url):
    def callback(request):
        payload = json.loads(request.body)
        payload["draft_id"] = "2h111aefv8pzwzfykrn7hercj"
        return 200, {}, json.dumps(payload)

    mocked_responses.add_callback(
        responses.POST,
        api_url + "/send",
        callback=callback,
        content_type="application/json",
    )


@pytest.fixture
def mock_files(mocked_responses, api_url, account_id):
    files_content = {"3qfe4k3siosfjtjpfdnon8zbn": b"Hello, World!"}
    files_metadata = {
        "3qfe4k3siosfjtjpfdnon8zbn": {
            "id": "3qfe4k3siosfjtjpfdnon8zbn",
            "content_type": "text/plain",
            "filename": "hello.txt",
            "account_id": account_id,
            "object": "file",
            "size": len(files_content["3qfe4k3siosfjtjpfdnon8zbn"]),
        }
    }
    mocked_responses.add(
        responses.GET,
        api_url + "/files",
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
        uploaded_lines = request.body.decode("utf8").splitlines()
        content_disposition = uploaded_lines[1]
        _, params = cgi.parse_header(content_disposition)
        filename = params.get("filename", None)
        content = "".join(uploaded_lines[3:-1])
        size = len(content.encode("utf8"))

        body = [
            {
                "id": generate_id(),
                "content_type": "text/plain",
                "filename": filename,
                "account_id": account_id,
                "object": "file",
                "size": size,
            }
        ]
        return (200, {}, json.dumps(body))

    mocked_responses.add_callback(
        responses.POST, api_url + "/files", callback=create_callback
    )


@pytest.fixture
def mock_event_create_response(mocked_responses, api_url, message_body):
    def callback(_request):
        try:
            payload = json.loads(_request.body)
        except ValueError:
            return 400, {}, ""

        payload["id"] = "cv4ei7syx10uvsxbs21ccsezf"
        return 200, {}, json.dumps(payload)

    mocked_responses.add_callback(
        responses.POST, api_url + "/events", callback=callback
    )

    put_body = {"title": "loaded from JSON", "ignored": "ignored"}
    mocked_responses.add(
        responses.PUT,
        api_url + "/events/cv4ei7syx10uvsxbs21ccsezf",
        body=json.dumps(put_body),
    )


@pytest.fixture
def mock_event_generate_ics(mocked_responses, api_url, message_body):
    mocked_responses.add(
        responses.POST, api_url + "/events/to-ics", body=json.dumps({"ics": ""})
    )


@pytest.fixture
def mock_scheduler_create_response(mocked_responses, api_url, message_body):
    def callback(_request):
        try:
            payload = json.loads(_request.body)
        except ValueError:
            return 400, {}, ""

        payload["id"] = "cv4ei7syx10uvsxbs21ccsezf"
        return 200, {}, json.dumps(payload)

    mocked_responses.add_callback(
        responses.POST, "https://api.schedule.nylas.com/manage/pages", callback=callback
    )

    mocked_responses.add(
        responses.PUT,
        "https://api.schedule.nylas.com/manage/pages/cv4ei7syx10uvsxbs21ccsezf",
        body=json.dumps(message_body),
    )


@pytest.fixture
def mock_event_create_response_with_limits(mocked_responses, api_url, message_body):
    def callback(request):
        url = URLObject(request.url)
        limit = int(url.query_dict.get("limit") or 50)
        body = [message_body for _ in range(0, limit)]
        return 200, {}, json.dumps(body)

    mocked_responses.add_callback(responses.GET, api_url + "/events", callback=callback)


@pytest.fixture
def mock_event_create_notify_response(mocked_responses, api_url, message_body):
    mocked_responses.add(
        responses.POST,
        api_url + "/events?notify_participants=true&other_param=1",
        body=json.dumps(message_body),
    )


@pytest.fixture
def mock_send_rsvp(mocked_responses, api_url, message_body):
    mocked_responses.add(
        responses.POST,
        re.compile(api_url + "/send-rsvp"),
        body=json.dumps(message_body),
    )


@pytest.fixture
def mock_components_create_response(mocked_responses, api_url, message_body):
    def callback(_request):
        try:
            payload = json.loads(_request.body)
        except ValueError:
            return 400, {}, ""

        payload["id"] = "cv4ei7syx10uvsxbs21ccsezf"
        return 200, {}, json.dumps(payload)

    mocked_responses.add_callback(
        responses.POST, re.compile(api_url + "/component/*"), callback=callback
    )

    mocked_responses.add(
        responses.PUT,
        re.compile(api_url + "/component/*"),
        body=json.dumps(message_body),
    )


@pytest.fixture
def mock_thread_search_response(mocked_responses, api_url):
    snippet = (
        "Hey Helena, Looking forward to getting together for dinner on Friday. "
        "What can I bring? I have a couple bottles of wine or could put together"
    )
    response_body = json.dumps(
        [
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
                    {"name": "Ben Bitdiddle", "email": "ben.bitdiddle@gmail.com"}
                ],
                "snippet": snippet,
                "folders": [
                    {
                        "name": "inbox",
                        "display_name": "INBOX",
                        "id": "f0idlvozkrpj3ihxze7obpivh",
                    }
                ],
                "message_ids": [
                    "251r594smznew6yhiocht2v29",
                    "7upzl8ss738iz8xf48lm84q3e",
                    "ah5wuphj3t83j260jqucm9a28",
                ],
                "draft_ids": ["251r594smznew6yhi12312saq"],
                "version": 2,
            }
        ]
    )

    mocked_responses.add(
        responses.GET,
        api_url + "/threads/search?q=Helena",
        body=response_body,
        status=200,
        content_type="application/json",
        match_querystring=True,
    )


@pytest.fixture
def mock_message_search_response(mocked_responses, api_url):
    snippet = (
        "Sounds good--that bottle of Pinot should go well with the meal. "
        "I'll also bring a surprise for dessert. :) "
        "Do you have ice cream? Looking fo"
    )
    response_body = json.dumps(
        [
            {
                "id": "84umizq7c4jtrew491brpa6iu",
                "object": "message",
                "account_id": "14e5bn96uizyuhidhcw5rfrb0",
                "thread_id": "5vryyrki4fqt7am31uso27t3f",
                "subject": "Re: Dinner on Friday?",
                "from": [{"name": "Ben Bitdiddle", "email": "ben.bitdiddle@gmail.com"}],
                "to": [{"name": "Bill Rogers", "email": "wbrogers@mit.edu"}],
                "cc": [],
                "bcc": [],
                "reply_to": [],
                "date": 1370084645,
                "unread": True,
                "starred": False,
                "folder": {
                    "name": "inbox",
                    "display_name": "INBOX",
                    "id": "f0idlvozkrpj3ihxze7obpivh",
                },
                "snippet": snippet,
                "body": "<html><body>....</body></html>",
                "files": [],
                "events": [],
            },
            {
                "id": "84umizq7asdf3aw491brpa6iu",
                "object": "message",
                "account_id": "14e5bakdsfljskidhcw5rfrb0",
                "thread_id": "5vryyralskdjfwlj1uso27t3f",
                "subject": "Re: Dinner on Friday?",
                "from": [{"name": "Ben Bitdiddle", "email": "ben.bitdiddle@gmail.com"}],
                "to": [{"name": "Bill Rogers", "email": "wbrogers@mit.edu"}],
                "cc": [],
                "bcc": [],
                "reply_to": [],
                "date": 1370084645,
                "unread": True,
                "starred": False,
                "folder": {
                    "name": "inbox",
                    "display_name": "INBOX",
                    "id": "f0idlvozkrpj3ihxze7obpivh",
                },
                "snippet": snippet,
                "body": "<html><body>....</body></html>",
                "files": [],
                "events": [],
            },
        ]
    )

    mocked_responses.add(
        responses.GET,
        api_url + "/messages/search?q=Pinot",
        body=response_body,
        status=200,
        content_type="application/json",
        match_querystring=True,
    )


@pytest.fixture
def mock_calendars(mocked_responses, api_url):
    calendars = [
        {
            "id": "8765",
            "events": [
                {
                    "title": "Pool party",
                    "location": "Local Community Pool",
                    "participants": ["Alice", "Bob", "Claire", "Dot"],
                }
            ],
        }
    ]

    def list_callback(request):
        url = URLObject(request.url)
        offset = int(url.query_dict.get("offset") or 0)
        if offset:
            return (200, {}, json.dumps([]))
        return (200, {}, json.dumps(calendars))

    endpoint = re.compile(api_url + "/calendars")
    mocked_responses.add_callback(
        responses.GET,
        endpoint,
        content_type="application/json",
        callback=list_callback,
    )


@pytest.fixture
def mock_contacts(mocked_responses, account_id, api_url):
    contact1 = {
        "id": "5x6b54whvcz1j22ggiyorhk9v",
        "object": "contact",
        "account_id": account_id,
        "given_name": "Charlie",
        "middle_name": None,
        "surname": "Bucket",
        "birthday": "1964-10-05",
        "suffix": None,
        "nickname": None,
        "company_name": None,
        "job_title": "Student",
        "manager_name": None,
        "office_location": None,
        "notes": None,
        "picture_url": "{base}/contacts/{id}/picture".format(
            base=api_url, id="5x6b54whvcz1j22ggiyorhk9v"
        ),
        "emails": [{"email": "charlie@gmail.com", "type": None}],
        "im_addresses": [],
        "physical_addresses": [],
        "phone_numbers": [],
        "web_pages": [],
    }
    contact2 = {
        "id": "4zqkfw8k1d12h0k784ipeh498",
        "object": "contact",
        "account_id": account_id,
        "given_name": "William",
        "middle_name": "J",
        "surname": "Wonka",
        "birthday": "1955-02-28",
        "suffix": None,
        "nickname": None,
        "company_name": None,
        "job_title": "Chocolate Artist",
        "manager_name": None,
        "office_location": "Willy Wonka Factory",
        "notes": None,
        "picture_url": None,
        "emails": [{"email": "scrumptious@wonka.com", "type": None}],
        "im_addresses": [],
        "physical_addresses": [],
        "phone_numbers": [],
        "web_pages": [{"type": "work", "url": "http://www.wonka.com"}],
    }
    contact3 = {
        "id": "9fn1aoi2i00qv6h1zpag6b26w",
        "object": "contact",
        "account_id": account_id,
        "given_name": "Oompa",
        "middle_name": None,
        "surname": "Loompa",
        "birthday": None,
        "suffix": None,
        "nickname": None,
        "company_name": None,
        "job_title": None,
        "manager_name": None,
        "office_location": "Willy Wonka Factory",
        "notes": None,
        "picture_url": None,
        "emails": [],
        "im_addresses": [],
        "physical_addresses": [],
        "phone_numbers": [],
        "web_pages": [],
    }
    contacts = [contact1, contact2, contact3]

    def list_callback(request):
        url = URLObject(request.url)
        offset = int(url.query_dict.get("offset") or 0)
        if offset:
            return (200, {}, json.dumps([]))
        return (200, {}, json.dumps(contacts))

    def create_callback(request):
        payload = json.loads(request.body)
        payload["id"] = generate_id()
        return (200, {}, json.dumps(payload))

    for contact in contacts:
        mocked_responses.add(
            responses.GET,
            re.compile(api_url + "/contacts/" + contact["id"]),
            content_type="application/json",
            status=200,
            body=json.dumps(contact),
        )
        if contact.get("picture_url"):
            mocked_responses.add(
                responses.GET,
                contact["picture_url"],
                content_type="image/jpeg",
                status=200,
                body=os.urandom(50),
                stream=True,
            )
        else:
            mocked_responses.add(
                responses.GET,
                "{base}/contacts/{id}/picture".format(base=api_url, id=contact["id"]),
                status=404,
                body="",
            )
    mocked_responses.add_callback(
        responses.GET,
        re.compile(api_url + "/contacts"),
        content_type="application/json",
        callback=list_callback,
    )
    mocked_responses.add_callback(
        responses.POST,
        api_url + "/contacts",
        content_type="application/json",
        callback=create_callback,
    )


@pytest.fixture
def mock_contact(mocked_responses, account_id, api_url):
    contact = {
        "id": "9hga75n6mdvq4zgcmhcn7hpys",
        "object": "contact",
        "account_id": account_id,
        "given_name": "Given",
        "middle_name": "Middle",
        "surname": "Sur",
        "birthday": "1964-10-05",
        "suffix": "Jr",
        "nickname": "Testy",
        "company_name": "Test Data Inc",
        "job_title": "QA Tester",
        "manager_name": "George",
        "office_location": "Over the Rainbow",
        "source": "inbox",
        "notes": "This is a note",
        "picture_url": "{base}/contacts/{id}/picture".format(
            base=api_url, id="9hga75n6mdvq4zgcmhcn7hpys"
        ),
        "emails": [
            {"type": "first", "email": "one@example.com"},
            {"type": "second", "email": "two@example.com"},
            {"type": "primary", "email": "abc@example.com"},
            {"type": "primary", "email": "xyz@example.com"},
            {"type": None, "email": "unknown@example.com"},
        ],
        "im_addresses": [
            {"type": "aim", "im_address": "SmarterChild"},
            {"type": "gtalk", "im_address": "fake@gmail.com"},
            {"type": "gtalk", "im_address": "fake2@gmail.com"},
        ],
        "physical_addresses": [
            {
                "type": "home",
                "format": "structured",
                "street_address": "123 Awesome Street",
                "postal_code": "99989",
                "state": "CA",
                "country": "America",
            }
        ],
        "phone_numbers": [
            {"type": "home", "number": "555-555-5555"},
            {"type": "mobile", "number": "555-555-5555"},
            {"type": "mobile", "number": "987654321"},
        ],
        "web_pages": [
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

        stripped_payload = {key: value for key, value in payload.items() if value}
        updated_contact_json = copy.copy(contact)
        updated_contact_json.update(stripped_payload)
        return (200, {}, json.dumps(updated_contact_json))

    mocked_responses.add(
        responses.GET,
        "{base}/contacts/{id}".format(base=api_url, id=contact["id"]),
        content_type="application/json",
        status=200,
        body=json.dumps(contact),
    )
    mocked_responses.add(
        responses.GET,
        contact["picture_url"],
        content_type="image/jpeg",
        status=200,
        body=os.urandom(50),
        stream=True,
    )

    mocked_responses.add_callback(
        responses.PUT,
        "{base}/contacts/{id}".format(base=api_url, id=contact["id"]),
        content_type="application/json",
        callback=update_callback,
    )


@pytest.fixture
def mock_events(mocked_responses, api_url):
    events = [
        {
            "id": "1234abcd5678",
            "message_id": "evh5uy0shhpm5d0le89goor17",
            "ical_uid": "19960401T080045Z-4000F192713-0052@example.com",
            "title": "Pool party",
            "location": "Local Community Pool",
            "participants": [
                {
                    "comment": None,
                    "email": "kelly@nylas.com",
                    "name": "Kelly Nylanaut",
                    "status": "noreply",
                },
                {
                    "comment": None,
                    "email": "sarah@nylas.com",
                    "name": "Sarah Nylanaut",
                    "status": "no",
                },
            ],
            "metadata": {},
        },
        {
            "id": "9876543cba",
            "message_id": None,
            "ical_uid": None,
            "title": "Event Without Message",
            "description": "This event does not have a corresponding message ID.",
            "metadata": {},
        },
        {
            "id": "1231241zxc",
            "message_id": None,
            "ical_uid": None,
            "title": "Event With Metadata",
            "description": "This event uses metadata to store custom values.",
            "metadata": {"platform": "python", "event_type": "meeting"},
        },
    ]

    def list_callback(request):
        url = URLObject(request.url)
        offset = int(url.query_dict.get("offset") or 0)
        metadata_key = url.query_multi_dict.get("metadata_key")
        metadata_value = url.query_multi_dict.get("metadata_value")
        metadata_pair = url.query_multi_dict.get("metadata_pair")

        if offset:
            return (200, {}, json.dumps([]))
        if metadata_key or metadata_value or metadata_pair:
            results = []
            for event in events:
                if (
                    metadata_key
                    and set(metadata_key) & set(event["metadata"])
                    or metadata_value
                    and set(metadata_value) & set(event["metadata"].values())
                ):
                    results.append(event)
                elif metadata_pair:
                    for pair in metadata_pair:
                        key_value = pair.split(":")
                        if (
                            key_value[0] in event["metadata"]
                            and event["metadata"][key_value[0]] == key_value[1]
                        ):
                            results.append(event)
            return (200, {}, json.dumps(results))
        return (200, {}, json.dumps(events))

    endpoint = re.compile(api_url + "/events")
    mocked_responses.add_callback(
        responses.GET, endpoint, content_type="application/json", callback=list_callback
    )


@pytest.fixture
def mock_schedulers(mocked_responses, api_url):
    scheduler_list = [
        {
            "app_client_id": "test-client-id",
            "app_organization_id": 12345,
            "config": {
                "appearance": {
                    "color": "#0068D3",
                    "company_name": "",
                    "logo": "",
                    "show_autoschedule": "true",
                    "show_nylas_branding": "false",
                    "show_timezone_options": "true",
                    "show_week_view": "true",
                    "submit_text": "Submit",
                },
                "locale": "en",
                "reminders": [],
                "timezone": "America/Los_Angeles",
            },
            "created_at": "2021-10-22",
            "edit_token": "test-edit-token-1",
            "id": 90210,
            "modified_at": "2021-10-22",
            "name": "test-1",
            "slug": "test1",
        },
        {
            "app_client_id": "test-client-id",
            "app_organization_id": 12345,
            "config": {
                "calendar_ids": {
                    "test-calendar-id": {
                        "availability": ["availability-id"],
                        "booking": "booking-id",
                    }
                },
                "event": {
                    "capacity": -1,
                    "duration": 45,
                    "location": "Location TBD",
                    "title": "test-event",
                },
                "locale": "en",
                "reminders": [],
                "timezone": "America/Los_Angeles",
            },
            "created_at": "2021-10-22",
            "edit_token": "test-edit-token-2",
            "id": 90211,
            "modified_at": "2021-10-22",
            "name": "test-2",
            "slug": "test2",
        },
    ]

    def list_callback(arg=None):
        return 200, {}, json.dumps(scheduler_list)

    def return_one_callback(arg=None):
        return 200, {}, json.dumps(scheduler_list[0])

    info_endpoint = re.compile("https://api.schedule.nylas.com/schedule/.*/info")

    mocked_responses.add_callback(
        responses.GET,
        "https://api.schedule.nylas.com/manage/pages",
        content_type="application/json",
        callback=list_callback,
    )

    mocked_responses.add_callback(
        responses.GET,
        info_endpoint,
        content_type="application/json",
        callback=return_one_callback,
    )


@pytest.fixture
def mock_scheduler_get_available_calendars(mocked_responses, api_url):
    calendars = [
        {
            "calendars": [
                {"id": "calendar-id", "name": "Emailed events", "read_only": "true"},
            ],
            "email": "swag@nylas.com",
            "id": "scheduler-id",
            "name": "Python Tester",
        }
    ]

    def list_callback(arg=None):
        return 200, {}, json.dumps(calendars)

    calendars_url = "https://api.schedule.nylas.com/manage/pages/{id}/calendars".format(
        id="cv4ei7syx10uvsxbs21ccsezf"
    )

    mocked_responses.add_callback(
        responses.GET,
        calendars_url,
        content_type="application/json",
        callback=list_callback,
    )


@pytest.fixture
def mock_scheduler_upload_image(mocked_responses, api_url):
    upload = {
        "filename": "test.png",
        "originalFilename": "test.png",
        "publicUrl": "https://public.nylas.com/test.png",
        "signedUrl": "https://signed.nylas.com/test.png",
    }

    def list_callback(arg=None):
        return 200, {}, json.dumps(upload)

    calendars_url = (
        "https://api.schedule.nylas.com/manage/pages/{id}/upload-image".format(
            id="cv4ei7syx10uvsxbs21ccsezf"
        )
    )

    mocked_responses.add_callback(
        responses.PUT,
        calendars_url,
        content_type="application/json",
        callback=list_callback,
    )


@pytest.fixture
def mock_scheduler_provider_availability(mocked_responses, api_url):
    response = {
        "busy": [
            {
                "end": 1636731958,
                "start": 1636728347,
            },
        ],
        "email": "test@example.com",
        "name": "John Doe",
    }

    def callback(arg=None):
        return 200, {}, json.dumps(response)

    provider_url = re.compile(
        "https://api.schedule.nylas.com/schedule/availability/(google|o365)"
    )

    mocked_responses.add_callback(
        responses.GET,
        provider_url,
        callback=callback,
    )


@pytest.fixture
def mock_scheduler_timeslots(mocked_responses, api_url):
    scheduler_time_slots = [
        {
            "account_id": "test-account-id",
            "calendar_id": "test-calendar-id",
            "emails": ["test@example.com"],
            "end": 1636731958,
            "host_name": "www.hostname.com",
            "start": 1636728347,
        },
    ]

    booking_confirmation = {
        "account_id": "test-account-id",
        "additional_field_values": {
            "test": "yes",
        },
        "calendar_event_id": "test-event-id",
        "calendar_id": "test-calendar-id",
        "edit_hash": "test-edit-hash",
        "end_time": 1636731958,
        "id": 123,
        "is_confirmed": False,
        "location": "Earth",
        "recipient_email": "recipient@example.com",
        "recipient_locale": "en_US",
        "recipient_name": "Recipient Doe",
        "recipient_tz": "America/New_York",
        "start_time": 1636728347,
        "title": "Test Booking",
    }

    cancel_payload = {
        "success": True,
    }

    def list_timeslots(arg=None):
        return 200, {}, json.dumps(scheduler_time_slots)

    def book_timeslot(arg=None):
        return 200, {}, json.dumps(booking_confirmation)

    def confirm_booking(arg=None):
        booking_confirmation["is_confirmed"] = True
        return 200, {}, json.dumps(booking_confirmation)

    def cancel_booking(arg=None):
        return 200, {}, json.dumps(cancel_payload)

    timeslots_url = re.compile("https://api.schedule.nylas.com/schedule/.*/timeslots")

    confirm_url = re.compile("https://api.schedule.nylas.com/schedule/.*/.*/confirm")

    cancel_url = re.compile("https://api.schedule.nylas.com/schedule/.*/.*/cancel")

    mocked_responses.add_callback(
        responses.GET,
        timeslots_url,
        callback=list_timeslots,
    )

    mocked_responses.add_callback(
        responses.POST,
        timeslots_url,
        callback=book_timeslot,
    )

    mocked_responses.add_callback(
        responses.POST,
        confirm_url,
        callback=confirm_booking,
    )

    mocked_responses.add_callback(
        responses.POST,
        cancel_url,
        callback=cancel_booking,
    )


@pytest.fixture
def mock_components(mocked_responses, api_url):
    components = [
        {
            "active": True,
            "settings": {},
            "allowed_domains": [],
            "id": "component-id",
            "name": "PyTest Component",
            "public_account_id": "account-id",
            "public_application_id": "application-id",
            "type": "agenda",
            "created_at": "2021-10-22T18:02:10.000Z",
            "updated_at": "2021-10-22T18:02:10.000Z",
            "accessed_at": None,
            "public_token_id": "token-id",
        },
    ]

    def list_callback(arg=None):
        return 200, {}, json.dumps(components)

    endpoint = re.compile(api_url + "/component/*")
    mocked_responses.add_callback(
        responses.GET, endpoint, content_type="application/json", callback=list_callback
    )


@pytest.fixture
def mock_create_webhook(mocked_responses, api_url, client_id):
    webhook = {"application_id": "application-id", "id": "webhook-id", "version": "1.0"}

    def callback(request):
        try:
            payload = json.loads(request.body)
        except ValueError:
            return 400, {}, ""

        if (
            "callback_url" not in payload
            and ("triggers" not in payload and type(payload["triggers"]) is not list)
            and "state" not in payload
        ):
            return 400, {}, ""

        webhook["callback_url"] = payload["callback_url"]
        webhook["triggers"] = payload["triggers"]
        webhook["state"] = payload["state"]

        return 200, {}, json.dumps(webhook)

    endpoint = "{base}/a/{client_id}/webhooks".format(base=api_url, client_id=client_id)
    mocked_responses.add_callback(
        responses.POST,
        endpoint,
        callback=callback,
        content_type="application/json",
    )


@pytest.fixture
def mock_webhooks(mocked_responses, api_url, client_id):
    webhook = {
        "application_id": "application-id",
        "callback_url": "https://your-server.com/webhook",
        "id": "webhook-id",
        "state": "active",
        "triggers": ["message.created"],
        "version": "2.0",
    }

    def list_callback(request):
        return 200, {}, json.dumps([webhook])

    def single_callback(request):
        webhook["id"] = get_id_from_url(request.url)
        return 200, {}, json.dumps(webhook)

    def update_callback(request):
        try:
            payload = json.loads(request.body)
        except ValueError:
            return 400, {}, ""

        if "state" in payload:
            webhook["state"] = payload["state"]
        webhook["id"] = get_id_from_url(request.url)
        return 200, {}, json.dumps(webhook)

    def delete_callback(request):
        return 200, {}, json.dumps({"success": True})

    def get_id_from_url(url):
        path = URLObject(url).path
        return path.rsplit("/", 1)[-1]

    endpoint_single = re.compile(
        "{base}/a/{client_id}/webhooks/*".format(base=api_url, client_id=client_id)
    )
    endpoint_list = "{base}/a/{client_id}/webhooks".format(
        base=api_url, client_id=client_id
    )
    mocked_responses.add_callback(
        responses.GET,
        endpoint_list,
        content_type="application/json",
        callback=list_callback,
    )
    mocked_responses.add_callback(
        responses.GET,
        endpoint_single,
        content_type="application/json",
        callback=single_callback,
    )
    mocked_responses.add_callback(
        responses.PUT,
        endpoint_single,
        content_type="application/json",
        callback=update_callback,
    )
    mocked_responses.add_callback(
        responses.DELETE,
        endpoint_single,
        content_type="application/json",
        callback=delete_callback,
    )


@pytest.fixture
def mock_resources(mocked_responses, api_url):
    resources = [
        {
            "object": "room_resource",
            "email": "training-room-1A@google.com",
            "name": "Google Training Room",
            "building": "San Francisco",
            "capacity": "10",
            "floor_name": "7",
            "floor_number": None,
        },
        {
            "object": "room_resource",
            "email": "training-room@outlook.com",
            "name": "Microsoft Training Room",
            "building": "Seattle",
            "capacity": "5",
            "floor_name": "Office",
            "floor_number": "2",
        },
    ]

    endpoint = re.compile(api_url + "/resources")
    mocked_responses.add(
        responses.GET,
        endpoint,
        body=json.dumps(resources),
        status=200,
        content_type="application/json",
    )


@pytest.fixture
def mock_job_statuses(mocked_responses, api_url):
    job_status = [
        {
            "account_id": "test_account_id",
            "action": "save_draft",
            "created_at": 1622846160,
            "id": "test_id",
            "job_status_id": "test_job_status_id",
            "object": "message",
            "status": "successful",
        },
        {
            "account_id": "test_account_id",
            "action": "update_event",
            "created_at": 1622846160,
            "id": "test_id_2",
            "job_status_id": "test_job_status_id_2",
            "object": "event",
            "status": "successful",
        },
    ]

    endpoint = re.compile(api_url + "/job-statuses")
    mocked_responses.add(
        responses.GET,
        endpoint,
        body=json.dumps(job_status),
        status=200,
        content_type="application/json",
    )


@pytest.fixture
def mock_account_management(mocked_responses, api_url, account_id, client_id):
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

    upgrade_url = "{base}/a/{client_id}/accounts/{id}/upgrade".format(
        base=api_url, id=account_id, client_id=client_id
    )
    downgrade_url = "{base}/a/{client_id}/accounts/{id}/downgrade".format(
        base=api_url, id=account_id, client_id=client_id
    )
    mocked_responses.add(
        responses.POST,
        upgrade_url,
        content_type="application/json",
        status=200,
        body=paid_response,
    )
    mocked_responses.add(
        responses.POST,
        downgrade_url,
        content_type="application/json",
        status=200,
        body=cancelled_response,
    )


@pytest.fixture
def mock_revoke_all_tokens(mocked_responses, api_url, account_id, client_id):
    revoke_all_url = "{base}/a/{client_id}/accounts/{id}/revoke-all".format(
        base=api_url, id=account_id, client_id=client_id
    )
    mocked_responses.add(
        responses.POST,
        revoke_all_url,
        content_type="application/json",
        status=200,
        body=json.dumps({"success": True}),
    )


@pytest.fixture
def mock_application_details(mocked_responses, api_url, client_id):
    application_details_url = "{base}/a/{client_id}".format(
        base=api_url, client_id=client_id
    )

    def modify_endpoint(request):
        return 200, {}, json.dumps(json.loads(request.body))

    mocked_responses.add(
        responses.GET,
        application_details_url,
        content_type="application/json",
        status=200,
        body=json.dumps(
            {
                "application_name": "My New App Name",
                "icon_url": "http://localhost:5555/icon.png",
                "redirect_uris": [
                    "http://localhost:5555/login_callback",
                    "localhost",
                    "https://customerA.myapplication.com/login_callback",
                ],
            }
        ),
    )
    mocked_responses.add_callback(
        responses.PUT,
        application_details_url,
        content_type="application/json",
        callback=modify_endpoint,
    )


@pytest.fixture
def mock_ip_addresses(mocked_responses, api_url, client_id):
    ip_addresses_url = "{base}/a/{client_id}/ip_addresses".format(
        base=api_url, client_id=client_id
    )
    mocked_responses.add(
        responses.GET,
        ip_addresses_url,
        content_type="application/json",
        status=200,
        body=json.dumps(
            {
                "ip_addresses": [
                    "39.45.235.23",
                    "23.10.341.123",
                    "12.56.256.654",
                    "67.20.987.231",
                ],
                "updated_at": 1552072984,
            }
        ),
    )


@pytest.fixture
def mock_token_info(mocked_responses, api_url, account_id, client_id):
    token_info_url = "{base}/a/{client_id}/accounts/{id}/token-info".format(
        base=api_url, id=account_id, client_id=client_id
    )
    mocked_responses.add(
        responses.POST,
        token_info_url,
        content_type="application/json",
        status=200,
        body=json.dumps(
            {
                "created_at": 1563496685,
                "scopes": "calendar,email,contacts",
                "state": "valid",
                "updated_at": 1563496685,
            }
        ),
    )


@pytest.fixture
def mock_free_busy(mocked_responses, api_url):
    free_busy_url = "{base}/calendars/free-busy".format(base=api_url)

    def free_busy_callback(request):
        payload = json.loads(request.body)
        email = payload["emails"][0]
        resp_data = [
            {
                "object": "free_busy",
                "email": email,
                "time_slots": [
                    {
                        "object": "time_slot",
                        "status": "busy",
                        "start_time": 1409594400,
                        "end_time": 1409598000,
                    },
                    {
                        "object": "time_slot",
                        "status": "busy",
                        "start_time": 1409598000,
                        "end_time": 1409599000,
                    },
                ],
            }
        ]
        return 200, {}, json.dumps(resp_data)

    mocked_responses.add_callback(
        responses.POST,
        free_busy_url,
        content_type="application/json",
        callback=free_busy_callback,
    )


@pytest.fixture
def mock_availability(mocked_responses, api_url):
    availability_url = "{base}/calendars/availability".format(base=api_url)

    def availability_callback(request):
        payload = json.loads(request.body)
        resp_data = {
            "object": "availability",
            "time_slots": [
                {
                    "object": "time_slot",
                    "status": "free",
                    "start_time": 1409594400,
                    "end_time": 1409598000,
                },
                {
                    "object": "time_slot",
                    "status": "free",
                    "start_time": 1409598000,
                    "end_time": 1409599000,
                },
            ],
        }

        return 200, {}, json.dumps(resp_data)

    mocked_responses.add_callback(
        responses.POST,
        availability_url,
        content_type="application/json",
        callback=availability_callback,
    )

    mocked_responses.add_callback(
        responses.POST,
        "{url}/consecutive".format(url=availability_url),
        content_type="application/json",
        callback=availability_callback,
    )


@pytest.fixture
def mock_sentiment_analysis(mocked_responses, api_url, account_id):
    sentiment_url = "{base}/neural/sentiment".format(base=api_url)

    def sentiment_callback(request):
        payload = json.loads(request.body)
        if "message_id" in payload:
            response = [
                {
                    "account_id": account_id,
                    "processed_length": 11,
                    "sentiment": "NEUTRAL",
                    "sentiment_score": 0.30000001192092896,
                    "text": "hello world",
                }
            ]
        else:
            response = {
                "account_id": account_id,
                "processed_length": len(payload["text"]),
                "sentiment": "NEUTRAL",
                "sentiment_score": 0.30000001192092896,
                "text": payload["text"],
            }

        return 200, {}, json.dumps(response)

    mocked_responses.add_callback(
        responses.PUT,
        sentiment_url,
        content_type="application/json",
        callback=sentiment_callback,
    )


@pytest.fixture
def mock_extract_signature(mocked_responses, api_url, account_id):
    signature_url = "{base}/neural/signature".format(base=api_url)

    def signature_callback(request):
        payload = json.loads(request.body)
        response = {
            "account_id": account_id,
            "body": "This is the body<div>Nylas Swag</div><div>Software Engineer</div><div>123-456-8901</div><div>swag@nylas.com</div><img src='https://example.com/logo.png' alt='https://example.com/link.html'></a>",
            "signature": "Nylas Swag\n\nSoftware Engineer\n\n123-456-8901\n\nswag@nylas.com",
            "date": 1624029503,
            "from": [
                {
                    "email": "swag@nylas.com",
                    "name": "Nylas Swag",
                },
            ],
            "id": "abc123",
            "model_version": "0.0.1",
            "object": "message",
            "provider_name": "gmail",
            "subject": "Subject",
            "to": [
                {
                    "email": "me@nylas.com",
                    "name": "me",
                },
            ],
        }
        if "parse_contacts" not in payload or payload["parse_contacts"] is True:
            response["contacts"] = {
                "job_titles": ["Software Engineer"],
                "links": [
                    {
                        "description": "string",
                        "url": "https://example.com/link.html",
                    },
                ],
                "phone_numbers": ["123-456-8901"],
                "emails": ["swag@nylas.com"],
                "names": [
                    {
                        "first_name": "Nylas",
                        "last_name": "Swag",
                    },
                ],
            }

        return 200, {}, json.dumps([response])

    mocked_responses.add_callback(
        responses.PUT,
        signature_url,
        content_type="application/json",
        callback=signature_callback,
    )


@pytest.fixture
def mock_categorize(mocked_responses, api_url, account_id):
    categorize_url = "{base}/neural/categorize".format(base=api_url)

    def categorize_callback(request):
        response = {
            "account_id": account_id,
            "body": "This is a body",
            "categorizer": {
                "categorized_at": 1627076720,
                "category": "feed",
                "model_version": "6194f733",
                "subcategories": ["ooo"],
            },
            "date": 1624029503,
            "from": [
                {
                    "email": "swag@nylas.com",
                    "name": "Nylas Swag",
                },
            ],
            "id": "abc123",
            "object": "message",
            "provider_name": "gmail",
            "subject": "Subject",
            "to": [
                {
                    "email": "me@nylas.com",
                    "name": "me",
                },
            ],
        }

        return 200, {}, json.dumps([response])

    def recategorize_callback(request):
        response = {
            "account_id": account_id,
            "category": "conversation",
            "is_primary_label": "true",
            "message_id": "abc123",
            "recategorized_at": "2021-07-17T00:04:22.006193",
            "recategorized_from": {
                "category": "feed",
                "model_version": "6194f733",
                "subcategories": ["ooo"],
            },
            "subcategories": ["ooo"],
        }

        return 200, {}, json.dumps(response)

    mocked_responses.add_callback(
        responses.PUT,
        categorize_url,
        content_type="application/json",
        callback=categorize_callback,
    )

    mocked_responses.add_callback(
        responses.POST,
        "{}/feedback".format(categorize_url),
        content_type="application/json",
        callback=recategorize_callback,
    )


@pytest.fixture
def mock_ocr_request(mocked_responses, api_url, account_id):
    ocr_url = "{base}/neural/ocr".format(base=api_url)

    def ocr_callback(request):
        response = {
            "account_id": account_id,
            "content_type": "application/pdf",
            "filename": "sample.pdf",
            "id": "abc123",
            "object": "file",
            "ocr": ["This is page 1", "This is page 2"],
            "processed_pages": 2,
            "size": 20,
        }

        return 200, {}, json.dumps(response)

    mocked_responses.add_callback(
        responses.PUT,
        ocr_url,
        content_type="application/json",
        callback=ocr_callback,
    )


@pytest.fixture
def mock_clean_conversation(mocked_responses, api_url, account_id):
    conversation_url = "{base}/neural/conversation".format(base=api_url)
    file_url = "{base}/files/1781777f666586677621".format(base=api_url)

    def conversation_callback(request):
        response = {
            "account_id": account_id,
            "body": "<img src='cid:1781777f666586677621' /> This is the body",
            "conversation": "<img src='cid:1781777f666586677621' /> This is the conversation",
            "date": 1624029503,
            "from": [
                {
                    "email": "swag@nylas.com",
                    "name": "Nylas Swag",
                },
            ],
            "id": "abc123",
            "model_version": "0.0.1",
            "object": "message",
            "provider_name": "gmail",
            "subject": "Subject",
            "to": [
                {
                    "email": "me@nylas.com",
                    "name": "me",
                },
            ],
        }

        return 200, {}, json.dumps([response])

    def file_callback(request):
        response = {
            "id": "1781777f666586677621",
            "content_type": "image/png",
            "filename": "hello.png",
            "account_id": account_id,
            "object": "file",
            "size": 123,
        }

        return 200, {}, json.dumps(response)

    mocked_responses.add_callback(
        responses.PUT,
        conversation_url,
        content_type="application/json",
        callback=conversation_callback,
    )

    mocked_responses.add_callback(
        responses.GET,
        file_url,
        content_type="application/json",
        callback=file_callback,
    )


@pytest.fixture
def mock_deltas_since(mocked_responses, api_url):
    deltas = {
        "cursor_start": "start_cursor",
        "cursor_end": "end_cursor",
        "deltas": [
            {
                "attributes": {
                    "account_id": "aid-5678",
                    "given_name": "First",
                    "surname": "Last",
                    "id": "id-1234",
                    "object": "contact",
                },
                "cursor": "contact_cursor",
                "event": "create",
                "id": "delta-1",
                "object": "contact",
            },
            {
                "attributes": {
                    "account_id": "aid-5678",
                    "content_type": "text/plain",
                    "filename": "sample.txt",
                    "id": "id-1234",
                    "object": "file",
                    "size": 123,
                },
                "cursor": "file_cursor",
                "event": "create",
                "id": "delta-2",
                "object": "file",
            },
            {
                "attributes": {
                    "account_id": "aid-5678",
                    "to": [{"email": "foo", "name": "bar"}],
                    "subject": "foo",
                    "id": "id-1234",
                    "object": "message",
                },
                "cursor": "message_cursor",
                "event": "create",
                "id": "delta-3",
                "object": "message",
            },
            {
                "attributes": {
                    "account_id": "aid-5678",
                    "to": [{"email": "foo", "name": "bar"}],
                    "subject": "foo",
                    "id": "id-1234",
                    "object": "draft",
                },
                "cursor": "draft_cursor",
                "event": "create",
                "id": "delta-4",
                "object": "draft",
            },
            {
                "attributes": {
                    "account_id": "aid-5678",
                    "subject": "Subject",
                    "id": "id-1234",
                    "object": "thread",
                },
                "cursor": "thread_cursor",
                "event": "create",
                "id": "delta-5",
                "object": "thread",
            },
            {
                "attributes": {
                    "id": "id-1234",
                    "title": "test event",
                    "when": {"time": 1409594400, "object": "time"},
                    "participants": [
                        {
                            "name": "foo",
                            "email": "bar",
                            "status": "noreply",
                            "comment": "This is a comment",
                            "phone_number": "416-000-0000",
                        },
                    ],
                    "ical_uid": "id-5678",
                    "master_event_id": "master-1234",
                    "original_start_time": 1409592400,
                },
                "cursor": "event_cursor",
                "event": "create",
                "id": "delta-6",
                "object": "event",
            },
            {
                "attributes": {
                    "account_id": "aid-5678",
                    "id": "id-1234",
                    "object": "folder",
                    "name": "inbox",
                    "display_name": "name",
                },
                "cursor": "folder_cursor",
                "event": "create",
                "id": "delta-7",
                "object": "folder",
            },
            {
                "attributes": {
                    "account_id": "aid-5678",
                    "id": "id-1234",
                    "object": "label",
                    "name": "inbox",
                },
                "cursor": "label_cursor",
                "event": "create",
                "id": "delta-8",
                "object": "label",
            },
        ],
    }

    def callback(request):
        return 200, {}, json.dumps(deltas)

    mocked_responses.add_callback(
        responses.GET,
        "{base}/delta".format(base=api_url),
        callback=callback,
        content_type="application/json",
    )


@pytest.fixture
def mock_delta_cursor(mocked_responses, api_url):
    def callback(request):
        return 200, {}, json.dumps({"cursor": "cursor"})

    mocked_responses.add_callback(
        responses.POST,
        "{base}/delta/latest_cursor".format(base=api_url),
        callback=callback,
        content_type="application/json",
    )


@pytest.fixture
def mock_delta_stream(mocked_responses, api_url):
    delta = {
        "attributes": {
            "account_id": "aid-5678",
            "given_name": "First",
            "surname": "Last",
            "id": "id-1234",
            "object": "contact",
        },
        "cursor": "contact_cursor",
        "event": "create",
        "id": "delta-1",
        "object": "contact",
    }

    def stream_callback(request):
        return 200, {}, json.dumps(delta)

    def longpoll_callback(request):
        response = {
            "cursor_start": "start_cursor",
            "cursor_end": "end_cursor",
            "deltas": [delta],
        }
        return 200, {}, json.dumps(response)

    mocked_responses.add_callback(
        responses.GET,
        "{base}/delta/streaming".format(base=api_url),
        callback=stream_callback,
        content_type="application/json",
    )

    mocked_responses.add_callback(
        responses.GET,
        "{base}/delta/longpoll".format(base=api_url),
        callback=longpoll_callback,
        content_type="application/json",
    )

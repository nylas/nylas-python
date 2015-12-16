import json
import pytest
import responses
from conftest import API_URL
from nylas.client.errors import InvalidRequestError


@pytest.fixture
def mock_draft_saved_response():
    response_body = json.dumps(
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
            "to": [
                {
                    "email": "helena@nylas.com",
                    "name": "Helena Handbasket"
                }
            ],
            "unread": False,
            "version": 0
        })

    responses.add(responses.POST, API_URL + '/drafts/',
                  content_type='application/json', status=200,
                  body=response_body, match_querystring=True)


@pytest.fixture
def mock_draft_updated_response():
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

    responses.add(responses.PUT, API_URL + '/drafts/2h111aefv8pzwzfykrn7hercj',
                  content_type='application/json', status=200,
                  body=json.dumps(body), match_querystring=True)

    body['subject'] = 'Update #2'
    responses.add(responses.PUT, API_URL + '/drafts/2h111aefv8pzwzfykrn7hercj?random_query=true&param2=param',
                  content_type='application/json', status=200,
                  body=json.dumps(body), match_querystring=True)


@pytest.fixture
def mock_draft_sent_response():
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
            responses.POST, API_URL + '/send/',
            callback=callback,
            content_type='application/json')


@responses.activate
def test_save_send_draft(api_client, mock_draft_saved_response,
                         mock_draft_updated_response, mock_draft_sent_response):
    draft = api_client.drafts.create()
    draft.to = [{'name': 'My Friend', 'email': 'my.friend@example.com'}]
    draft.subject = "Here's an attachment"
    draft.body = "Cheers mate!"
    draft.save()

    draft.subject = "Stay polish, stay hungary"
    draft.save(random_query='true', param2='param')
    assert draft.subject == 'Update #2'

    msg = draft.send()
    assert msg['thread_id'] == 'clm33kapdxkposgltof845v9s'

    # Second time should throw an error
    raised = False
    try:
        draft.send()
    except InvalidRequestError:
        raised = True

    assert raised is True

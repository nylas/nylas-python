import re
import json
import pytest
import responses
from nylas import APIClient

# pylint: disable=redefined-outer-name

@pytest.fixture
def api_url():
    return 'http://localhost:2222'


@pytest.fixture
def api_client(api_url):
    return APIClient(None, None, None, api_url)


@pytest.fixture
def mock_account(api_url):
    response_body = json.dumps([
        {
            "account_id": "4dl0ni6vxomazo73r5ozdo16j",
            "email_address": "ben.bitdiddle1861@gmail.com",
            "id": "4dl0ni6vxomazo73r5ozdo16j",
            "name": "Ben Bitdiddle",
            "object": "account",
            "provider": "gmail"
        }
    ])
    responses.add(responses.GET, api_url + '/n?limit=1&offset=0',
                  content_type='application/json', status=200,
                  body=response_body, match_querystring=True)


@pytest.fixture
def mock_save_draft(api_url):
    save_endpoint = re.compile(api_url + '/drafts/')
    response_body = json.dumps({
        "id": "4dl0ni6vxomazo73r5oydo16k",
        "version": "4dw0ni6txomazo33r5ozdo16j"
    })
    responses.add(responses.POST, save_endpoint,
                  content_type='application/json', status=200,
                  body=response_body, match_querystring=True)

import re
import json
import pytest
import responses
from nylas import APIClient
from nylas.client.errors import *

API_URL = 'http://localhost:2222'


@pytest.fixture
def api_client():
    return APIClient(None, None, None, API_URL)


@pytest.fixture
def mock_account():
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
    responses.add(responses.GET, API_URL + '/n?limit=1&offset=0',
                  content_type='application/json', status=200,
                  body=response_body, match_querystring=True)


@pytest.fixture
def mock_save_draft():
    save_endpoint = re.compile(API_URL + '/drafts/')
    response_body = json.dumps({
        "id": "4dl0ni6vxomazo73r5oydo16k",
        "version": "4dw0ni6txomazo33r5ozdo16j"
    })
    responses.add(responses.POST, save_endpoint,
                  content_type='application/json', status=200,
                  body=response_body, match_querystring=True)



from unittest.mock import patch, Mock

import pytest
import requests

from nylas.handler.http_client import HttpClient

from nylas import Client


@pytest.fixture
def client():
    return Client(
        api_key="test-key",
    )


@pytest.fixture
def http_client():
    return HttpClient(
        api_server="https://test.nylas.com",
        api_key="test-key",
        timeout=30,
    )


@pytest.fixture
def patched_version_and_sys():
    with patch("sys.version_info", (1, 2, 3, "final", 5)), patch(
        "nylas.handler.http_client.__VERSION__", "2.0.0"
    ):
        yield


@pytest.fixture
def patched_session_request():
    mock_response = Mock()
    mock_response.content = b"mock data"
    mock_response.json.return_value = {"foo": "bar"}
    mock_response.status_code = 200

    with patch("requests.Session.request", return_value=mock_response) as mock_request:
        yield mock_request


@pytest.fixture
def mock_session_timeout():
    with patch("requests.Session.request", side_effect=requests.exceptions.Timeout):
        yield


@pytest.fixture
def http_client_list_response():
    mock_http_client = Mock()
    mock_http_client._execute.return_value = {
        "request_id": "abc-123",
        "data": [
            {
                "id": "calendar-123",
                "grant_id": "grant-123",
                "name": "Mock Calendar",
                "read_only": False,
                "is_owned_by_user": True,
                "object": "calendar",
            }
        ],
    }
    return mock_http_client


@pytest.fixture
def http_client_response():
    mock_http_client = Mock()
    mock_http_client._execute.return_value = {
        "request_id": "abc-123",
        "data": {
            "id": "calendar-123",
            "grant_id": "grant-123",
            "name": "Mock Calendar",
            "read_only": False,
            "is_owned_by_user": True,
            "object": "calendar",
        },
    }
    return mock_http_client


@pytest.fixture
def http_client_delete_response():
    mock_http_client = Mock()
    mock_http_client._execute.return_value = {
        "request_id": "abc-123",
    }
    return mock_http_client

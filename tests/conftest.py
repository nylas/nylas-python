from unittest.mock import patch, Mock

import pytest
import requests
from nylas.models.response import Response, ListResponse

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
    with patch(
        "nylas.models.response.ListResponse.from_dict",
        return_value=ListResponse([], "bar"),
    ):
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
        yield mock_http_client


@pytest.fixture
def http_client_response():
    with patch(
        "nylas.models.response.Response.from_dict", return_value=Response({}, "bar")
    ):
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
        yield mock_http_client


@pytest.fixture
def http_client_delete_response():
    mock_http_client = Mock()
    mock_http_client._execute.return_value = {
        "request_id": "abc-123",
    }
    return mock_http_client


@pytest.fixture
def http_client_token_exchange():
    mock_http_client = Mock()
    mock_http_client._execute.return_value = {
        "access_token": "nylas_access_token",
        "expires_in": 3600,
        "id_token": "jwt_token",
        "refresh_token": "nylas_refresh_token",
        "scope": "https://www.googleapis.com/auth/gmail.readonly profile",
        "token_type": "Bearer",
        "grant_id": "grant_123",
        "provider": "google",
    }
    return mock_http_client


@pytest.fixture
def http_client_token_info():
    mock_http_client = Mock()
    mock_http_client._execute.return_value = {
        "request_id": "abc-123",
        "data": {
            "iss": "https://nylas.com",
            "aud": "http://localhost:3030",
            "sub": "Jaf84d88-£274-46cc-bbc9-aed7dac061c7",
            "email": "user@example.com",
            "iat": 1692094848,
            "exp": 1692095173,
        },
    }
    return mock_http_client


@pytest.fixture
def http_client_free_busy():
    mock_http_client = Mock()
    mock_http_client._execute.return_value = {
        "request_id": "dd3ec9a2-8f15-403d-b269-32b1f1beb9f5",
        "data": [
            {
                "email": "user1@example.com",
                "time_slots": [
                    {
                        "start_time": 1690898400,
                        "end_time": 1690902000,
                        "status": "busy",
                        "object": "time_slot",
                    },
                    {
                        "start_time": 1691064000,
                        "end_time": 1691067600,
                        "status": "busy",
                        "object": "time_slot",
                    },
                ],
                "object": "free_busy",
            },
            {
                "email": "user2@example.com",
                "error": "Unable to resolve e-mail address user2@example.com to an Active Directory object.",
                "object": "error",
            },
        ],
    }
    return mock_http_client


@pytest.fixture
def http_client_list_scheduled_messages():
    mock_http_client = Mock()
    mock_http_client._execute.return_value = {
        "request_id": "dd3ec9a2-8f15-403d-b269-32b1f1beb9f5",
        "data": [
            {
                "schedule_id": "8cd56334-6d95-432c-86d1-c5dab0ce98be",
                "status": {
                    "code": "pending",
                    "description": "schedule send awaiting send at time",
                },
            },
            {
                "schedule_id": "rb856334-6d95-432c-86d1-c5dab0ce98be",
                "status": {"code": "sucess", "description": "schedule send succeeded"},
                "close_time": 1690579819,
            },
        ],
    }
    return mock_http_client


@pytest.fixture
def http_client_clean_messages():
    mock_http_client = Mock()
    mock_http_client._execute.return_value = {
        "request_id": "dd3ec9a2-8f15-403d-b269-32b1f1beb9f5",
        "data": [
            {
                "body": "Hello, I just sent a message using Nylas!",
                "from": [
                    {"name": "Daenerys Targaryen", "email": "daenerys.t@example.com"}
                ],
                "grant_id": "41009df5-bf11-4c97-aa18-b285b5f2e386",
                "id": "message-1",
                "object": "message",
                "conversation": "cleaned example",
            },
            {
                "body": "Hello, this is a test message!",
                "from": [{"name": "Michael Scott", "email": "m.scott@email.com"}],
                "grant_id": "41009df5-bf11-4c97-aa18-b285b5f2e386",
                "id": "message-2",
                "object": "message",
                "conversation": "another example",
            },
        ],
    }
    return mock_http_client

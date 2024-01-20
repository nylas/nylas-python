from unittest import mock
from unittest.mock import patch, Mock

import pytest
import requests
from nylas.models.errors import NylasApiError, NylasOAuthError

from nylas.handler.http_client import (
    HttpClient,
    _build_query_params,
    _validate_response,
)


class TestData:
    def __init__(self, content_type=None):
        self.content_type = content_type


class TestHttpClient:
    @pytest.fixture
    def http_client(self):
        return HttpClient(
            api_server="https://test.nylas.com",
            api_key="test-key",
            timeout=30,
        )

    @pytest.fixture
    def patched_version_and_sys(self):
        with patch("sys.version_info", (1, 2, 3, "final", 5)), patch(
            "nylas.handler.http_client.__VERSION__", "2.0.0"
        ):
            yield

    @pytest.fixture
    def patched_session_request(self):
        mock_response = Mock()
        mock_response.content = b"mock data"

        with patch("requests.Session.request", return_value=mock_response):
            yield mock

    @pytest.fixture
    def mock_session_timeout(self):
        with patch("requests.Session.request", side_effect=requests.exceptions.Timeout):
            yield

    def test_http_client_init(self):
        http_client = HttpClient(
            api_server="https://test.nylas.com",
            api_key="test-key",
            timeout=60,
        )

        assert http_client.api_server == "https://test.nylas.com"
        assert http_client.api_key == "test-key"
        assert http_client.timeout == 60

    def test_build_headers_default(self, http_client, patched_version_and_sys):
        headers = http_client._build_headers()

        assert headers == {
            "X-Nylas-API-Wrapper": "python",
            "User-Agent": "Nylas Python SDK 2.0.0 - 1.2.3",
            "Authorization": "Bearer test-key",
        }

    def test_build_headers_extra_headers(self, http_client, patched_version_and_sys):
        headers = http_client._build_headers(
            extra_headers={
                "foo": "bar",
                "X-Test": "test",
            }
        )

        assert headers == {
            "X-Nylas-API-Wrapper": "python",
            "User-Agent": "Nylas Python SDK 2.0.0 - 1.2.3",
            "Authorization": "Bearer test-key",
            "foo": "bar",
            "X-Test": "test",
        }

    def test_build_headers_json_body(self, http_client, patched_version_and_sys):
        headers = http_client._build_headers(
            response_body={
                "foo": "bar",
            }
        )

        assert headers == {
            "X-Nylas-API-Wrapper": "python",
            "User-Agent": "Nylas Python SDK 2.0.0 - 1.2.3",
            "Authorization": "Bearer test-key",
            "Content-type": "application/json",
        }

    def test_build_headers_form_body(self, http_client, patched_version_and_sys):
        headers = http_client._build_headers(
            response_body={
                "foo": "bar",
            },
            data=TestData(content_type="application/x-www-form-urlencoded"),
        )

        assert headers == {
            "X-Nylas-API-Wrapper": "python",
            "User-Agent": "Nylas Python SDK 2.0.0 - 1.2.3",
            "Authorization": "Bearer test-key",
            "Content-type": "application/x-www-form-urlencoded",
        }

    def test_build_request_default(self, http_client, patched_version_and_sys):
        request = http_client._build_request(
            method="GET",
            path="/foo",
        )

        assert request == {
            "method": "GET",
            "url": "https://test.nylas.com/foo",
            "headers": {
                "X-Nylas-API-Wrapper": "python",
                "User-Agent": "Nylas Python SDK 2.0.0 - 1.2.3",
                "Authorization": "Bearer test-key",
            },
        }

    def test_build_query_params(self, patched_version_and_sys):
        url = _build_query_params(
            base_url="https://test.nylas.com/foo",
            query_params={
                "foo": "bar",
                "list": ["a", "b", "c"],
                "map": {"key1": "value1", "key2": "value2"},
            },
        )

        assert (
            url
            == "https://test.nylas.com/foo?foo=bar&list=a&list=b&list=c&map=key1:value1&map=key2:value2"
        )

    def test_execute_download_request(self, http_client, patched_session_request):
        response = http_client._execute_download_request(
            path="/foo",
        )
        assert response == b"mock data"

    def test_execute_download_request_with_stream(
        self, http_client, patched_session_request
    ):
        response = http_client._execute_download_request(
            path="/foo",
            stream=True,
        )
        assert isinstance(response, Mock) is True
        assert response.content == b"mock data"

    def test_execute_download_request_timeout(self, http_client, mock_session_timeout):
        with pytest.raises(Exception) as e:
            http_client._execute_download_request(
                path="/foo",
            )
        assert (
            str(e.value)
            == "Nylas SDK timed out before receiving a response from the server."
        )

    def test_validate_response(self):
        response = Mock()
        response.status_code = 200
        response.json.return_value = {"foo": "bar"}
        response.url = "https://test.nylas.com/foo"

        validation = _validate_response(response)
        assert validation == {"foo": "bar"}

    def test_validate_response_400_error(self):
        response = Mock()
        response.status_code = 400
        response.json.return_value = {
            "request_id": "123",
            "error": {
                "type": "api_error",
                "message": "The request is invalid.",
                "provider_error": {"foo": "bar"},
            },
        }
        response.url = "https://test.nylas.com/foo"

        with pytest.raises(Exception) as e:
            _validate_response(response)
        assert e.type == NylasApiError
        assert str(e.value) == "The request is invalid."
        assert e.value.type == "api_error"
        assert e.value.request_id == "123"
        assert e.value.status_code == 400
        assert e.value.provider_error == {"foo": "bar"}

    def test_validate_response_auth_error(self):
        response = Mock()
        response.status_code = 401
        response.json.return_value = {
            "error": "invalid_request",
            "error_description": "The request is invalid.",
            "error_uri": "https://docs.nylas.com/reference#authentication-errors",
            "error_code": 100241,
        }
        response.url = "https://test.nylas.com/connect/token"

        with pytest.raises(Exception) as e:
            _validate_response(response)
        assert e.type == NylasOAuthError
        assert str(e.value) == "The request is invalid."
        assert e.value.error == "invalid_request"
        assert e.value.error_code == 100241
        assert e.value.error_description == "The request is invalid."

    def test_validate_response_400_keyerror(self):
        response = Mock()
        response.status_code = 400
        response.json.return_value = {
            "request_id": "123",
            "foo": "bar",
        }
        response.url = "https://test.nylas.com/foo"

        with pytest.raises(Exception) as e:
            _validate_response(response)
        assert e.type == NylasApiError
        assert str(e.value) == "{'request_id': '123', 'foo': 'bar'}"
        assert e.value.type == "unknown"
        assert e.value.request_id == "123"
        assert e.value.status_code == 400

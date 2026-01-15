from unittest.mock import Mock

import pytest

from nylas.handler.http_client import (
    HttpClient,
    _build_query_params,
    _validate_response,
)
from nylas.models.errors import NylasApiError, NylasOAuthError


class TestData:
    def __init__(self, content_type=None):
        self.content_type = content_type


class TestHttpClient:
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
            "Content-type": "application/json; charset=utf-8",
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

    def test_build_headers_override_headers(self, http_client, patched_version_and_sys):
        headers = http_client._build_headers(
            overrides={
                "headers": {
                    "foo": "bar",
                    "X-Test": "test",
                }
            }
        )

        assert headers == {
            "X-Nylas-API-Wrapper": "python",
            "User-Agent": "Nylas Python SDK 2.0.0 - 1.2.3",
            "Authorization": "Bearer test-key",
            "foo": "bar",
            "X-Test": "test",
        }

    def test_build_headers_override_api_key(self, http_client, patched_version_and_sys):
        headers = http_client._build_headers(
            overrides={
                "api_key": "test-key-override",
            }
        )

        assert headers == {
            "X-Nylas-API-Wrapper": "python",
            "User-Agent": "Nylas Python SDK 2.0.0 - 1.2.3",
            "Authorization": "Bearer test-key-override",
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

    def test_build_request_override_api_uri(self, http_client, patched_version_and_sys):
        request = http_client._build_request(
            method="GET",
            path="/foo",
            overrides={
                "api_uri": "https://override.nylas.com",
            },
        )

        assert request == {
            "method": "GET",
            "url": "https://override.nylas.com/foo",
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

    def test_execute_download_request(self, http_client, patched_request):
        response = http_client._execute_download_request(
            path="/foo",
        )
        assert response == b"mock data"

    def test_execute_download_request_with_stream(self, http_client, patched_request):
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

    def test_execute_download_request_override_timeout(
        self, http_client, patched_version_and_sys, patched_request
    ):
        response = http_client._execute_download_request(
            path="/foo",
            overrides={"timeout": 60},
        )
        patched_request.assert_called_once_with(
            "GET",
            "https://test.nylas.com/foo",
            headers={
                "X-Nylas-API-Wrapper": "python",
                "User-Agent": "Nylas Python SDK 2.0.0 - 1.2.3",
                "Authorization": "Bearer test-key",
                "Content-type": "application/json; charset=utf-8",
            },
            timeout=60,
            stream=False,
        )

    def test_validate_response(self):
        response = Mock()
        response.status_code = 200
        response.json.return_value = {"foo": "bar"}
        response.url = "https://test.nylas.com/foo"
        response.headers = {"X-Test-Header": "test"}

        response_json, response_headers = _validate_response(response)
        assert response_json == {"foo": "bar"}
        assert response_headers == {"X-Test-Header": "test"}

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

    def test_execute(self, http_client, patched_version_and_sys, patched_request):
        mock_response = Mock()
        mock_response.json.return_value = {"foo": "bar"}
        mock_response.headers = {"X-Test-Header": "test"}
        mock_response.status_code = 200
        patched_request.return_value = mock_response

        response_json, response_headers = http_client._execute(
            method="GET",
            path="/foo",
            headers={"test": "header"},
            query_params={"query": "param"},
            request_body={"foo": "bar"},
        )

        assert response_json == {"foo": "bar"}
        assert response_headers == {"X-Test-Header": "test"}
        patched_request.assert_called_once_with(
            "GET",
            "https://test.nylas.com/foo?query=param",
            headers={
                "X-Nylas-API-Wrapper": "python",
                "User-Agent": "Nylas Python SDK 2.0.0 - 1.2.3",
                "Authorization": "Bearer test-key",
                "Content-type": "application/json; charset=utf-8",
                "test": "header",
            },
            data=b'{"foo": "bar"}',
            timeout=30,
        )

    def test_execute_override_timeout(
        self, http_client, patched_version_and_sys, patched_request
    ):
        mock_response = Mock()
        mock_response.json.return_value = {"foo": "bar"}
        mock_response.headers = {"X-Test-Header": "test"}
        mock_response.status_code = 200
        patched_request.return_value = mock_response

        response_json, response_headers = http_client._execute(
            method="GET",
            path="/foo",
            headers={"test": "header"},
            query_params={"query": "param"},
            request_body={"foo": "bar"},
            overrides={"timeout": 60},
        )

        assert response_json == {"foo": "bar"}
        assert response_headers == {"X-Test-Header": "test"}
        patched_request.assert_called_once_with(
            "GET",
            "https://test.nylas.com/foo?query=param",
            headers={
                "X-Nylas-API-Wrapper": "python",
                "User-Agent": "Nylas Python SDK 2.0.0 - 1.2.3",
                "Authorization": "Bearer test-key",
                "Content-type": "application/json; charset=utf-8",
                "test": "header",
            },
            data=b'{"foo": "bar"}',
            timeout=60,
        )

    def test_execute_timeout(self, http_client, mock_session_timeout):
        with pytest.raises(Exception) as e:
            http_client._execute(
                method="GET",
                path="/foo",
                headers={"test": "header"},
                query_params={"query": "param"},
                request_body={"foo": "bar"},
            )
        assert (
            str(e.value)
            == "Nylas SDK timed out before receiving a response from the server."
        )

    def test_validate_response_with_headers(self):
        response = Mock()
        response.status_code = 200
        response.json.return_value = {"foo": "bar"}
        response.url = "https://test.nylas.com/foo"
        response.headers = {"X-Test-Header": "test"}

        json_response, headers = _validate_response(response)
        assert json_response == {"foo": "bar"}
        assert headers == {"X-Test-Header": "test"}

    def test_validate_response_400_error_with_headers(self):
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
        response.headers = {"X-Test-Header": "test"}

        with pytest.raises(NylasApiError) as e:
            _validate_response(response)
        assert e.value.headers == {"X-Test-Header": "test"}

    def test_validate_response_auth_error_with_headers(self):
        response = Mock()
        response.status_code = 401
        response.json.return_value = {
            "error": "invalid_request",
            "error_description": "The request is invalid.",
            "error_uri": "https://docs.nylas.com/reference#authentication-errors",
            "error_code": 100241,
        }
        response.url = "https://test.nylas.com/connect/token"
        response.headers = {"X-Test-Header": "test"}

        with pytest.raises(NylasOAuthError) as e:
            _validate_response(response)
        assert e.value.headers == {"X-Test-Header": "test"}

    def test_execute_with_headers(self, http_client, patched_version_and_sys, patched_request):
        mock_response = Mock()
        mock_response.json.return_value = {"foo": "bar"}
        mock_response.headers = {"X-Test-Header": "test"}
        mock_response.status_code = 200
        patched_request.return_value = mock_response

        response_json, response_headers = http_client._execute(
            method="GET",
            path="/foo",
            headers={"test": "header"},
            query_params={"query": "param"},
            request_body={"foo": "bar"},
        )

        assert response_json == {"foo": "bar"}
        assert response_headers == {"X-Test-Header": "test"}
        patched_request.assert_called_once_with(
            "GET",
            "https://test.nylas.com/foo?query=param",
            headers={
                "X-Nylas-API-Wrapper": "python",
                "User-Agent": "Nylas Python SDK 2.0.0 - 1.2.3",
                "Authorization": "Bearer test-key",
                "Content-type": "application/json; charset=utf-8",
                "test": "header",
            },
            data=b'{"foo": "bar"}',
            timeout=30,
        )

    def test_execute_with_utf8_characters(self, http_client, patched_version_and_sys, patched_request):
        """Test that UTF-8 characters are safely encoded in JSON requests."""
        mock_response = Mock()
        mock_response.json.return_value = {"success": True}
        mock_response.headers = {"X-Test-Header": "test"}
        mock_response.status_code = 200
        patched_request.return_value = mock_response

        # Request with special characters
        request_body = {
            "title": "Réunion d'équipe",
            "description": "De l'idée à la post-prod, sans friction",
            "location": "café",
        }

        response_json, response_headers = http_client._execute(
            method="POST",
            path="/events",
            request_body=request_body,
        )

        assert response_json == {"success": True}
        # Verify that the data is sent as UTF-8 encoded bytes
        call_kwargs = patched_request.call_args[1]
        assert "data" in call_kwargs
        sent_data = call_kwargs["data"]
        
        # Data should be bytes
        assert isinstance(sent_data, bytes)
        
        # The JSON should contain actual UTF-8 characters (not escaped)
        decoded = sent_data.decode('utf-8')
        assert "Réunion d'équipe" in decoded
        assert "De l'idée à la post-prod" in decoded
        assert "café" in decoded
        # Should NOT contain unicode escape sequences
        assert "\\u" not in decoded

    def test_execute_with_none_request_body(self, http_client, patched_version_and_sys, patched_request):
        """Test that None request_body is handled correctly."""
        mock_response = Mock()
        mock_response.json.return_value = {"success": True}
        mock_response.headers = {"X-Test-Header": "test"}
        mock_response.status_code = 200
        patched_request.return_value = mock_response

        response_json, response_headers = http_client._execute(
            method="GET",
            path="/events",
            request_body=None,
        )

        assert response_json == {"success": True}
        # Verify that data is None when request_body is None
        call_kwargs = patched_request.call_args[1]
        assert "data" in call_kwargs
        assert call_kwargs["data"] is None

    def test_execute_with_emoji_and_international_characters(self, http_client, patched_version_and_sys, patched_request):
        """Test that emoji and various international characters are safely encoded."""
        mock_response = Mock()
        mock_response.json.return_value = {"success": True}
        mock_response.headers = {"X-Test-Header": "test"}
        mock_response.status_code = 200
        patched_request.return_value = mock_response

        request_body = {
            "emoji": "🎉 Party time! 🥳",
            "japanese": "こんにちは",
            "chinese": "你好",
            "russian": "Привет",
            "german": "Größe",
            "spanish": "¿Cómo estás?",
        }

        response_json, response_headers = http_client._execute(
            method="POST",
            path="/messages",
            request_body=request_body,
        )

        assert response_json == {"success": True}
        call_kwargs = patched_request.call_args[1]
        sent_data = call_kwargs["data"]
        
        # Data should be bytes
        assert isinstance(sent_data, bytes)
        
        # All characters should be preserved (not escaped)
        decoded = sent_data.decode('utf-8')
        assert "🎉 Party time! 🥳" in decoded
        assert "こんにちは" in decoded
        assert "你好" in decoded
        assert "Привет" in decoded
        assert "Größe" in decoded
        assert "¿Cómo estás?" in decoded
        # Should NOT contain unicode escape sequences
        assert "\\u" not in decoded

    def test_execute_with_right_single_quotation_mark(self, http_client, patched_version_and_sys, patched_request):
        """Test that right single quotation mark (\\u2019) is handled correctly.
        
        This character caused UnicodeEncodeError: 'latin-1' codec can't encode character '\\u2019'.
        """
        mock_response = Mock()
        mock_response.json.return_value = {"success": True}
        mock_response.headers = {"X-Test-Header": "test"}
        mock_response.status_code = 200
        patched_request.return_value = mock_response

        # The \u2019 character is the right single quotation mark (')
        # This was the exact character that caused the original encoding error
        request_body = {
            "subject": "It's a test",  # Contains \u2019 (right single quotation mark)
            "body": "Here's another example with curly apostrophe",
        }

        response_json, response_headers = http_client._execute(
            method="POST",
            path="/messages/send",
            request_body=request_body,
        )

        assert response_json == {"success": True}
        call_kwargs = patched_request.call_args[1]
        sent_data = call_kwargs["data"]
        
        # Data should be bytes
        assert isinstance(sent_data, bytes)
        
        # The character should be preserved (not escaped)
        decoded = sent_data.decode('utf-8')
        assert "'" in decoded  # \u2019 right single quotation mark
        assert "It's a test" in decoded
        assert "Here's another" in decoded
        # Should NOT contain unicode escape sequences
        assert "\\u2019" not in decoded

    def test_execute_with_multipart_data_not_affected(self, http_client, patched_version_and_sys, patched_request):
        """Test that multipart/form-data is not affected by the change."""
        mock_response = Mock()
        mock_response.json.return_value = {"success": True}
        mock_response.headers = {"X-Test-Header": "test"}
        mock_response.status_code = 200
        patched_request.return_value = mock_response

        # When data is provided (multipart), request_body should be ignored
        mock_data = Mock()
        mock_data.content_type = "multipart/form-data"

        response_json, response_headers = http_client._execute(
            method="POST",
            path="/messages/send",
            request_body={"foo": "bar"},  # This should be ignored
            data=mock_data,
        )

        assert response_json == {"success": True}
        call_kwargs = patched_request.call_args[1]
        # Should use the multipart data, not JSON
        assert call_kwargs["data"] == mock_data

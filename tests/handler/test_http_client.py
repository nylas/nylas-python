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
                "Content-type": "application/json",
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
                "Content-type": "application/json",
                "test": "header",
            },
            json={"foo": "bar"},
            timeout=30,
            data=None,
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
                "Content-type": "application/json",
                "test": "header",
            },
            json={"foo": "bar"},
            timeout=60,
            data=None,
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
                "Content-type": "application/json",
                "test": "header",
            },
            json={"foo": "bar"},
            timeout=30,
            data=None,
        )

    def test_validate_response_500_error_html(self):
        response = Mock()
        response.status_code = 500
        response.json.side_effect = ValueError("No JSON object could be decoded")
        response.text = "<html><body><h1>Internal Server Error</h1></body></html>"
        response.headers = {"Content-Type": "text/html", "x-fastly-id": "fastly-123"}

        with pytest.raises(NylasApiError) as e:
            _validate_response(response)
        assert e.value.type == "network_error"
        assert str(e.value) == """
                        HTTP 500: Non-JSON response received (flow_id: fastly-123).
                        Body: <html><body><h1>Internal Server Error</h1></body></html>"""
        assert e.value.status_code == 500

    def test_validate_response_502_error_plain_text(self):
        response = Mock()
        response.status_code = 502
        response.json.side_effect = ValueError("No JSON object could be decoded")
        response.text = "Bad Gateway"
        response.headers = {"Content-Type": "text/plain"}

        with pytest.raises(NylasApiError) as e:
            _validate_response(response)
        assert e.value.type == "network_error"
        assert str(e.value) == """
                        HTTP 502: Non-JSON response received.
                        Body: Bad Gateway"""
        assert e.value.status_code == 502

    def test_validate_response_200_success_non_json(self):
        response = Mock()
        response.status_code = 200
        response.json.side_effect = ValueError("No JSON object could be decoded")
        response.headers = {"Content-Type": "text/plain"}

        response_json, response_headers = _validate_response(response)
        assert response_json == {}
        assert response_headers == {"Content-Type": "text/plain"}

    def test_validate_response_error_empty_response(self):
        response = Mock()
        response.status_code = 500
        response.json.side_effect = ValueError("No JSON object could be decoded")
        response.text = ""
        response.headers = {"Content-Type": "text/html"}

        with pytest.raises(NylasApiError) as e:
            _validate_response(response)
        assert e.value.type == "network_error"
        assert str(e.value) == """
                        HTTP 500: Non-JSON response received.
                        Body: """
        assert e.value.status_code == 500

    def test_validate_response_error_long_response_not_truncated(self):
        response = Mock()
        response.status_code = 500
        response.json.side_effect = ValueError("No JSON object could be decoded")
        response.text = "A" * 600
        response.headers = {"Content-Type": "text/html"}

        with pytest.raises(NylasApiError) as e:
            _validate_response(response)
        assert e.value.type == "network_error"
        expected_body = "A" * 200 + "..."
        assert str(e.value) == f"""
                        HTTP 500: Non-JSON response received.
                        Body: {expected_body}"""
        assert e.value.status_code == 500

    def test_validate_response_with_flow_id_header(self):
        response = Mock()
        response.status_code = 503
        response.json.side_effect = ValueError("No JSON object could be decoded")
        response.text = "Service Unavailable"
        response.headers = {"x-fastly-id": "ABC123DEF456"}

        with pytest.raises(NylasApiError) as e:
            _validate_response(response)
        assert e.value.type == "network_error"
        assert str(e.value) == """
                        HTTP 503: Non-JSON response received (flow_id: ABC123DEF456).
                        Body: Service Unavailable"""
        assert e.value.status_code == 503

    def test_validate_response_without_flow_id_header(self):
        response = Mock()
        response.status_code = 504
        response.json.side_effect = ValueError("No JSON object could be decoded")
        response.text = "Gateway Timeout"
        response.headers = {"Content-Type": "text/plain"}

        with pytest.raises(NylasApiError) as e:
            _validate_response(response)
        assert e.value.type == "network_error"
        assert str(e.value) == """
                        HTTP 504: Non-JSON response received.
                        Body: Gateway Timeout"""
        assert e.value.status_code == 504

    def test_validate_response_different_content_types(self):
        content_types = [
            ("text/html", "<h1>Error</h1>"),
            ("text/plain", "Plain text error"),
            ("application/xml", "<?xml version='1.0'?><error/>"),
            ("text/css", "body { color: red; }"),
        ]
        
        for content_type, body in content_types:
            response = Mock()
            response.status_code = 500
            response.json.side_effect = ValueError("No JSON object could be decoded")
            response.text = body
            response.headers = {"Content-Type": content_type}

            with pytest.raises(NylasApiError) as e:
                _validate_response(response)
            assert e.value.type == "network_error"
            assert str(e.value) == f"""
                        HTTP 500: Non-JSON response received.
                        Body: {body}"""
            assert e.value.status_code == 500

from unittest.mock import patch

import pytest
from nylas.handler.http_client import HttpClient, _build_query_params


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

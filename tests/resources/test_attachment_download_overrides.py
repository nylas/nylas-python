from unittest.mock import Mock

import pytest
import requests

from nylas import Client
from nylas.models.errors import NylasSdkTimeoutError


@pytest.mark.parametrize("method", ["download", "download_bytes"])
@pytest.mark.parametrize(
    "overrides",
    [
        None,
        {"api_uri": "https://override.example.test"},
        {"headers": {"X-Test": "custom"}},
        {"api_key": "override-key"},
        {"skip_auth": True},
        {"timeout": 60},
    ],
)
def test_attachment_download_honors_overrides(method, overrides, monkeypatch):
    client = Client(api_key="test-key", api_uri="https://api.example.test", timeout=30)
    response = requests.Response()
    response.status_code = 200
    response._content = b"attachment data"
    request = Mock(return_value=response)
    monkeypatch.setattr(requests, "request", request)

    result = getattr(client.attachments, method)(
        "grant-test",
        "attachment-test",
        {"message_id": "message-test"},
        overrides=overrides,
    )

    options = overrides or {}
    call = request.call_args
    assert call.args[0] == "GET"
    assert call.args[1] == (
        options.get("api_uri", "https://api.example.test")
        + "/v3/grants/grant-test/attachments/attachment-test/download?message_id=message-test"
    )
    headers = call.kwargs["headers"]
    if options.get("skip_auth"):
        assert "Authorization" not in headers
    else:
        assert headers["Authorization"] == "Bearer " + options.get(
            "api_key", "test-key"
        )
    if "headers" in options:
        assert headers["X-Test"] == "custom"
    assert "Content-type" not in headers
    assert call.kwargs["timeout"] == options.get("timeout", 30)
    assert call.kwargs["stream"] is (method == "download")
    if method == "download":
        assert result is response
    else:
        assert result == b"attachment data"


@pytest.mark.parametrize("method", ["download", "download_bytes"])
def test_download_timeout_preserves_override_url(method, monkeypatch):
    client = Client(api_key="test-key", api_uri="https://api.example.test")
    monkeypatch.setattr(
        requests, "request", Mock(side_effect=requests.exceptions.Timeout)
    )
    with pytest.raises(NylasSdkTimeoutError) as error:
        getattr(client.attachments, method)(
            "grant-test",
            "attachment-test",
            {"message_id": "message-test"},
            overrides={"api_uri": "https://override.example.test", "timeout": 60},
        )
    assert error.value.url.startswith("https://override.example.test/")
    assert error.value.timeout == 60

from unittest import mock
from unittest.mock import Mock, patch

from nylas.models.auth import (
    CodeExchangeResponse,
    TokenInfoResponse,
    ProviderDetectResponse,
)
from nylas.models.grants import Grant

from nylas.resources.auth import (
    _hash_pkce_secret,
    _build_query,
    _build_query_with_pkce,
    _build_query_with_admin_consent,
    Auth,
)


class TestAuth:
    def test_hash_pkce_secret(self):
        assert (
            _hash_pkce_secret("nylas")
            == "ZTk2YmY2Njg2YTNjMzUxMGU5ZTkyN2RiNzA2OWNiMWNiYTliOTliMDIyZjQ5NDgzYTZjZTMyNzA4MDllNjhhMg"
        )

    def test_build_query(self):
        config = {
            "foo": "bar",
            "scope": ["email", "calendar"],
        }

        assert _build_query(config) == {
            "foo": "bar",
            "response_type": "code",
            "access_type": "online",
            "scope": "email calendar",
        }

    def test_build_query_with_pkce(self):
        config = {
            "foo": "bar",
            "scope": ["email", "calendar"],
        }

        assert _build_query_with_pkce(config, "secret-hash-123") == {
            "foo": "bar",
            "response_type": "code",
            "access_type": "online",
            "scope": "email calendar",
            "code_challenge": "secret-hash-123",
            "code_challenge_method": "s256",
        }

    def test_build_query_with_admin_consent(self):
        config = {
            "foo": "bar",
            "scope": ["email", "calendar"],
            "credential_id": "credential-id-123",
        }

        assert _build_query_with_admin_consent(config) == {
            "foo": "bar",
            "response_type": "adminconsent",
            "access_type": "online",
            "scope": "email calendar",
            "credential_id": "credential-id-123",
        }

    def test_url_auth_builder(self, http_client):
        auth = Auth(http_client)

        assert (
            auth._url_auth_builder({"foo": "bar"})
            == "https://test.nylas.com/v3/connect/auth?foo=bar"
        )

    def test_get_token(self, http_client_token_exchange):
        auth = Auth(http_client_token_exchange)
        req = {
            "redirect_uri": "https://example.com",
            "code": "code",
            "client_id": "client_id",
            "client_secret": "client_secret",
        }

        res = auth._get_token(req)

        http_client_token_exchange._execute.assert_called_once_with(
            method="POST",
            path="/v3/connect/token",
            request_body=req,
        )
        assert type(res) is CodeExchangeResponse
        assert res.access_token == "nylas_access_token"
        assert res.expires_in == 3600
        assert res.id_token == "jwt_token"
        assert res.refresh_token == "nylas_refresh_token"
        assert res.scope == "https://www.googleapis.com/auth/gmail.readonly profile"
        assert res.token_type == "Bearer"
        assert res.grant_id == "grant_123"

    def test_get_token_info(self, http_client_token_info):
        auth = Auth(http_client_token_info)
        req = {
            "foo": "bar",
        }

        res = auth._get_token_info(req)

        http_client_token_info._execute.assert_called_once_with(
            method="GET",
            path="/v3/connect/tokeninfo",
            query_params=req,
        )
        assert type(res) is TokenInfoResponse
        assert res.iss == "https://nylas.com"
        assert res.aud == "http://localhost:3030"
        assert res.sub == "Jaf84d88-£274-46cc-bbc9-aed7dac061c7"
        assert res.email == "user@example.com"
        assert res.iat == 1692094848
        assert res.exp == 1692095173

    def test_url_for_oauth2(self, http_client):
        auth = Auth(http_client)
        config = {
            "client_id": "abc-123",
            "redirect_uri": "https://example.com/oauth/callback",
            "scope": ["email.read_only", "calendar", "contacts"],
            "login_hint": "test@gmail.com",
            "provider": "google",
            "prompt": "select_provider,detect",
            "state": "abc-123-state",
        }

        url = auth.url_for_oauth2(config)

        assert (
            url
            == "https://test.nylas.com/v3/connect/auth?client_id=abc-123&redirect_uri=https%3A//example.com/oauth/callback&scope=email.read_only%20calendar%20contacts&login_hint=test%40gmail.com&provider=google&prompt=select_provider%2Cdetect&state=abc-123-state&response_type=code&access_type=online"
        )

    def test_exchange_code_for_token(self, http_client_token_exchange):
        auth = Auth(http_client_token_exchange)
        config = {
            "client_id": "abc-123",
            "client_secret": "secret",
            "code": "code",
            "redirect_uri": "https://example.com/oauth/callback",
        }

        auth.exchange_code_for_token(config)

        http_client_token_exchange._execute.assert_called_once_with(
            method="POST",
            path="/v3/connect/token",
            request_body={
                "client_id": "abc-123",
                "client_secret": "secret",
                "code": "code",
                "redirect_uri": "https://example.com/oauth/callback",
                "grant_type": "authorization_code",
            },
        )

    def test_exchange_code_for_token_no_secret(self, http_client_token_exchange):
        http_client_token_exchange.api_key = "nylas-api-key"
        auth = Auth(http_client_token_exchange)
        config = {
            "client_id": "abc-123",
            "code": "code",
            "redirect_uri": "https://example.com/oauth/callback",
        }

        auth.exchange_code_for_token(config)

        http_client_token_exchange._execute.assert_called_once_with(
            method="POST",
            path="/v3/connect/token",
            request_body={
                "client_id": "abc-123",
                "code": "code",
                "redirect_uri": "https://example.com/oauth/callback",
                "client_secret": "nylas-api-key",
                "grant_type": "authorization_code",
            },
        )

    def test_custom_authentication(self):
        mock_http_client = Mock()
        mock_http_client._execute.return_value = {
            "request_id": "abc-123",
            "data": {
                "id": "e19f8e1a-eb1c-41c0-b6a6-d2e59daf7f47",
                "provider": "google",
                "grant_status": "valid",
                "email": "email@example.com",
                "scope": ["Mail.Read", "User.Read", "offline_access"],
                "user_agent": "string",
                "ip": "string",
                "state": "my-state",
                "created_at": 1617817109,
                "updated_at": 1617817109,
            },
        }
        auth = Auth(mock_http_client)

        res = auth.custom_authentication(
            {"provider": "google", "settings": {"foo": "bar"}}
        )

        mock_http_client._execute.assert_called_once_with(
            method="POST",
            path="/v3/connect/custom",
            request_body={"provider": "google", "settings": {"foo": "bar"}},
        )
        assert type(res.data) is Grant
        assert res.data.id == "e19f8e1a-eb1c-41c0-b6a6-d2e59daf7f47"
        assert res.data.provider == "google"
        assert res.data.grant_status == "valid"
        assert res.data.email == "email@example.com"
        assert res.data.scope == ["Mail.Read", "User.Read", "offline_access"]
        assert res.data.user_agent == "string"
        assert res.data.ip == "string"
        assert res.data.state == "my-state"
        assert res.data.created_at == 1617817109
        assert res.data.updated_at == 1617817109

    def test_refresh_access_token(self, http_client_token_exchange):
        auth = Auth(http_client_token_exchange)
        config = {
            "redirect_uri": "https://example.com/oauth/callback",
            "refresh_token": "refresh-12345",
            "client_id": "abc-123",
            "client_secret": "secret",
        }

        auth.refresh_access_token(config)

        http_client_token_exchange._execute.assert_called_once_with(
            method="POST",
            path="/v3/connect/token",
            request_body={
                "redirect_uri": "https://example.com/oauth/callback",
                "refresh_token": "refresh-12345",
                "client_id": "abc-123",
                "client_secret": "secret",
                "grant_type": "refresh_token",
            },
        )

    def test_refresh_access_token_no_secret(self, http_client_token_exchange):
        http_client_token_exchange.api_key = "nylas-api-key"
        auth = Auth(http_client_token_exchange)
        config = {
            "redirect_uri": "https://example.com/oauth/callback",
            "refresh_token": "refresh-12345",
            "client_id": "abc-123",
        }

        auth.refresh_access_token(config)

        http_client_token_exchange._execute.assert_called_once_with(
            method="POST",
            path="/v3/connect/token",
            request_body={
                "redirect_uri": "https://example.com/oauth/callback",
                "refresh_token": "refresh-12345",
                "client_id": "abc-123",
                "client_secret": "nylas-api-key",
                "grant_type": "refresh_token",
            },
        )

    def test_id_token_info(self, http_client_token_info):
        auth = Auth(http_client_token_info)

        auth.id_token_info("id-123")

        http_client_token_info._execute.assert_called_once_with(
            method="GET",
            path="/v3/connect/tokeninfo",
            query_params={"id_token": "id-123"},
        )

    def test_validate_access_token(self, http_client_token_info):
        auth = Auth(http_client_token_info)

        auth.validate_access_token("id-123")

        http_client_token_info._execute.assert_called_once_with(
            method="GET",
            path="/v3/connect/tokeninfo",
            query_params={"access_token": "id-123"},
        )

    @mock.patch("uuid.uuid4")
    def test_url_for_oauth2_pkce(self, mock_uuid4, http_client):
        mock_uuid4.return_value = "nylas"
        auth = Auth(http_client)
        config = {
            "client_id": "abc-123",
            "redirect_uri": "https://example.com/oauth/callback",
            "scope": ["email.read_only", "calendar", "contacts"],
            "login_hint": "test@gmail.com",
            "provider": "google",
            "prompt": "select_provider,detect",
            "state": "abc-123-state",
        }

        result = auth.url_for_oauth2_pkce(config)

        assert (
            result.url
            == "https://test.nylas.com/v3/connect/auth?client_id=abc-123&redirect_uri=https%3A//example.com/oauth/callback&scope=email.read_only%20calendar%20contacts&login_hint=test%40gmail.com&provider=google&prompt=select_provider%2Cdetect&state=abc-123-state&response_type=code&access_type=online&code_challenge=ZTk2YmY2Njg2YTNjMzUxMGU5ZTkyN2RiNzA2OWNiMWNiYTliOTliMDIyZjQ5NDgzYTZjZTMyNzA4MDllNjhhMg&code_challenge_method=s256"
        )
        assert result.secret == "nylas"
        assert (
            result.secret_hash
            == "ZTk2YmY2Njg2YTNjMzUxMGU5ZTkyN2RiNzA2OWNiMWNiYTliOTliMDIyZjQ5NDgzYTZjZTMyNzA4MDllNjhhMg"
        )

    def test_url_for_admin_consent(self, http_client):
        auth = Auth(http_client)
        config = {
            "credential_id": "cred-123",
            "client_id": "abc-123",
            "redirect_uri": "https://example.com/oauth/callback",
            "scope": ["email.read_only", "calendar", "contacts"],
            "login_hint": "test@gmail.com",
            "prompt": "select_provider,detect",
            "state": "abc-123-state",
        }

        url = auth.url_for_admin_consent(config)

        assert (
            url
            == "https://test.nylas.com/v3/connect/auth?provider=microsoft&credential_id=cred-123&client_id=abc-123&redirect_uri=https%3A//example.com/oauth/callback&scope=email.read_only%20calendar%20contacts&login_hint=test%40gmail.com&prompt=select_provider%2Cdetect&state=abc-123-state&response_type=adminconsent&access_type=online"
        )

    def test_revoke(self, http_client_response):
        auth = Auth(http_client_response)

        res = auth.revoke("access_token")

        http_client_response._execute.assert_called_once_with(
            method="POST",
            path="/v3/connect/revoke",
            query_params={"token": "access_token"},
        )
        assert res is True

    def test_detect_provider(self):
        mock_http_client = Mock()
        mock_http_client._execute.return_value = {
            "request_id": "abc-123",
            "data": {
                "email_address": "test@gmail.com",
                "detected": True,
                "provider": "google",
                "type": "string",
            },
        }
        auth = Auth(mock_http_client)
        req = {
            "email": "test@gmail.com",
            "client_id": "client-123",
            "all_provider_types": True,
        }

        res = auth.detect_provider(req)

        mock_http_client._execute.assert_called_once_with(
            method="POST", path="/v3/providers/detect", query_params=req
        )
        assert type(res.data) == ProviderDetectResponse

import base64
import hashlib
import uuid

from nylas.config import RequestOverrides
from nylas.handler.http_client import _build_query_params
from nylas.models.grants import CreateGrantRequest, Grant

from nylas.models.auth import (
    CodeExchangeResponse,
    PkceAuthUrl,
    TokenInfoResponse,
    CodeExchangeRequest,
    TokenExchangeRequest,
    ProviderDetectResponse,
    ProviderDetectParams,
    URLForAuthenticationConfig,
    URLForAdminConsentConfig,
)
from nylas.models.response import Response
from nylas.resources.resource import Resource


def _hash_pkce_secret(secret: str) -> str:
    sha256_hash = hashlib.sha256(secret.encode()).hexdigest()
    return base64.b64encode(sha256_hash.encode()).decode().rstrip("=")


def _build_query(config: dict) -> dict:
    config["response_type"] = "code"

    if "access_type" not in config:
        config["access_type"] = "online"

    if "scope" in config:
        config["scope"] = " ".join(config["scope"])

    return config


def _build_query_with_pkce(config: dict, secret_hash: str) -> dict:
    params = _build_query(config)

    params["code_challenge"] = secret_hash
    params["code_challenge_method"] = "s256"

    return params


def _build_query_with_admin_consent(config: dict) -> dict:
    params = _build_query(config)

    params["response_type"] = "adminconsent"

    if "credential_id" in config:
        params["credential_id"] = config["credential_id"]

    return params


class Auth(Resource):
    """
    A collection of authentication related API endpoints

    These endpoints allow for various functionality related to authentication.
    """

    def url_for_oauth2(self, config: URLForAuthenticationConfig) -> str:
        """
        Build the URL for authenticating users to your application via Hosted Authentication.

        Args:
            config: The configuration for building the URL.

        Returns:
            The URL for hosted authentication.
        """
        query = _build_query(config)

        return self._url_auth_builder(query)

    def exchange_code_for_token(
        self, request: CodeExchangeRequest, overrides: RequestOverrides = None
    ) -> CodeExchangeResponse:
        """
        Exchange an authorization code for an access token.

        Args:
            request: The request parameters for the code exchange
            overrides: The request overrides to use for the request.

        Returns:
            Information about the Nylas application
        """
        if "client_secret" not in request:
            request["client_secret"] = self._http_client.api_key

        request_body = dict(request)
        request_body["grant_type"] = "authorization_code"

        return self._get_token(request_body, overrides)

    def custom_authentication(
        self, request_body: CreateGrantRequest, overrides: RequestOverrides = None
    ) -> Response[Grant]:
        """
        Create a Grant via Custom Authentication.

        Args:
            request_body: The values to create the Grant with.
            overrides: The request overrides to use for the request.

        Returns:
            The created Grant.
        """

        json_response, headers = self._http_client._execute(
            method="POST",
            path="/v3/connect/custom",
            request_body=request_body,
            overrides=overrides,
        )
        return Response.from_dict(json_response, Grant, headers)

    def refresh_access_token(
        self, request: TokenExchangeRequest, overrides: RequestOverrides = None
    ) -> CodeExchangeResponse:
        """
        Refresh an access token.

        Args:
            request: The refresh token request.
            overrides: The request overrides to use for the request.

        Returns:
            The response containing the new access token.
        """
        if "client_secret" not in request:
            request["client_secret"] = self._http_client.api_key

        request_body = dict(request)
        request_body["grant_type"] = "refresh_token"

        return self._get_token(request_body, overrides)

    def id_token_info(
        self, id_token: str, overrides: RequestOverrides = None
    ) -> Response[TokenInfoResponse]:
        """
        Get info about an ID token.

        Args:
            id_token: The ID token to query.
            overrides: The request overrides to use for the request.

        Returns:
            The API response with the token information.
        """

        query_params = {
            "id_token": id_token,
        }

        return self._get_token_info(query_params, overrides)

    def validate_access_token(
        self, access_token: str, overrides: RequestOverrides = None
    ) -> Response[TokenInfoResponse]:
        """
        Get info about an access token.

        Args:
            access_token: The access token to query.
            overrides: The request overrides to use for the request.

        Returns:
            The API response with the token information.
        """

        query_params = {
            "access_token": access_token,
        }

        return self._get_token_info(query_params, overrides)

    def url_for_oauth2_pkce(self, config: URLForAuthenticationConfig) -> PkceAuthUrl:
        """
        Build the URL for authenticating users to your application via Hosted Authentication with PKCE.

        IMPORTANT: YOU WILL NEED TO STORE THE 'secret' returned to use it inside the CodeExchange flow

        Args:
            config: The configuration for the authentication request.

        Returns:
            The URL for hosted authentication with secret & hashed secret.
        """
        secret = str(uuid.uuid4())
        secret_hash = _hash_pkce_secret(secret)
        query = _build_query_with_pkce(config, secret_hash)

        return PkceAuthUrl(secret, secret_hash, self._url_auth_builder(query))

    def url_for_admin_consent(self, config: URLForAdminConsentConfig) -> str:
        """Build the URL for admin consent authentication for Microsoft.

        Args:
            config: The configuration for the authentication request.

        Returns:
            The URL for hosted authentication.
        """
        config_with_provider = {"provider": "microsoft", **config}
        query = _build_query_with_admin_consent(config_with_provider)

        return self._url_auth_builder(query)

    def revoke(self, token: str, overrides: RequestOverrides = None) -> True:
        """Revoke a single access token.

        Args:
            token: The access token to revoke.
            overrides: The request overrides to use for the request.

        Returns:
            True: If the token was revoked successfully.
        """
        self._http_client._execute(
            method="POST",
            path="/v3/connect/revoke",
            query_params={"token": token},
            overrides=overrides,
        )

        return True

    def detect_provider(
        self, params: ProviderDetectParams, overrides: RequestOverrides = None
    ) -> Response[ProviderDetectResponse]:
        """
        Detect provider from email address.

        Args:
            params: The parameters to include in the request
            overrides: The request overrides to use for the request.

        Returns:
            The detected provider, if found.
        """

        json_response, headers = self._http_client._execute(
            method="POST",
            path="/v3/providers/detect",
            query_params=params,
            overrides=overrides,
        )
        return Response.from_dict(json_response, ProviderDetectResponse, headers)

    def _url_auth_builder(self, query: dict) -> str:
        base = f"{self._http_client.api_server}/v3/connect/auth"
        return _build_query_params(base, query)

    def _get_token(
        self, request_body: dict, overrides: RequestOverrides
    ) -> CodeExchangeResponse:
        json_response, _ = self._http_client._execute(
            method="POST",
            path="/v3/connect/token",
            request_body=request_body,
            overrides=overrides,
        )
        return CodeExchangeResponse.from_dict(json_response)

    def _get_token_info(
        self, query_params: dict, overrides: RequestOverrides
    ) -> Response[TokenInfoResponse]:
        json_response, headers = self._http_client._execute(
            method="GET",
            path="/v3/connect/tokeninfo",
            query_params=query_params,
            overrides=overrides,
        )
        return Response.from_dict(json_response, TokenInfoResponse, headers)

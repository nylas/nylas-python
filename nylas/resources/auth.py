import base64
import hashlib
import urllib.parse
import uuid

from nylas.handler.http_client import HttpClient
from nylas.models.auth import (
    CodeExchangeResponse,
    PkceAuthUrl,
    OpenID,
    ServerSideHostedAuthResponse,
)
from nylas.models.response import Response
from nylas.resources.grants import Grants
from nylas.resources.resource import Resource


def _hash_pkce_secret(secret: str) -> str:
    sha256_hash = hashlib.sha256(secret.encode()).digest()
    return base64.b64encode(sha256_hash).decode()


class Auth(Resource):
    def __init__(self, http_client: HttpClient, client_id: str, client_secret: str):
        super(Auth, self).__init__(http_client)
        self.client_id = client_id
        self.client_secret = client_secret

    @property
    def grants(self) -> Grants:
        return Grants(self._http_client)

    def exchange_code_for_token(
        self, code: str, redirect_uri: str, code_verifier: str = None
    ) -> Response[CodeExchangeResponse]:
        """Exchange an authorization code for an access token.

        Args:
            code (str): The OAuth 2.0 code from the authorization request.
            redirect_uri (str): The redirect URI of the integration.
            code_verifier (str): The code verifier used to generate the code challenge.

        Returns:
            Response: The API response with the access token information.
        """

        request_body = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
        }

        if code_verifier is not None:
            request_body["code_verifier"] = code_verifier

        return self._get_token(request_body)

    def refresh_access_token(
        self, refresh_token: str, redirect_uri: str
    ) -> Response[CodeExchangeResponse]:
        """Refresh an access token.

        Args:
            refresh_token (str): The refresh token to refresh.
            redirect_uri (str): The redirect URI of the integration.

        Returns:
            Response: The API response with the refreshed token information.
        """

        request_body = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "refresh_token",
            "code": refresh_token,
            "redirect_uri": redirect_uri,
        }

        return self._get_token(request_body)

    def validate_id_token(self, id_token: str) -> Response[OpenID]:
        """Validate an ID token.

        Args:
            id_token (str): The ID token to validate.

        Returns:
            Response: The API response with the token information.
        """

        query_params = {
            "id_token": id_token,
        }

        return self._validate_token(query_params)

    def validate_access_token(self, access_token: str) -> Response[OpenID]:
        """Validate an access token.

        Args:
            access_token (str): The access token to validate.

        Returns:
            Response: The API response with the token information.
        """

        query_params = {
            "access_token": access_token,
        }

        return self._validate_token(query_params)

    def url_for_authentication(self, config: dict) -> str:
        """Build the URL for authenticating users to your application via Hosted Authentication.

        Args:
            config (dict): The configuration for the authentication request.

        Returns:
            str: The URL for hosted authentication.
        """
        query = self._build_query(config)

        return self._url_auth_builder(query)

    def url_for_authentication_pkce(self, config: dict) -> PkceAuthUrl:
        """Build the URL for authenticating users to your application via Hosted Authentication with PKCE.

        IMPORTANT: YOU WILL NEED TO STORE THE 'secret' returned to use it inside the CodeExchange flow

        Args:
            config (dict): The configuration for the authentication request.

        Returns:
            PkceAuthUrl: The URL for hosted authentication with secret & hashed secret.
        """
        secret = str(uuid.uuid4())
        secret_hash = _hash_pkce_secret(secret)
        query = self._build_query_with_pkce(config, secret_hash)

        return PkceAuthUrl(secret, secret_hash, self._url_auth_builder(query))

    def url_for_admin_consent(self, config: dict) -> str:
        """Build the URL for admin consent authentication for Microsoft.

        Args:
            config (dict): The configuration for the authentication request.

        Returns:
            str: The URL for hosted authentication.
        """
        config_with_provider = {"provider": "microsoft", **config}
        query = self._build_query_with_admin_consent(config_with_provider)

        return self._url_auth_builder(query)

    def server_side_hosted_auth(
        self, config: dict
    ) -> Response[ServerSideHostedAuthResponse]:
        """Create a new authorization request and get a new unique login url.
        Used only for hosted authentication.
        This is the initial step requested from the server side to issue a new login url.

        Args:
            config (dict): The configuration for the authentication request.

        Returns:
            Response: The API response with the authorization request.
        """
        credentials = "{}:{}".format(self.client_id, self.client_secret)
        encoded_credentials = base64.b64encode(credentials.encode()).decode("utf-8")

        json_response = self._http_client._execute(
            method="POST",
            path="/v3/connect/auth",
            request_body=config,
            headers={"Authorization": "Basic {}".format(encoded_credentials)},
        )

        return Response.from_dict(json_response, ServerSideHostedAuthResponse)

    def revoke(self, token: str) -> True:
        """Revoke a single access token.

        Args:
            token (str): The access token to revoke.

        Returns:
            True: If the token was revoked successfully.
        """
        self._http_client._execute(
            method="POST",
            path="/v3/connect/revoke",
            query_params={"token": token},
        )

        return True

    def _url_auth_builder(self, query: dict) -> str:
        return "{}/v3/connect/auth?{}".format(
            self._http_client.api_server, urllib.parse.urlencode(query)
        )

    def _build_query(self, config: dict) -> dict:
        params = {
            "client_id": self.client_id,
            "redirect_uri": config["redirect_uri"],
            "access_type": config["accessType"] or "offline",
            "provider": config["provider"],
            "response_type": "code",
        }

        if config["loginHint"]:
            params["login_hint"] = config["loginHint"]
            if config["includeGrantScopes"]:
                params["include_grant_scopes"] = str(
                    config["includeGrantScopes"]
                ).lower()

        if config["scopes"]:
            params["scopes"] = " ".join(config["scopes"])

        if config["prompt"]:
            params["prompt"] = config["prompt"]

        if config["metadata"]:
            params["metadata"] = config["metadata"]

        if config["state"]:
            params["state"] = config["state"]

        return params

    def _build_query_with_pkce(self, config: dict, secret_hash: str) -> dict:
        params = self._build_query(config)

        params["code_challenge"] = secret_hash
        params["code_challenge_method"] = "s256"

        return params

    def _build_query_with_admin_consent(self, config: dict) -> dict:
        params = self._build_query(config)

        params["response_type"] = "adminconsent"
        params["credential_id"] = config["credentialId"]

        return params

    def _get_token(self, request_body: dict) -> Response[CodeExchangeResponse]:
        json_response = self._http_client._execute(
            method="POST", path="/v3/connect/token", request_body=request_body
        )
        return Response.from_dict(json_response, CodeExchangeResponse)

    def _validate_token(self, query_params: dict) -> Response[OpenID]:
        json_response = self._http_client._execute(
            method="GET", path="/v3/connect/tokeninfo", query_params=query_params
        )
        return Response.from_dict(json_response, OpenID)

import hashlib
import hmac
from enum import Enum
from nylas import APIClient


class Routes:
    def __init__(self, api):
        """
        Collection of helpful routes to be implemented in a Python server

        Args:
            api (APIClient): The configured Nylas API client

        Raises:
            ValueError: If a Nylas API client is not passed in
        """
        if not api or not isinstance(api, APIClient):
            raise ValueError("An APIClient must be set for Routes")
        self._api = api

    def build_auth_url(
        self, scopes, email_address, success_url, client_uri=None, state=None
    ):
        """
        Build the URL for authenticating users to your application via Hosted Authentication

        Args:
            scopes (list[str]): Authentication scopes to request from the authenticating user
            email_address (str): The user's email address
            success_url (str): The URI to which the user will be redirected once authentication completes
            client_uri (str): The route of the client
            state (str): An optional arbitrary string that is returned as a URL parameter in your redirect URI

        Returns:
            str: The URL for hosted authentication
        """
        return self._api.authentication_url(
            (client_uri or "") + success_url,
            login_hint=email_address,
            scopes=scopes,
            state=state,
        )

    def exchange_code_for_token(self, code):
        """
        Exchange an authorization code for an access token

        Args:
            code (str): One-time authorization code from Nylas

        Returns:
            dict: The object containing the access token and other information
        """
        return self._api.token_for_code(code)

    def verify_webhook_signature(self, nylas_signature, raw_body):
        """
        Verify incoming webhook signature came from Nylas

        Args:
            nylas_signature (str): The signature to verify
            raw_body (buffer): The raw body from the payload

        Returns:
            bool: True if the webhook signature was verified from Nylas
        """
        digest = hmac.new(
            self._api.client_secret, msg=raw_body, digestmod=hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(digest, nylas_signature)


class DefaultPaths(str, Enum):
    """
    This is an Enum representing the default paths the Nylas backend middlewares and frontend SDKs are preconfigured to
    """

    BUILD_AUTH_URL = "/nylas/generate-auth-url"
    EXCHANGE_CODE_FOR_TOKEN = "/nylas/exchange-mailbox-token"
    WEBHOOKS = "/nylas/webhook"

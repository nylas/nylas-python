from dataclasses import dataclass
from typing import Optional, List, Literal

from dataclasses_json import dataclass_json
from typing_extensions import TypedDict, NotRequired

AccessType = Literal["online", "offline"]
Provider = Literal["google", "imap", "microsoft"]


class URLForAuthenticationConfig(TypedDict):
    """
    Configuration for generating a URL for OAuth 2.0 authentication.

    Attributes:
        client_id: The client ID of your application.
        redirect_uri: Redirect URI of the integration.
        provider: The integration provider type that you already had set up with Nylas for this application.
            If not set, the user is directed to the Hosted Login screen and prompted to select a provider.
        access_type: If the exchange token should return a refresh token too.
            Not suitable for client side or JavaScript apps.
        prompt: The prompt parameter is used to force the consent screen to be displayed even if the user has already given consent to your application.
        scope: A space-delimited list of scopes that identify the resources that your application could access on the user's behalf.
            If no scope is given, all of the default integration's scopes are used.
        include_grant_scopes: If set to true, the scopes granted to the application will be included in the response.
        state: Optional state to be returned after authentication
        login_hint: Prefill the login name (usually email) during authorization flow.
            If a Grant for the provided email already exists, a Grant's re-auth will automatically be initiated.
    """

    client_id: str
    redirect_uri: str
    provider: NotRequired[Provider]
    access_type: NotRequired[AccessType]
    prompt: NotRequired[str]
    scope: NotRequired[List[str]]
    include_grant_scopes: NotRequired[bool]
    state: NotRequired[str]
    login_hint: NotRequired[str]


class URLForAdminConsentConfig(URLForAuthenticationConfig):
    """
    Configuration for generating a URL for admin consent authentication for Microsoft.

    Attributes:
        credential_id: The credential ID for the Microsoft account
    """

    credential_id: str


class CodeExchangeRequest(TypedDict):
    """
    Interface of a Nylas code exchange request

    Attributes:
        redirect_uri: Should match the same redirect URI that was used for getting the code during the initial authorization request.
        code: OAuth 2.0 code fetched from the previous step.
        client_id: Client ID of the application.
        client_secret: Client secret of the application.
        code_verifier: The original plain text code verifier (code_challenge) used in the initial authorization request (PKCE).
    """

    redirect_uri: str
    code: str
    client_id: str
    client_secret: str
    code_verifier: NotRequired[str]


class TokenExchangeRequest(TypedDict):
    """
    Interface of a Nylas token exchange request

    Attributes:
        redirect_uri: Should match the same redirect URI that was used for getting the code during the initial authorization request.
        refresh_token: Token to refresh/request your short-lived access token
        client_id: Client ID of the application.
        client_secret: Client secret of the application.
    """

    redirect_uri: str
    refresh_token: str
    client_id: str
    client_secret: str


@dataclass_json
@dataclass
class CodeExchangeResponse:
    access_token: str
    grant_id: str
    scope: str
    expires_in: int
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None
    token_type: Optional[str] = None


@dataclass_json
@dataclass
class OpenID:
    iss: str
    aud: str
    iat: int
    exp: int
    sub: Optional[str] = None
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    at_hash: Optional[str] = None
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    nick_name: Optional[str] = None
    picture_url: Optional[str] = None
    genre: Optional[str] = None
    locale: Optional[str] = None


@dataclass_json
@dataclass
class PkceAuthUrl:
    secret: str
    secret_hash: str
    url: str


class ProviderDetectParams(TypedDict):
    """
    Interface representing the object used to set parameters for detecting a provider.

    Attributes:
        email: Email address to detect the provider for.
        client_id: Client ID of the Nylas application.
        all_provider_types: Search by all providers regardless of created integrations. If unset, defaults to false.
    """

    email: str
    client_id: str
    all_provider_types: NotRequired[bool]


@dataclass_json
@dataclass
class ProviderDetectResponse:
    """
    Interface representing the Nylas provider detect response.

    Attributes:
        email_address: Email provided for autodetection
        detected: Whether the provider was detected
        provider: Detected provider
        type: Provider type (if IMAP provider detected displays the IMAP provider)
    """

    email_address: str
    detected: bool
    provider: Optional[str] = None
    type: Optional[str] = None

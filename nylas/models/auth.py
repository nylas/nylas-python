from dataclasses import dataclass
from typing import Optional, List, Literal

from dataclasses_json import dataclass_json
from typing_extensions import TypedDict, NotRequired

AccessType = Literal["online", "offline"]
""" Literal for the access type of the authentication URL. """

Provider = Literal["google", "imap", "microsoft", "icloud", "virtual-calendar", "yahoo", "ews", "zoom"]
""" Literal for the different authentication providers. """

Prompt = Literal[
    "select_provider", "detect", "select_provider,detect", "detect,select_provider"
]
""" Literal for the different supported OAuth prompts. """


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
        prompt: The prompt parameter is used to force the consent screen to be displayed even if the user
            has already given consent to your application.
        scope: A space-delimited list of scopes that identify the resources that your application
            could access on the user's behalf.
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
    prompt: NotRequired[Prompt]
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
        redirect_uri: Should match the same redirect URI that was used for getting the code during the initial
            authorization request.
        code: OAuth 2.0 code fetched from the previous step.
        client_id: Client ID of the application.
        client_secret: Client secret of the application. If not provided, the API Key will be used instead.
        code_verifier: The original plain text code verifier (code_challenge) used in the initial
            authorization request (PKCE).
    """

    redirect_uri: str
    code: str
    client_id: str
    client_secret: NotRequired[str]
    code_verifier: NotRequired[str]


class TokenExchangeRequest(TypedDict):
    """
    Interface of a Nylas token exchange request

    Attributes:
        redirect_uri: Should match the same redirect URI that was used for getting the code during the initial
            authorization request.
        refresh_token: Token to refresh/request your short-lived access token
        client_id: Client ID of the application.
        client_secret: Client secret of the application. If not provided, the API Key will be used instead.
    """

    redirect_uri: str
    refresh_token: str
    client_id: str
    client_secret: NotRequired[str]


@dataclass_json
@dataclass
class CodeExchangeResponse:
    """
    Class representation of a Nylas code exchange response.

    Attributes:
        access_token: Supports exchanging the Nylas code for an access token, or refreshing an access token.
        grant_id: ID representing the new Grant.
        scope: List of scopes associated with the token.
        expires_in: The remaining lifetime of the access token, in seconds.
        email: Email address of the grant that is created.
        refresh_token: Returned only if the code is requested using "access_type=offline".
        id_token: A JWT that contains identity information about the user. Digitally signed by Nylas.
        token_type: Always "Bearer".
        provider: The provider that the code was exchanged with.
    """

    access_token: str
    grant_id: str
    expires_in: int
    email: Optional[str] = None
    refresh_token: Optional[str] = None
    scope: Optional[str] = None
    id_token: Optional[str] = None
    token_type: Optional[str] = None
    provider: Optional[Provider] = None


@dataclass_json
@dataclass
class TokenInfoResponse:
    """
    Class representation of a Nylas token information response.

    Attributes:
        iss: The issuer of the token.
        aud: The token's audience.
        iat: The time that the token was issued.
        exp: The time that the token expires.
        sub: The token's subject.
        email: The email address of the Grant belonging to the user's token.
    """

    iss: str
    aud: str
    iat: int
    exp: int
    sub: Optional[str] = None
    email: Optional[str] = None


@dataclass_json
@dataclass
class PkceAuthUrl:
    """
    Class representing the object containing the OAuth 2.0 URL and the hashed secret.

    Attributes:
        secret: Server-side challenge used in the OAuth 2.0 flow.
        secret_hash: SHA-256 hash of the secret.
        url: The URL for hosted authentication.
    """

    secret: str
    secret_hash: str
    url: str


class ProviderDetectParams(TypedDict):
    """
    Interface representing the object used to set parameters for detecting a provider.

    Attributes:
        email: Email address to detect the provider for.
        all_provider_types: Search by all providers regardless of created integrations. If unset, defaults to false.
    """

    email: str
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

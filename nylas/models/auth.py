from dataclasses import dataclass
from typing import Optional, Dict, Any, List, Literal

from dataclasses_json import dataclass_json


AccessType = Literal["online", "offline"]
Provider = Literal["google", "imap", "microsoft"]


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


@dataclass_json
@dataclass
class ServerSideHostedAuthRequest:
    redirect_uri: str
    provider: Optional[Provider] = None
    state: Optional[str] = None
    login_hint: Optional[str] = None
    cookie_nonce: Optional[str] = None
    grant_id: Optional[str] = None
    scope: Optional[List[str]] = None
    expires_in: Optional[int] = None
    settings: Optional[Dict[str, Any]] = None


@dataclass_json
@dataclass
class ServerSideHostedAuthResponse:
    url: str
    id: str
    expires_at: int
    request: ServerSideHostedAuthRequest

from dataclasses import dataclass
from typing import Optional

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class ProviderSettings:
    name: Optional[str] = None
    imap_host: Optional[str] = None
    imap_port: Optional[int] = None
    smtp_host: Optional[str] = None
    smtp_port: Optional[int] = None
    password_link: Optional[str] = None
    primary: Optional[bool] = None


@dataclass_json
@dataclass
class Provider:
    name: str
    provider: str
    type: str
    settings: Optional[ProviderSettings] = None


@dataclass_json
@dataclass
class ProviderDetectResponse:
    email_address: str
    detected: bool
    provider: Optional[str] = None
    type: Optional[str] = None

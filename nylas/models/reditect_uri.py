from dataclasses import dataclass
from typing import Optional

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class RedirectUriSettings:
    origin: Optional[str] = None
    bundle_id: Optional[str] = None
    package_name: Optional[str] = None
    sha1_certificate_fingerprint: Optional[str] = None


@dataclass_json
@dataclass
class RedirectUri:
    id: str
    url: str
    platform: str
    settings: Optional[RedirectUriSettings] = None

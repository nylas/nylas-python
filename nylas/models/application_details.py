from dataclasses import dataclass
from typing import Literal, Optional, List

from dataclasses_json import dataclass_json

from nylas.models.reditect_uri import RedirectUri

Region = Literal["us", "eu"]
Environment = Literal["production", "staging"]


@dataclass_json
@dataclass
class Branding:
    name: str
    icon_url: Optional[str] = None
    website_url: Optional[str] = None
    description: Optional[str] = None


@dataclass_json
@dataclass
class HostedAuthentication:
    background_image_url: str
    alignment: Optional[str] = None
    color_primary: Optional[str] = None
    color_secondary: Optional[str] = None
    title: Optional[str] = None
    subtitle: Optional[str] = None
    background_color: Optional[str] = None
    spacing: Optional[int] = None


@dataclass_json
@dataclass
class ApplicationDetails:
    application_id: str
    organization_id: str
    region: Region
    environment: Environment
    branding: Branding
    hostedAuthentication: Optional[HostedAuthentication] = None
    redirect_uris: List[RedirectUri] = None

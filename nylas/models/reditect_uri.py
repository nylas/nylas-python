from dataclasses import dataclass
from typing import Optional

from dataclasses_json import dataclass_json
from typing_extensions import TypedDict, NotRequired


@dataclass_json
@dataclass
class RedirectUriSettings:
    origin: Optional[str] = None
    bundle_id: Optional[str] = None
    app_store_id: Optional[str] = None
    team_id: Optional[str] = None
    package_name: Optional[str] = None
    sha1_certificate_fingerprint: Optional[str] = None


@dataclass_json
@dataclass
class RedirectUri:
    id: str
    url: str
    platform: str
    settings: Optional[RedirectUriSettings] = None


class WritableRedirectUriSettings(TypedDict):
    """
    Class representing redirect uri settings to be provided for a create/update call.

    Attributes:
        origin: Optional origin for the redirect uri.
        bundle_id: Optional bundle id for the redirect uri.
        app_store_id: Optional app store id for the redirect uri.
        team_id: Optional team id for the redirect uri.
        package_name: Optional package name for the redirect uri.
        sha1_certificate_fingerprint: Optional sha1 certificate fingerprint for the redirect uri.
    """

    origin: NotRequired[str]
    bundle_id: NotRequired[str]
    app_store_id: NotRequired[str]
    team_id: NotRequired[str]
    package_name: NotRequired[str]
    sha1_certificate_fingerprint: NotRequired[str]


class CreateRedirectUriRequest(TypedDict):
    """
    Class representing a request to create a redirect uri.

    Attributes:
        url: Redirect URL.
        platform: Platform identifier.
        settings: Optional settings for the redirect uri.
    """

    url: str
    platform: str
    settings: NotRequired[WritableRedirectUriSettings]


class UpdateRedirectUriRequest(TypedDict):
    """
    Class representing a request to update a redirect uri.

    Attributes:
        url: Redirect URL.
        platform: Platform identifier.
        settings: Optional settings for the redirect uri.
    """

    url: NotRequired[str]
    platform: NotRequired[str]
    settings: NotRequired[WritableRedirectUriSettings]

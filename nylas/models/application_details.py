from dataclasses import dataclass, field
from typing import Literal, Optional, List

from dataclasses_json import dataclass_json

from nylas.models.redirect_uri import RedirectUri

Region = Literal["us", "eu"]
""" Literal representing the available Nylas API regions. """

Environment = Literal["production", "staging"]
""" Literal representing the different Nylas API environments. """


@dataclass_json
@dataclass
class Branding:
    """
    Class representation of branding details for the application.

    Attributes:
        name: Name of the application.
        icon_url: URL pointing to the application icon.
        website_url: Application/publisher website URL.
        description: Description of the application.
    """

    name: str
    icon_url: Optional[str] = None
    website_url: Optional[str] = None
    description: Optional[str] = None


@dataclass_json
@dataclass
class HostedAuthentication:
    """
    Class representation of hosted authentication branding details.

    Attributes:
        background_image_url: URL pointing to the background image.
        alignment: Alignment of the background image.
        color_primary: Primary color of the hosted authentication page.
        color_secondary: Secondary color of the hosted authentication page.
        title: Title of the hosted authentication page.
        subtitle: Subtitle for the hosted authentication page.
        background_color: Background color of the hosted authentication page.
        spacing: CSS spacing attribute in px.
    """

    background_image_url: Optional[str] = None
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
    """
    Class representation of a Nylas application details object.

    Attributes:
        application_id: Public application ID.
        organization_id: ID representing the organization.
        region: Region identifier.
        environment: Environment identifier.
        branding: Branding details for the application.
        hosted_authentication: Hosted authentication branding details.
        callback_uris: List of redirect URIs.
    """

    application_id: str
    organization_id: str
    region: Region
    environment: Environment
    branding: Branding
    hosted_authentication: Optional[HostedAuthentication] = None
    callback_uris: List[RedirectUri] = field(default_factory=list)

from dataclasses import dataclass, field
from typing import Optional, List

from dataclasses_json import dataclass_json
from typing_extensions import TypedDict, NotRequired

from nylas.models.redirect_uri import RedirectUri, WritableRedirectUriSettings

Region = str
""" The Nylas API region (free-form string, e.g. ``us``, ``eu``). """

Environment = str
""" The Nylas API environment (free-form string, e.g. ``sandbox``). """


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
        terms_of_service_url: URL pointing to the terms of service.
        privacy_policy_url: URL pointing to the privacy policy.
    """

    background_image_url: Optional[str] = None
    alignment: Optional[str] = None
    color_primary: Optional[str] = None
    color_secondary: Optional[str] = None
    title: Optional[str] = None
    subtitle: Optional[str] = None
    background_color: Optional[str] = None
    spacing: Optional[int] = None
    terms_of_service_url: Optional[str] = None
    privacy_policy_url: Optional[str] = None


@dataclass_json
@dataclass
class IdpSettings:
    """
    Class representation of identity provider settings for the application.

    Attributes:
        origins: Comma-separated list of allowed origins.
        issuers: Comma-separated list of allowed issuers.
    """

    origins: Optional[str] = None
    issuers: Optional[str] = None


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
        domain: The white-label domain associated with the application, if any.
        hosted_authentication: Hosted authentication branding details.
        idp_settings: Identity provider settings.
        callback_uris: List of redirect URIs.
        created_at: Unix timestamp (seconds) when the application was created.
        updated_at: Unix timestamp (seconds) when the application was last updated.
        blocked: Whether the application is blocked.
    """

    application_id: str
    organization_id: str
    region: Region
    environment: Environment
    branding: Branding
    domain: Optional[str] = None
    hosted_authentication: Optional[HostedAuthentication] = None
    idp_settings: Optional[IdpSettings] = None
    callback_uris: List[RedirectUri] = field(default_factory=list)
    created_at: Optional[int] = None
    updated_at: Optional[int] = None
    blocked: Optional[bool] = None


class WritableBranding(TypedDict):
    """
    Class representing branding details for a create/update application call.

    Attributes:
        name: Name of the application.
        icon_url: URL pointing to the application icon.
        website_url: Application/publisher website URL.
        description: Description of the application.
    """

    name: NotRequired[str]
    icon_url: NotRequired[str]
    website_url: NotRequired[str]
    description: NotRequired[str]


class WritableHostedAuthentication(TypedDict):
    """
    Class representing hosted authentication details for a create/update application call.

    Attributes:
        background_image_url: URL pointing to the background image.
        alignment: Alignment of the background image.
        color_primary: Primary color of the hosted authentication page.
        color_secondary: Secondary color of the hosted authentication page.
        title: Title of the hosted authentication page.
        subtitle: Subtitle for the hosted authentication page.
        background_color: Background color of the hosted authentication page.
        spacing: CSS spacing attribute in px.
        terms_of_service_url: URL pointing to the terms of service.
        privacy_policy_url: URL pointing to the privacy policy.
    """

    background_image_url: NotRequired[str]
    alignment: NotRequired[str]
    color_primary: NotRequired[str]
    color_secondary: NotRequired[str]
    title: NotRequired[str]
    subtitle: NotRequired[str]
    background_color: NotRequired[str]
    spacing: NotRequired[int]
    terms_of_service_url: NotRequired[str]
    privacy_policy_url: NotRequired[str]


class WritableIdpSettings(TypedDict):
    """
    Class representing identity provider settings for a create/update application call.

    Attributes:
        origins: Comma-separated list of allowed origins.
        issuers: Comma-separated list of allowed issuers.
    """

    origins: NotRequired[str]
    issuers: NotRequired[str]


class WritableAdditionalSettings(TypedDict):
    """
    Class representing additional application settings for an update call.

    These settings are write-only: they can be set via the update call but are
    stripped from every response and are not bound on the application model.

    Attributes:
        login_url: The login URL.
        logout_url: The logout URL.
        refresh_token_expiration_absolute: Absolute refresh token expiration.
        refresh_token_expiration_idle: Idle refresh token expiration.
        rotate_refresh_token: Whether to rotate the refresh token.
        allow_query_param_in_redirect_uri: Whether query params are allowed in redirect URIs.
    """

    login_url: NotRequired[str]
    logout_url: NotRequired[str]
    refresh_token_expiration_absolute: NotRequired[int]
    refresh_token_expiration_idle: NotRequired[int]
    rotate_refresh_token: NotRequired[bool]
    allow_query_param_in_redirect_uri: NotRequired[bool]


class UpdateApplicationRedirectUriRequest(TypedDict):
    """
    Class representing a callback URI provided for an update application call.

    Attributes:
        id: Existing callback URI ID. Include this when preserving or updating an existing URI.
        url: Redirect URL.
        platform: Platform identifier. Optional; defaults to "web" server-side.
        settings: Optional settings for the redirect URI.
    """

    id: NotRequired[str]
    url: str
    platform: NotRequired[str]
    settings: NotRequired[WritableRedirectUriSettings]


class UpdateApplicationRequest(TypedDict):
    """
    Class representing a request to update a Nylas application.

    Note:
        ``additional_settings`` is write-only and is stripped from the response.

    Attributes:
        branding: Branding details for the application.
        hosted_authentication: Hosted authentication branding details.
        idp_settings: Identity provider settings.
        callback_uris: List of callback URIs for the application.
        domain: The white-label domain associated with the application.
        additional_settings: Additional (write-only) application settings.
    """

    branding: NotRequired[WritableBranding]
    hosted_authentication: NotRequired[WritableHostedAuthentication]
    idp_settings: NotRequired[WritableIdpSettings]
    callback_uris: NotRequired[List[UpdateApplicationRedirectUriRequest]]
    domain: NotRequired[str]
    additional_settings: NotRequired[WritableAdditionalSettings]

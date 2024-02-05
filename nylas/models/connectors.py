from dataclasses import dataclass
from typing import Dict, Any, List, Optional, Union
from typing_extensions import TypedDict, NotRequired

from dataclasses_json import dataclass_json

from nylas.models.auth import Provider
from nylas.models.list_query_params import ListQueryParams


@dataclass_json
@dataclass
class Connector:
    """
    Interface representing the Nylas connector response.

    Attributes:
        provider: The provider type
        settings: Optional settings from provider
        scope: Default scopes for the connector
    """

    provider: Provider
    settings: Optional[Dict[str, Any]] = None
    scope: Optional[List[str]] = None


class BaseCreateConnectorRequest(TypedDict):
    """
    Interface representing the base Nylas connector creation request.

    Attributes:
        provider: The provider type
    """

    provider: Provider


class GoogleCreateConnectorSettings(TypedDict):
    """
    Interface representing a Google connector creation request.

    Attributes:
        client_id: The Google Client ID
        client_secret: The Google Client Secret
        topic_name: The Google Pub/Sub topic name
    """

    client_id: str
    client_secret: str
    topic_name: NotRequired[str]


class MicrosoftCreateConnectorSettings(TypedDict):
    """
    Interface representing a Microsoft connector creation request.

    Attributes:
        client_id: The Google Client ID
        client_secret: The Google Client Secret
        tenant: The Microsoft tenant ID
    """

    client_id: str
    client_secret: str
    tenant: NotRequired[str]


class GoogleCreateConnectorRequest(BaseCreateConnectorRequest):
    """
    Interface representing the base Nylas connector creation request.

    Attributes:
        provider (Provider): The provider type, should be Google
        settings: The Google OAuth provider credentials and settings
        scope: The Google OAuth scopes
    """

    settings: GoogleCreateConnectorSettings
    scope: NotRequired[List[str]]


class MicrosoftCreateConnectorRequest(BaseCreateConnectorRequest):
    """
    Interface representing the base Nylas connector creation request.

    Attributes:
        name (str): Custom name of the connector
        provider (Provider): The provider type, should be Google
        settings: The Microsoft OAuth provider credentials and settings
        scope: The Microsoft OAuth scopes
    """

    settings: MicrosoftCreateConnectorSettings
    scope: NotRequired[List[str]]


class ImapCreateConnectorRequest(BaseCreateConnectorRequest):
    """
    Interface representing the base Nylas connector creation request.

    Attributes:
        name (str): Custom name of the connector
        provider (Provider): The provider type, should be IMAP
    """

    pass


class VirtualCalendarsCreateConnectorRequest(BaseCreateConnectorRequest):
    """
    Interface representing the base Nylas connector creation request.

    Attributes:
        name (str): Custom name of the connector
        provider (Provider): The provider type
    """

    pass


CreateConnectorRequest = Union[
    GoogleCreateConnectorRequest,
    MicrosoftCreateConnectorRequest,
    ImapCreateConnectorRequest,
    VirtualCalendarsCreateConnectorRequest,
]
""" The type of the Nylas connector creation request. """


class UpdateConnectorRequest(TypedDict):
    """
    Interface representing the base Nylas connector creation request.

    Attributes:
        name: Custom name of the connector
        settings: The OAuth provider credentials and settings
        scope: The OAuth scopes
    """

    name: NotRequired[str]
    settings: NotRequired[Dict[str, Any]]
    scope: NotRequired[List[str]]


class ListConnectorQueryParams(ListQueryParams):
    """
    Interface of the query parameters for listing connectors.

    Attributes:
        limit (NotRequired[int]): The maximum number of objects to return.
            This field defaults to 50. The maximum allowed value is 200.
        page_token (NotRequired[str]): An identifier that specifies which page of data to return.
            This value should be taken from a ListResponse object's next_cursor parameter.
    """

    pass

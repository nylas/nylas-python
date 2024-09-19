from dataclasses import dataclass, field
from typing import List, Any, Dict, Optional

from dataclasses_json import dataclass_json
from typing_extensions import TypedDict, NotRequired

from nylas.models.auth import Provider


@dataclass_json
@dataclass
class Grant:
    """
    Interface representing a Nylas Grant object.

    Attributes:
        id: Globally unique object identifier.
        provider: OAuth provider that the user authenticated with.
        account_id: Globally unique identifier for your v2 account that has been migrated using our migration APIs.
        scope: Scopes specified for the grant.
        created_at: Unix timestamp when the grant was created.
        grant_status: Status of the grant, if it is still valid or if the user needs to re-authenticate.
        email: Email address associated with the grant.
        user_agent: End user's client user agent.
        ip: End user's client IP address.
        state: Initial state that was sent as part of the OAuth request.
        updated_at: Unix timestamp when the grant was updated.
        provider_user_id: Provider's ID for the user this grant is associated with.
        settings: Settings required by the provider that were sent as part of the OAuth request.
    """

    id: str
    provider: str
    scope: List[str] = field(default_factory=list)
    account_id: Optional[str] = None
    grant_status: Optional[str] = None
    email: Optional[str] = None
    user_agent: Optional[str] = None
    ip: Optional[str] = None
    state: Optional[str] = None
    created_at: Optional[int] = None
    updated_at: Optional[int] = None
    provider_user_id: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None


class CreateGrantRequest(TypedDict):
    """
    Interface representing a request to create a grant.

    Attributes:
        provider: OAuth provider.
        settings: Settings required by provider.
        state: Optional state value to return to developer's website after authentication flow is completed.
        scope: Optional list of scopes to request. If not specified it will use the integration default scopes.
    """

    provider: Provider
    settings: Dict[str, Any]
    state: NotRequired[str]
    scope: NotRequired[List[str]]


class UpdateGrantRequest(TypedDict):
    """
    Interface representing a request to update a grant.

    Attributes:
        settings: Settings required by provider.
        scope: List of integration scopes for the grant.
    """

    settings: NotRequired[Dict[str, Any]]
    scope: NotRequired[List[str]]


class ListGrantsQueryParams(TypedDict):
    """
    Interface representing the query parameters for listing grants.

    Attributes:
        limit: The maximum number of objects to return.
            This field defaults to 10. The maximum allowed value is 200.
        offset: Offset grant results by this number.
        sortBy: Sort entries by field name
        orderBy: Specify ascending or descending order.
        since: Scope grants from a specific point in time by Unix timestamp.
        before: Scope grants to a specific point in time by Unix timestamp.
        email: Filtering your query based on grant email address (if applicable)
        grantStatus: Filtering your query based on grant email status (if applicable)
        ip: Filtering your query based on grant IP address
        provider: Filtering your query based on OAuth provider
    """

    limit: NotRequired[int]
    offset: NotRequired[int]
    sortBy: NotRequired[str]
    orderBy: NotRequired[str]
    since: NotRequired[int]
    before: NotRequired[int]
    email: NotRequired[str]
    grantStatus: NotRequired[str]
    ip: NotRequired[str]
    provider: NotRequired[Provider]

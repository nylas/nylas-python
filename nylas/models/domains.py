from dataclasses import dataclass, field
from typing import Any, Literal, Optional

from dataclasses_json import config, dataclass_json
from typing_extensions import NotRequired, TypedDict

from nylas.models.list_query_params import ListQueryParams

DomainVerificationRequestType = Literal["ownership", "dkim", "spf", "feedback", "mx"]
DomainVerificationType = Literal[
    "ownership", "dkim", "spf", "feedback", "mx", "dmarc", "arc"
]


class DomainVerificationOptions(TypedDict, total=False):
    """Options for domain verification operations."""

    key_length: int


class ListDomainsQueryParams(ListQueryParams):
    """
    Query parameters for listing domains.

    Attributes:
        limit: Maximum number of objects to return.
        page_token: Cursor for the next page (from ``next_cursor`` on the previous response).
    """

    pass


class CreateDomainRequest(TypedDict):
    """Request body for registering a domain."""

    name: str
    domain_address: str


class UpdateDomainRequest(TypedDict, total=False):
    """Request body for updating a domain (currently only ``name`` is supported)."""

    name: str


class GetDomainInfoRequest(TypedDict):
    """Request body for retrieving DNS records for a verification type."""

    type: DomainVerificationRequestType
    options: NotRequired[DomainVerificationOptions]


class VerifyDomainRequest(TypedDict):
    """Request body for triggering DNS verification."""

    type: DomainVerificationRequestType
    options: NotRequired[DomainVerificationOptions]


@dataclass_json
@dataclass
class Domain:
    """
    A domain registered for Transactional Send or Nylas Inbound.
    """

    id: str
    name: str
    branded: bool
    domain_address: str
    organization_id: str
    region: str
    verified_ownership: bool
    verified_dkim: bool
    verified_spf: bool
    verified_mx: bool
    verified_feedback: bool
    verified_dmarc: bool
    verified_arc: bool
    created_at: int
    updated_at: int


@dataclass_json
@dataclass
class DomainVerificationAttempt:
    """
    DNS verification attempt or required records for a verification type.
    """

    verification_type: Optional[str] = field(
        default=None, metadata=config(field_name="type")
    )
    options: Optional[Any] = None
    host: Optional[str] = None
    value: Optional[str] = None
    status: Optional[str] = None


@dataclass_json
@dataclass
class DomainVerificationDetails:
    """
    Response data from get domain info or verify domain endpoints.
    """

    domain_id: str
    attempt: Optional[DomainVerificationAttempt] = None
    created_at: Optional[int] = None
    expires_at: Optional[int] = None
    message: Optional[str] = None

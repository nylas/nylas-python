from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import dataclass_json
from typing_extensions import NotRequired, TypedDict

from nylas.models.list_query_params import ListQueryParams


class ListPoliciesQueryParams(ListQueryParams):
    """
    Query parameters for listing policies.

    Attributes:
        limit: Maximum number of objects to return.
        page_token: Cursor for the next page (from ``next_cursor`` on the previous response).
    """

    pass


class PolicyOptionsRequest(TypedDict, total=False):
    """Request shape for policy options."""

    additional_folders: NotRequired[List[str]]
    use_cidr_aliasing: NotRequired[bool]


class PolicyLimitsRequest(TypedDict, total=False):
    """Request shape for policy limits."""

    limit_attachment_size_limit: NotRequired[int]
    limit_attachment_count_limit: NotRequired[int]
    limit_attachment_allowed_types: NotRequired[List[str]]
    limit_size_total_mime: NotRequired[int]
    limit_storage_total: NotRequired[int]
    limit_count_daily_message_per_grant: NotRequired[int]
    limit_inbox_retention_period: NotRequired[int]
    limit_spam_retention_period: NotRequired[int]


class PolicySpamDetectionRequest(TypedDict, total=False):
    """Request shape for policy spam detection settings."""

    use_list_dnsbl: NotRequired[bool]
    use_header_anomaly_detection: NotRequired[bool]
    spam_sensitivity: NotRequired[float]


class CreatePolicyRequest(TypedDict):
    """Request body for creating a policy."""

    name: str
    options: NotRequired[PolicyOptionsRequest]
    limits: NotRequired[PolicyLimitsRequest]
    rules: NotRequired[List[str]]
    spam_detection: NotRequired[PolicySpamDetectionRequest]


class UpdatePolicyRequest(TypedDict, total=False):
    """Request body for updating a policy."""

    name: NotRequired[str]
    options: NotRequired[PolicyOptionsRequest]
    limits: NotRequired[PolicyLimitsRequest]
    rules: NotRequired[List[str]]
    spam_detection: NotRequired[PolicySpamDetectionRequest]


@dataclass_json
@dataclass
class PolicyOptions:
    """Policy options applied to inboxes that use this policy."""

    additional_folders: Optional[List[str]] = None
    use_cidr_aliasing: Optional[bool] = None


@dataclass_json
@dataclass
class PolicyLimits:
    """Operational limits applied to inboxes that use this policy."""

    limit_attachment_size_limit: Optional[int] = None
    limit_attachment_count_limit: Optional[int] = None
    limit_attachment_allowed_types: Optional[List[str]] = None
    limit_size_total_mime: Optional[int] = None
    limit_storage_total: Optional[int] = None
    limit_count_daily_message_per_grant: Optional[int] = None
    limit_inbox_retention_period: Optional[int] = None
    limit_spam_retention_period: Optional[int] = None


@dataclass_json
@dataclass
class PolicySpamDetection:
    """Spam detection settings applied to inboxes that use this policy."""

    use_list_dnsbl: Optional[bool] = None
    use_header_anomaly_detection: Optional[bool] = None
    spam_sensitivity: Optional[float] = None


@dataclass_json
@dataclass
class Policy:
    """A policy for Nylas Agent Accounts."""

    id: Optional[str] = None
    name: Optional[str] = None
    application_id: Optional[str] = None
    organization_id: Optional[str] = None
    options: Optional[PolicyOptions] = None
    limits: Optional[PolicyLimits] = None
    rules: Optional[List[str]] = None
    spam_detection: Optional[PolicySpamDetection] = None
    created_at: Optional[int] = None
    updated_at: Optional[int] = None

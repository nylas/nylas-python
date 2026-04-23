from dataclasses import dataclass
from typing import Any, List, Optional

from dataclasses_json import dataclass_json
from typing_extensions import NotRequired, TypedDict

from nylas.models.list_query_params import ListQueryParams


class ListRulesQueryParams(ListQueryParams):
    """Query parameters for listing rules."""

    pass


class ListRuleEvaluationsQueryParams(ListQueryParams):
    """Query parameters for listing rule evaluations."""

    pass


class RuleConditionRequest(TypedDict):
    """A single condition used in a rule match clause."""

    field: str
    operator: str
    value: Any


class RuleMatchRequest(TypedDict):
    """Match clause for create/update rule requests."""

    conditions: List[RuleConditionRequest]
    operator: NotRequired[str]


class RuleActionRequest(TypedDict):
    """Action object used in create/update rule requests."""

    type: str
    value: NotRequired[str]


class CreateRuleRequest(TypedDict):
    """Request body for creating a rule."""

    name: str
    match: RuleMatchRequest
    actions: List[RuleActionRequest]
    description: NotRequired[str]
    priority: NotRequired[int]
    enabled: NotRequired[bool]
    trigger: NotRequired[str]


class UpdateRuleRequest(TypedDict, total=False):
    """Request body for updating a rule."""

    name: NotRequired[str]
    match: NotRequired[RuleMatchRequest]
    actions: NotRequired[List[RuleActionRequest]]
    description: NotRequired[str]
    priority: NotRequired[int]
    enabled: NotRequired[bool]
    trigger: NotRequired[str]


@dataclass_json
@dataclass
class RuleCondition:
    """A condition in a rule match clause."""

    field: Optional[str] = None
    operator: Optional[str] = None
    value: Optional[Any] = None


@dataclass_json
@dataclass
class RuleMatch:
    """A rule's condition set and matching strategy."""

    operator: Optional[str] = None
    conditions: Optional[List[RuleCondition]] = None


@dataclass_json
@dataclass
class RuleAction:
    """An action applied when a rule matches."""

    type: Optional[str] = None
    value: Optional[str] = None


@dataclass_json
@dataclass
class Rule:
    """A rule used for automated filtering and routing."""

    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[int] = None
    enabled: Optional[bool] = None
    trigger: Optional[str] = None
    match: Optional[RuleMatch] = None
    actions: Optional[List[RuleAction]] = None
    application_id: Optional[str] = None
    organization_id: Optional[str] = None
    created_at: Optional[int] = None
    updated_at: Optional[int] = None


@dataclass_json
@dataclass
class RuleEvaluationInput:
    """Sender data used as input to rule evaluation."""

    from_address: Optional[str] = None
    from_domain: Optional[str] = None
    from_tld: Optional[str] = None


@dataclass_json
@dataclass
class RuleEvaluationAppliedActions:
    """Actions applied when rules matched."""

    blocked: Optional[bool] = None
    marked_as_spam: Optional[bool] = None
    marked_as_read: Optional[bool] = None
    marked_starred: Optional[bool] = None
    archived: Optional[bool] = None
    trashed: Optional[bool] = None
    folder_ids: Optional[List[str]] = None


@dataclass_json
@dataclass
class RuleEvaluation:
    """An audit record describing rule evaluation for a grant."""

    id: Optional[str] = None
    grant_id: Optional[str] = None
    message_id: Optional[str] = None
    evaluated_at: Optional[int] = None
    evaluation_stage: Optional[str] = None
    evaluation_input: Optional[RuleEvaluationInput] = None
    applied_actions: Optional[RuleEvaluationAppliedActions] = None
    matched_rule_ids: Optional[List[str]] = None
    application_id: Optional[str] = None
    organization_id: Optional[str] = None
    created_at: Optional[int] = None
    updated_at: Optional[int] = None

from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import dataclass_json
from typing_extensions import TypedDict, NotRequired


@dataclass_json
@dataclass
class Workspace:
    """
    Class representing a Nylas workspace.

    A workspace (internally a GrantWorkspace) groups grants in a Nylas application
    by email domain. Grants can be auto-grouped (by matching email domain) or
    manually assigned/removed.

    Attributes:
        workspace_id: Globally unique workspace identifier (UUID).
        application_id: The owning Nylas application UUID. Set server-side from the
            API key, never from the request body.
        name: Descriptive workspace name.
        domain: Top-level email domain. May be an empty string when the workspace was
            created with auto_group=false and no domain.
        auto_group: When true, new grants whose email domain matches `domain` are
            automatically assigned to the workspace.
        created_at: Creation timestamp, represented as a Unix timestamp in seconds.
        updated_at: Last-update timestamp, represented as a Unix timestamp in seconds.
        policy_id: Inbox policy attached to the workspace (UUID).
        rules_ids: Inbox rules attached to the workspace (list of UUIDs).
    """

    workspace_id: str
    application_id: str
    name: str
    domain: str
    auto_group: bool
    created_at: int
    updated_at: int
    policy_id: Optional[str] = None
    rules_ids: Optional[List[str]] = None


@dataclass_json
@dataclass
class WorkspaceAutoGroupResponse:
    """
    Class representing the response from starting a workspace auto-group job.

    Attributes:
        job_id: The background job ID (UUID).
        message: A human-readable message describing the started job.
    """

    job_id: str
    message: str


@dataclass_json
@dataclass
class WorkspaceManualAssignResponse:
    """
    Class representing the response from manually assigning/removing grants.

    Attributes:
        application_id: The application owning the workspace (UUID).
        workspace_id: The workspace that was updated (UUID).
        domain: The workspace domain (empty string if none).
        grants_assigned: Grant IDs that were actually assigned. Serializes as `null`
            (deserialized as None) when no assigned grant matched.
        grants_removed: Grant IDs that were actually removed. Serializes as `null`
            (deserialized as None) when no removed grant matched.
    """

    application_id: str
    workspace_id: str
    domain: str
    grants_assigned: Optional[List[str]] = None
    grants_removed: Optional[List[str]] = None


class CreateWorkspaceRequest(TypedDict):
    """
    Class representation of a Nylas create workspace request.

    Attributes:
        name: The descriptive workspace name. Required.
        domain: The top-level email domain to group grants by.
        auto_group: When true, new grants whose email domain matches `domain` are
            auto-assigned. Defaults server-side to true when a domain is provided,
            false otherwise.
        policy_id: Inbox policy to attach to the workspace (UUID).
        rules_ids: Inbox rules to attach to the workspace (list of UUIDs).
    """

    name: str
    domain: NotRequired[str]
    auto_group: NotRequired[bool]
    policy_id: NotRequired[str]
    rules_ids: NotRequired[List[str]]


class UpdateWorkspaceRequest(TypedDict):
    """
    Class representation of a Nylas update workspace request.

    At least one field must be present. The workspace's domain is immutable; sending
    a changed domain is rejected by the API.

    Attributes:
        name: A new non-empty workspace name.
        domain: The workspace domain. Validated but immutable; changing it is rejected.
        auto_group: Whether to auto-group matching grants. Cannot be set to true on a
            workspace with an empty domain.
        policy_id: Inbox policy to attach (UUID). Send `None` to clear, omit to preserve.
        rules_ids: Inbox rules to attach (list of UUIDs). Send a list (including `[]`)
            to overwrite, omit to preserve.
    """

    name: NotRequired[str]
    domain: NotRequired[str]
    auto_group: NotRequired[bool]
    policy_id: NotRequired[Optional[str]]
    rules_ids: NotRequired[Optional[List[str]]]


class WorkspaceAutoGroupRequest(TypedDict):
    """
    Class representation of a Nylas workspace auto-group request.

    All fields are optional.

    Attributes:
        after_created_at: Only group grants created at/after this Unix timestamp.
        invalid_also: When true, includes invalid grants in the grouping pass.
            Defaults to false.
        specific_domain: Only group grants whose email domain matches this domain.
    """

    after_created_at: NotRequired[int]
    invalid_also: NotRequired[bool]
    specific_domain: NotRequired[str]


class WorkspaceManualAssignRequest(TypedDict):
    """
    Class representation of a Nylas workspace manual-assign request.

    At least one of `assign_grants` or `remove_grants` must contain a grant ID.

    Attributes:
        assign_grants: Grant IDs to assign to the workspace. Max 500 entries.
        remove_grants: Grant IDs to remove from the workspace. Max 500 entries.
    """

    assign_grants: NotRequired[List[str]]
    remove_grants: NotRequired[List[str]]

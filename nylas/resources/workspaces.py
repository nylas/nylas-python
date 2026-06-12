from nylas.config import RequestOverrides
from nylas.handler.api_resources import (
    ListableApiResource,
    FindableApiResource,
    CreatableApiResource,
    UpdatablePatchApiResource,
    DestroyableApiResource,
)
from nylas.models.response import Response, ListResponse, DeleteResponse
from nylas.models.workspaces import (
    Workspace,
    WorkspaceAutoGroupResponse,
    WorkspaceManualAssignResponse,
    CreateWorkspaceRequest,
    UpdateWorkspaceRequest,
    WorkspaceAutoGroupRequest,
    WorkspaceManualAssignRequest,
)


class Workspaces(
    ListableApiResource,
    FindableApiResource,
    CreatableApiResource,
    UpdatablePatchApiResource,
    DestroyableApiResource,
):
    """
    Nylas Workspaces API

    The Nylas Workspaces API allows you to group grants in a Nylas application by email
    domain. Grants can be auto-grouped by matching email domain or manually assigned and
    removed.
    """

    def list(self, overrides: RequestOverrides = None) -> ListResponse[Workspace]:
        """
        Return all workspaces for the application.

        Args:
            overrides: The request overrides to apply to the request.

        Returns:
            The list of workspaces.
        """
        return super().list(
            path="/v3/workspaces", response_type=Workspace, overrides=overrides
        )

    def find(
        self, workspace_id: str, overrides: RequestOverrides = None
    ) -> Response[Workspace]:
        """
        Return a workspace.

        Args:
            workspace_id: The ID of the workspace to retrieve. Accepts a UUID or a domain.
            overrides: The request overrides to apply to the request.

        Returns:
            The workspace.
        """
        return super().find(
            path=f"/v3/workspaces/{workspace_id}",
            response_type=Workspace,
            overrides=overrides,
        )

    def create(
        self, request_body: CreateWorkspaceRequest, overrides: RequestOverrides = None
    ) -> Response[Workspace]:
        """
        Create a workspace.

        Args:
            request_body: The values to create the workspace with.
            overrides: The request overrides to apply to the request.

        Returns:
            The created workspace.
        """
        return super().create(
            path="/v3/workspaces",
            request_body=request_body,
            response_type=Workspace,
            overrides=overrides,
        )

    def update(
        self,
        workspace_id: str,
        request_body: UpdateWorkspaceRequest,
        overrides: RequestOverrides = None,
    ) -> Response[Workspace]:
        """
        Update a workspace.

        The Workspaces API only supports updating via PATCH; the workspace must be
        addressed by its UUID (a domain path value is not accepted on update).

        Args:
            workspace_id: The UUID of the workspace to update.
            request_body: The values to update the workspace with.
            overrides: The request overrides to apply to the request.

        Returns:
            The updated workspace.
        """
        return super().patch(
            path=f"/v3/workspaces/{workspace_id}",
            request_body=request_body,
            response_type=Workspace,
            overrides=overrides,
        )

    def destroy(
        self, workspace_id: str, overrides: RequestOverrides = None
    ) -> DeleteResponse:
        """
        Delete a workspace.

        Args:
            workspace_id: The ID of the workspace to delete. Accepts a UUID or a domain.
            overrides: The request overrides to apply to the request.

        Returns:
            The deletion response (request ID only).
        """
        return super().destroy(
            path=f"/v3/workspaces/{workspace_id}", overrides=overrides
        )

    def auto_group(
        self,
        request_body: WorkspaceAutoGroupRequest = None,
        overrides: RequestOverrides = None,
    ) -> Response[WorkspaceAutoGroupResponse]:
        """
        Start a background job that auto-groups grants into workspaces by email domain.

        This endpoint is rate-limited to one call per minute per application.

        Args:
            request_body: Optional filters to scope which grants are grouped.
            overrides: The request overrides to apply to the request.

        Returns:
            The started auto-group job.
        """
        res, headers = self._http_client._execute(
            method="POST",
            path="/v3/workspaces/auto-group",
            request_body=request_body,
            overrides=overrides,
        )
        return Response.from_dict(res, WorkspaceAutoGroupResponse, headers)

    def manual_assign(
        self,
        workspace_id: str,
        request_body: WorkspaceManualAssignRequest,
        overrides: RequestOverrides = None,
    ) -> Response[WorkspaceManualAssignResponse]:
        """
        Manually assign grants to or remove grants from a workspace.

        Args:
            workspace_id: The ID of the workspace. Accepts a UUID or a domain.
            request_body: The grants to assign and/or remove.
            overrides: The request overrides to apply to the request.

        Returns:
            The grants that were assigned and removed.
        """
        res, headers = self._http_client._execute(
            method="POST",
            path=f"/v3/workspaces/{workspace_id}/manual-assign",
            request_body=request_body,
            overrides=overrides,
        )
        return Response.from_dict(res, WorkspaceManualAssignResponse, headers)

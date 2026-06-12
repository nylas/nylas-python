from nylas.models.workspaces import (
    Workspace,
    WorkspaceManualAssignResponse,
)
from nylas.resources.workspaces import Workspaces


class TestWorkspaces:
    def test_workspace_deserialization(self, http_client):
        workspace_json = {
            "workspace_id": "ws-123",
            "application_id": "app-456",
            "name": "Acme Workspace",
            "domain": "acme.com",
            "auto_group": True,
            "default": True,
            "policy_id": "policy-789",
            "rule_ids": ["rule-1", "rule-2"],
            "created_at": 1234567890,
            "updated_at": 1234567899,
        }

        workspace = Workspace.from_dict(workspace_json)

        assert workspace.workspace_id == "ws-123"
        assert workspace.application_id == "app-456"
        assert workspace.name == "Acme Workspace"
        assert workspace.domain == "acme.com"
        assert workspace.auto_group is True
        assert workspace.default is True
        assert workspace.policy_id == "policy-789"
        assert workspace.rule_ids == ["rule-1", "rule-2"]
        assert workspace.created_at == 1234567890
        assert workspace.updated_at == 1234567899

    def test_workspace_deserialization_optional_fields_absent(self, http_client):
        # default / policy_id / rule_ids may be absent; they must default
        # to None rather than raising.
        workspace_json = {
            "workspace_id": "ws-123",
            "application_id": "app-456",
            "name": "Empty Domain Workspace",
            "domain": "",
            "auto_group": False,
            "created_at": 1234567890,
            "updated_at": 1234567899,
        }

        workspace = Workspace.from_dict(workspace_json)

        assert workspace.domain == ""
        assert workspace.auto_group is False
        assert workspace.default is None
        assert workspace.policy_id is None
        assert workspace.rule_ids is None

    def test_manual_assign_response_null_grants(self, http_client):
        # grants_assigned / grants_removed serialize as null when no grant matched;
        # they must deserialize to None, not raise or coerce to [].
        response_json = {
            "application_id": "app-456",
            "workspace_id": "ws-123",
            "domain": "acme.com",
            "grants_assigned": None,
            "grants_removed": None,
        }

        result = WorkspaceManualAssignResponse.from_dict(response_json)

        assert result.application_id == "app-456"
        assert result.workspace_id == "ws-123"
        assert result.domain == "acme.com"
        assert result.grants_assigned is None
        assert result.grants_removed is None

    def test_manual_assign_response_populated_grants(self, http_client):
        response_json = {
            "application_id": "app-456",
            "workspace_id": "ws-123",
            "domain": "acme.com",
            "grants_assigned": ["grant-1"],
            "grants_removed": ["grant-2", "grant-3"],
        }

        result = WorkspaceManualAssignResponse.from_dict(response_json)

        assert result.grants_assigned == ["grant-1"]
        assert result.grants_removed == ["grant-2", "grant-3"]

    def test_list_workspaces(self, http_client_list_response):
        workspaces = Workspaces(http_client_list_response)

        workspaces.list()

        http_client_list_response._execute.assert_called_once_with(
            "GET", "/v3/workspaces", None, None, None, overrides=None
        )

    def test_find_workspace(self, http_client_response):
        workspaces = Workspaces(http_client_response)

        workspaces.find("ws-123")

        http_client_response._execute.assert_called_once_with(
            "GET", "/v3/workspaces/ws-123", None, None, None, overrides=None
        )

    def test_create_workspace(self, http_client_response):
        workspaces = Workspaces(http_client_response)
        request_body = {
            "name": "Acme Workspace",
            "domain": "acme.com",
            "auto_group": True,
            "policy_id": "policy-789",
            "rule_ids": ["rule-1"],
        }

        workspaces.create(request_body=request_body)

        http_client_response._execute.assert_called_once_with(
            "POST", "/v3/workspaces", None, None, request_body, overrides=None
        )

    def test_update_workspace_uses_patch(self, http_client_response):
        # Update must issue PATCH (no PUT route exists) against the workspace UUID.
        workspaces = Workspaces(http_client_response)
        request_body = {"name": "Renamed Workspace"}

        workspaces.update(workspace_id="ws-123", request_body=request_body)

        http_client_response._execute.assert_called_once_with(
            "PATCH", "/v3/workspaces/ws-123", None, None, request_body, overrides=None
        )

    def test_destroy_workspace(self, http_client_delete_response):
        workspaces = Workspaces(http_client_delete_response)

        workspaces.destroy("ws-123")

        http_client_delete_response._execute.assert_called_once_with(
            "DELETE", "/v3/workspaces/ws-123", None, None, None, overrides=None
        )

    def test_auto_group(self, http_client_response):
        workspaces = Workspaces(http_client_response)
        request_body = {
            "after_created_at": 1234567890,
            "invalid_also": True,
            "specific_domain": "acme.com",
        }

        workspaces.auto_group(request_body=request_body)

        http_client_response._execute.assert_called_once_with(
            method="POST",
            path="/v3/workspaces/auto-group",
            request_body=request_body,
            overrides=None,
        )

    def test_auto_group_no_body(self, http_client_response):
        workspaces = Workspaces(http_client_response)

        workspaces.auto_group()

        http_client_response._execute.assert_called_once_with(
            method="POST",
            path="/v3/workspaces/auto-group",
            request_body=None,
            overrides=None,
        )

    def test_manual_assign(self, http_client_response):
        workspaces = Workspaces(http_client_response)
        request_body = {
            "assign_grants": ["grant-1", "grant-2"],
            "remove_grants": ["grant-3"],
        }

        workspaces.manual_assign(workspace_id="ws-123", request_body=request_body)

        http_client_response._execute.assert_called_once_with(
            method="POST",
            path="/v3/workspaces/ws-123/manual-assign",
            request_body=request_body,
            overrides=None,
        )

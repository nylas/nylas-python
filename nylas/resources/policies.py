from nylas.config import RequestOverrides
from nylas.handler.api_resources import (
    CreatableApiResource,
    DestroyableApiResource,
    FindableApiResource,
    ListableApiResource,
    UpdatableApiResource,
)
from nylas.models.policies import (
    CreatePolicyRequest,
    ListPoliciesQueryParams,
    Policy,
    UpdatePolicyRequest,
)
from nylas.models.response import DeleteResponse, ListResponse, Response


class Policies(
    ListableApiResource,
    FindableApiResource,
    CreatableApiResource,
    UpdatableApiResource,
    DestroyableApiResource,
):
    """
    Nylas Policies API.

    Policies define operational configuration for Nylas Agent Accounts.
    """

    def list(
        self,
        query_params: ListPoliciesQueryParams = None,
        overrides: RequestOverrides = None,
    ) -> ListResponse[Policy]:
        return super().list(
            path="/v3/policies",
            response_type=Policy,
            query_params=query_params,
            overrides=overrides,
        )

    def create(
        self,
        request_body: CreatePolicyRequest,
        overrides: RequestOverrides = None,
    ) -> Response[Policy]:
        return super().create(
            path="/v3/policies",
            request_body=request_body,
            response_type=Policy,
            overrides=overrides,
        )

    def find(
        self, policy_id: str, overrides: RequestOverrides = None
    ) -> Response[Policy]:
        return super().find(
            path=f"/v3/policies/{policy_id}",
            response_type=Policy,
            overrides=overrides,
        )

    def update(
        self,
        policy_id: str,
        request_body: UpdatePolicyRequest,
        overrides: RequestOverrides = None,
    ) -> Response[Policy]:
        return super().update(
            path=f"/v3/policies/{policy_id}",
            response_type=Policy,
            request_body=request_body,
            method="PUT",
            overrides=overrides,
        )

    def destroy(
        self, policy_id: str, overrides: RequestOverrides = None
    ) -> DeleteResponse:
        return super().destroy(path=f"/v3/policies/{policy_id}", overrides=overrides)

from nylas.config import RequestOverrides
from nylas.handler.api_resources import (
    CreatableApiResource,
    DestroyableApiResource,
    FindableApiResource,
    ListableApiResource,
    UpdatableApiResource,
)
from nylas.models.response import DeleteResponse, ListResponse, Response
from nylas.models.rules import (
    CreateRuleRequest,
    ListRuleEvaluationsQueryParams,
    ListRulesQueryParams,
    Rule,
    RuleEvaluation,
    UpdateRuleRequest,
)


class Rules(
    ListableApiResource,
    FindableApiResource,
    CreatableApiResource,
    UpdatableApiResource,
    DestroyableApiResource,
):
    """Nylas Rules API."""

    def list(
        self,
        query_params: ListRulesQueryParams = None,
        overrides: RequestOverrides = None,
    ) -> ListResponse[Rule]:
        return super().list(
            path="/v3/rules",
            response_type=Rule,
            query_params=query_params,
            overrides=overrides,
        )

    def create(
        self,
        request_body: CreateRuleRequest,
        overrides: RequestOverrides = None,
    ) -> Response[Rule]:
        return super().create(
            path="/v3/rules",
            request_body=request_body,
            response_type=Rule,
            overrides=overrides,
        )

    def find(self, rule_id: str, overrides: RequestOverrides = None) -> Response[Rule]:
        return super().find(
            path=f"/v3/rules/{rule_id}",
            response_type=Rule,
            overrides=overrides,
        )

    def update(
        self,
        rule_id: str,
        request_body: UpdateRuleRequest,
        overrides: RequestOverrides = None,
    ) -> Response[Rule]:
        return super().update(
            path=f"/v3/rules/{rule_id}",
            response_type=Rule,
            request_body=request_body,
            method="PUT",
            overrides=overrides,
        )

    def destroy(self, rule_id: str, overrides: RequestOverrides = None) -> DeleteResponse:
        return super().destroy(path=f"/v3/rules/{rule_id}", overrides=overrides)

    def list_evaluations(
        self,
        grant_id: str,
        query_params: ListRuleEvaluationsQueryParams = None,
        overrides: RequestOverrides = None,
    ) -> ListResponse[RuleEvaluation]:
        return super().list(
            path=f"/v3/grants/{grant_id}/rule-evaluations",
            response_type=RuleEvaluation,
            query_params=query_params,
            overrides=overrides,
        )

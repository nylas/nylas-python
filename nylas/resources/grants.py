from nylas.handler.api_resources import (
    ListableApiResource,
    FindableApiResource,
    CreatableApiResource,
    UpdatableApiResource,
    DestroyableApiResource,
)
from nylas.models.delete_response import DeleteResponse
from nylas.models.grant import (
    Grant,
    ListGrantsQueryParams,
    CreateGrantRequest,
    UpdateGrantRequest,
)
from nylas.models.list_response import ListResponse
from nylas.models.response import Response


class Grants(
    ListableApiResource,
    FindableApiResource,
    CreatableApiResource,
    UpdatableApiResource,
    DestroyableApiResource,
):
    def list(self, query_params: ListGrantsQueryParams) -> ListResponse[Grant]:
        return super(Grants, self).list(
            path=f"/v3/grants", response_type=Grant, query_params=query_params
        )

    def find(self, grant_id: str) -> Response[Grant]:
        return super(Grants, self).find(
            path=f"/v3/grants/{grant_id}", response_type=Grant
        )

    def create(self, request_body: CreateGrantRequest) -> Response[Grant]:
        return super(Grants, self).create(
            path=f"/v3/grants", response_type=Grant, request_body=request_body
        )

    def update(
        self, grant_id: str, request_body: UpdateGrantRequest
    ) -> Response[Grant]:
        return super(Grants, self).update(
            path=f"/v3/grants/{grant_id}",
            response_type=Grant,
            request_body=request_body,
        )

    def destroy(self, grant_id: str) -> DeleteResponse:
        return super(Grants, self).destroy(path=f"/v3/grants/{grant_id}")

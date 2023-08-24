from nylas.handler.api_resources import (
    ListableApiResource,
    FindableApiResource,
    CreatableApiResource,
    UpdatableApiResource,
    DestroyableApiResource,
)
from nylas.models.delete_response import DeleteResponse
from nylas.models.grant import Grant
from nylas.models.list_response import ListResponse
from nylas.models.response import Response


class Grants(
    ListableApiResource[Grant],
    FindableApiResource[Grant],
    CreatableApiResource[Grant],
    UpdatableApiResource[Grant],
    DestroyableApiResource,
):
    def __init__(self, http_client):
        super(Grants, self).__init__("grants", http_client)

    def list(self, query_params: dict) -> ListResponse[Grant]:
        return super(Grants, self).list(path=f"/v3/grants", query_params=query_params)

    def find(self, grant_id: str) -> Response[Grant]:
        return super(Grants, self).find(path=f"/v3/grants/{grant_id}")

    def create(self, request_body: dict) -> Response[Grant]:
        return super(Grants, self).create(path=f"/v3/grants", request_body=request_body)

    def update(self, grant_id: str, request_body: dict) -> Response[Grant]:
        return super(Grants, self).update(
            path=f"/v3/grants/{grant_id}", request_body=request_body
        )

    def destroy(self, grant_id: str) -> DeleteResponse:
        return super(Grants, self).destroy(path=f"/v3/grants/{grant_id}")

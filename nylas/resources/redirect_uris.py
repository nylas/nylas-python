from nylas.handler.api_resources import (
    ListableApiResource,
    FindableApiResource,
    CreatableApiResource,
    UpdatableApiResource,
    DestroyableApiResource,
)
from nylas.models.delete_response import DeleteResponse
from nylas.models.list_response import ListResponse
from nylas.models.reditect_uri import RedirectUri
from nylas.models.response import Response


class RedirectUris(
    ListableApiResource[RedirectUri],
    FindableApiResource[RedirectUri],
    CreatableApiResource[RedirectUri],
    UpdatableApiResource[RedirectUri],
    DestroyableApiResource,
):
    def __init__(self, http_client):
        super(RedirectUris, self).__init__("redirect-uris", http_client)

    def list(self) -> ListResponse[RedirectUri]:
        return super(RedirectUris, self).list(path=f"/v3/redirect-uris")

    def find(self, redirect_uri_id: str) -> Response[RedirectUri]:
        return super(RedirectUris, self).find(
            path=f"/v3/redirect-uris/{redirect_uri_id}"
        )

    def create(self, request_body: dict) -> Response[RedirectUri]:
        return super(RedirectUris, self).create(
            path=f"/v3/redirect-uris", request_body=request_body
        )

    def update(self, redirect_uri_id: str, request_body: dict) -> Response[RedirectUri]:
        return super(RedirectUris, self).update(
            path=f"/v3/redirect-uris/{redirect_uri_id}", request_body=request_body
        )

    def destroy(self, redirect_uri_id: str) -> DeleteResponse:
        return super(RedirectUris, self).destroy(
            path=f"/v3/redirect-uris/{redirect_uri_id}"
        )

from nylas.handler.api_resources import (
    ListableApiResource,
    FindableApiResource,
    CreatableApiResource,
    UpdatableApiResource,
    DestroyableApiResource,
)
from nylas.models.delete_response import DeleteResponse
from nylas.models.list_response import ListResponse
from nylas.models.reditect_uri import (
    RedirectUri,
    CreateRedirectUriRequest,
    UpdateRedirectUriRequest,
)
from nylas.models.response import Response


class RedirectUris(
    ListableApiResource,
    FindableApiResource,
    CreatableApiResource,
    UpdatableApiResource,
    DestroyableApiResource,
):
    def list(self) -> ListResponse[RedirectUri]:
        return super(RedirectUris, self).list(
            path=f"/v3/redirect-uris", response_type=RedirectUri
        )

    def find(self, redirect_uri_id: str) -> Response[RedirectUri]:
        return super(RedirectUris, self).find(
            path=f"/v3/redirect-uris/{redirect_uri_id}",
            response_type=RedirectUri,
        )

    def create(self, request_body: CreateRedirectUriRequest) -> Response[RedirectUri]:
        return super(RedirectUris, self).create(
            path=f"/v3/redirect-uris",
            request_body=request_body,
            response_type=RedirectUri,
        )

    def update(
        self, redirect_uri_id: str, request_body: UpdateRedirectUriRequest
    ) -> Response[RedirectUri]:
        return super(RedirectUris, self).update(
            path=f"/v3/redirect-uris/{redirect_uri_id}",
            request_body=request_body,
            response_type=RedirectUri,
        )

    def destroy(self, redirect_uri_id: str) -> DeleteResponse:
        return super(RedirectUris, self).destroy(
            path=f"/v3/redirect-uris/{redirect_uri_id}"
        )

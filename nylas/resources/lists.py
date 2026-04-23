from nylas.config import RequestOverrides
from nylas.handler.api_resources import (
    CreatableApiResource,
    DestroyableApiResource,
    FindableApiResource,
    ListableApiResource,
    UpdatableApiResource,
)
from nylas.models.lists import (
    CreateListRequest,
    ListItem,
    ListListItemsQueryParams,
    ListListsQueryParams,
    NylasList,
    UpdateListItemsRequest,
    UpdateListRequest,
)
from nylas.models.response import DeleteResponse, ListResponse, Response


class Lists(
    ListableApiResource,
    FindableApiResource,
    CreatableApiResource,
    UpdatableApiResource,
    DestroyableApiResource,
):
    """Nylas Lists API."""

    def list(
        self,
        query_params: ListListsQueryParams = None,
        overrides: RequestOverrides = None,
    ) -> ListResponse[NylasList]:
        """Return all lists for the application."""
        return super().list(
            path="/v3/lists",
            response_type=NylasList,
            query_params=query_params,
            overrides=overrides,
        )

    def create(
        self,
        request_body: CreateListRequest,
        overrides: RequestOverrides = None,
    ) -> Response[NylasList]:
        """Create a new list."""
        return super().create(
            path="/v3/lists",
            request_body=request_body,
            response_type=NylasList,
            overrides=overrides,
        )

    def find(self, list_id: str, overrides: RequestOverrides = None) -> Response[NylasList]:
        """Return a specific list by ID."""
        return super().find(
            path=f"/v3/lists/{list_id}",
            response_type=NylasList,
            overrides=overrides,
        )

    def update(
        self,
        list_id: str,
        request_body: UpdateListRequest,
        overrides: RequestOverrides = None,
    ) -> Response[NylasList]:
        """Update a list by ID."""
        return super().update(
            path=f"/v3/lists/{list_id}",
            response_type=NylasList,
            request_body=request_body,
            method="PUT",
            overrides=overrides,
        )

    def destroy(self, list_id: str, overrides: RequestOverrides = None) -> DeleteResponse:
        """Delete a list by ID."""
        return super().destroy(path=f"/v3/lists/{list_id}", overrides=overrides)

    def list_items(
        self,
        list_id: str,
        query_params: ListListItemsQueryParams = None,
        overrides: RequestOverrides = None,
    ) -> ListResponse[ListItem]:
        """Return all items in a list."""
        return super().list(
            path=f"/v3/lists/{list_id}/items",
            response_type=ListItem,
            query_params=query_params,
            overrides=overrides,
        )

    def add_items(
        self,
        list_id: str,
        request_body: UpdateListItemsRequest,
        overrides: RequestOverrides = None,
    ) -> Response[NylasList]:
        """Add items to a list."""
        return super().create(
            path=f"/v3/lists/{list_id}/items",
            request_body=request_body,
            response_type=NylasList,
            overrides=overrides,
        )

    def remove_items(
        self,
        list_id: str,
        request_body: UpdateListItemsRequest,
        overrides: RequestOverrides = None,
    ) -> Response[NylasList]:
        """Remove items from a list."""
        json_response, headers = self._http_client._execute(
            "DELETE",
            f"/v3/lists/{list_id}/items",
            None,
            None,
            request_body,
            overrides=overrides,
        )
        return Response.from_dict(json_response, NylasList, headers)

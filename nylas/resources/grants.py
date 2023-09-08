from nylas.handler.api_resources import (
    ListableApiResource,
    FindableApiResource,
    CreatableApiResource,
    UpdatableApiResource,
    DestroyableApiResource,
)
from nylas.models.grants import (
    Grant,
    ListGrantsQueryParams,
    CreateGrantRequest,
    UpdateGrantRequest,
)
from nylas.models.response import Response, ListResponse, DeleteResponse


class Grants(
    ListableApiResource,
    FindableApiResource,
    CreatableApiResource,
    UpdatableApiResource,
    DestroyableApiResource,
):
    def list(self, query_params: ListGrantsQueryParams) -> ListResponse[Grant]:
        """
        Return all Grants.

        Args:
            query_params: The query parameters to include in the request.

        Returns:
            A list of Grants.
        """

        return super(Grants, self).list(
            path=f"/v3/grants", response_type=Grant, query_params=query_params
        )

    def find(self, grant_id: str) -> Response[Grant]:
        """
        Return a Grant.

        Args:
            grant_id: The ID of the Grant to retrieve.

        Returns:
            The Grant.
        """

        return super(Grants, self).find(
            path=f"/v3/grants/{grant_id}", response_type=Grant
        )

    def create(self, request_body: CreateGrantRequest) -> Response[Grant]:
        """
        Create a Grant.

        Args:
            request_body: The values to create the Grant with.

        Returns:
            The created Grant.
        """

        return super(Grants, self).create(
            path=f"/v3/grants", response_type=Grant, request_body=request_body
        )

    def update(
        self, grant_id: str, request_body: UpdateGrantRequest
    ) -> Response[Grant]:
        """
        Update a Grant.

        Args:
            grant_id: The ID of the Grant to update.
            request_body: The values to update the Grant with.

        Returns:
            The updated Grant.
        """

        return super(Grants, self).update(
            path=f"/v3/grants/{grant_id}",
            response_type=Grant,
            request_body=request_body,
        )

    def destroy(self, grant_id: str) -> DeleteResponse:
        """
        Delete a Grant.

        Args:
            grant_id: The ID of the Grant to delete.

        Returns:
            The deletion response.
        """

        return super(Grants, self).destroy(path=f"/v3/grants/{grant_id}")

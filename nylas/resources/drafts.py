from typing import Optional

from nylas.handler.api_resources import (
    ListableApiResource,
    FindableApiResource,
    UpdatableApiResource,
    DestroyableApiResource,
)
from nylas.models.drafts import ListDraftsQueryParams, Draft, UpdateDraftRequest
from nylas.models.response import ListResponse, Response, DeleteResponse


class Drafts(
    ListableApiResource,
    FindableApiResource,
    UpdatableApiResource,
    DestroyableApiResource,
):
    def list(
        self, identifier: str, query_params: Optional[ListDraftsQueryParams] = None
    ) -> ListResponse[Draft]:
        """
        Return all Drafts.

        Args:
            identifier: The identifier of the grant to get drafts for.
            query_params: The query parameters to filter drafts by.

        Returns:
            A list of Drafts.
        """
        return super(Drafts, self).list(
            path=f"/v3/grants/{identifier}/drafts",
            response_type=Draft,
            query_params=query_params,
        )

    def find(
        self,
        identifier: str,
        draft_id: str,
    ) -> Response[Draft]:
        """
        Return a Draft.

        Args:
            identifier: The identifier of the grant to get the draft for.
            draft_id: The identifier of the draft to get.

        Returns:
            The requested Draft.
        """
        return super(Drafts, self).find(
            path=f"/v3/grants/{identifier}/drafts/{draft_id}",
            response_type=Draft,
        )

    def update(
        self,
        identifier: str,
        draft_id: str,
        request_body: UpdateDraftRequest,
    ) -> Response[Draft]:
        """
        Update a Draft.

        Args:
            identifier: The identifier of the grant to update the draft for.
            draft_id: The identifier of the draft to update.
            request_body: The request body to update the draft with.

        Returns:
            The updated Draft.
        """
        return super(Drafts, self).update(
            path=f"/v3/grants/{identifier}/drafts/{draft_id}",
            response_type=Draft,
            request_body=request_body,
        )

    def destroy(self, identifier: str, draft_id: str) -> DeleteResponse:
        """
        Delete a Draft.

        Args:
            identifier: The identifier of the grant to delete the draft for.
            draft_id: The identifier of the draft to delete.

        Returns:
            The deletion response.
        """
        return super(Drafts, self).destroy(
            path=f"/v3/grants/{identifier}/drafts/{draft_id}",
        )

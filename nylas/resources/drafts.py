from typing import Optional

from nylas.handler.api_resources import (
    ListableApiResource,
    FindableApiResource,
    UpdatableApiResource,
    DestroyableApiResource,
    CreatableApiResource,
)
from nylas.models.drafts import (
    ListDraftsQueryParams,
    Draft,
    UpdateDraftRequest,
    CreateDraftRequest,
)
from nylas.models.response import ListResponse, Response, DeleteResponse
from nylas.utils.file_utils import _build_form_request


class Drafts(
    ListableApiResource,
    FindableApiResource,
    CreatableApiResource,
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

    def create(
        self, identifier: str, request_body: CreateDraftRequest
    ) -> Response[Draft]:
        """
        Create a Draft.

        Args:
            identifier: The identifier of the grant to send the message for.
            request_body: The request body to create a draft with.

        Returns:
            The newly created Draft.
        """
        json_response = self._http_client._execute(
            method="POST",
            path=f"/v3/grants/{identifier}/drafts",
            data=_build_form_request(request_body),
        )

        return Response.from_dict(json_response, Draft)

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
        json_response = self._http_client._execute(
            method="PUT",
            path=f"/v3/grants/{identifier}/drafts/{draft_id}",
            data=_build_form_request(request_body),
        )

        return Response.from_dict(json_response, Draft)

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

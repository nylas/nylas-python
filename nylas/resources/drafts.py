import io
import urllib.parse
from typing import Optional

from nylas.config import RequestOverrides
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
    FindDraftQueryParams,
)
from nylas.models.messages import Message
from nylas.models.response import ListResponse, Response, DeleteResponse
from nylas.utils.file_utils import (
    _build_form_request,
    MAXIMUM_JSON_ATTACHMENT_SIZE,
    encode_stream_to_base64,
)


class Drafts(
    ListableApiResource,
    FindableApiResource,
    CreatableApiResource,
    UpdatableApiResource,
    DestroyableApiResource,
):
    """
    Nylas Draft API

    The Drafts API allows you to create, read, update, and delete drafts and send them as messages.
    """

    def list(
        self,
        identifier: str,
        query_params: Optional[ListDraftsQueryParams] = None,
        overrides: RequestOverrides = None,
    ) -> ListResponse[Draft]:
        """
        Return all Drafts.

        Args:
            identifier: The identifier of the grant to get drafts for.
            query_params: The query parameters to filter drafts by.
            overrides: The request overrides to use for the request.

        Returns:
            A list of Drafts.
        """
        return super().list(
            path=f"/v3/grants/{identifier}/drafts",
            response_type=Draft,
            query_params=query_params,
            overrides=overrides,
        )

    def find(
        self,
        identifier: str,
        draft_id: str,
        overrides: RequestOverrides = None,
        query_params: FindDraftQueryParams = None,
    ) -> Response[Draft]:
        """
        Return a Draft.

        Args:
            identifier: The identifier of the grant to get the draft for.
            draft_id: The identifier of the draft to get.
            overrides: The request overrides to use for the request.
            query_params: The query parameters to include in the request.

        Returns:
            The requested Draft.
        """
        return super().find(
            path=f"/v3/grants/{identifier}/drafts/{urllib.parse.quote(draft_id, safe='')}",
            response_type=Draft,
            query_params=query_params,
            overrides=overrides,
        )

    def create(
        self,
        identifier: str,
        request_body: CreateDraftRequest,
        overrides: RequestOverrides = None,
    ) -> Response[Draft]:
        """
        Create a Draft.

        Args:
            identifier: The identifier of the grant to send the message for.
            request_body: The request body to create a draft with.
            overrides: The request overrides to use for the request.

        Returns:
            The newly created Draft.
        """
        path = f"/v3/grants/{identifier}/drafts"

        # Use form data only if the attachment size is greater than 3mb
        attachment_size = sum(
            attachment.get("size", 0)
            for attachment in request_body.get("attachments", [])
        )
        if attachment_size >= MAXIMUM_JSON_ATTACHMENT_SIZE:
            json_response = self._http_client._execute(
                method="POST",
                path=path,
                data=_build_form_request(request_body),
                overrides=overrides,
            )

            return Response.from_dict(json_response, Draft)

        # Encode the content of the attachments to base64
        for attachment in request_body.get("attachments", []):
            if issubclass(type(attachment["content"]), io.IOBase):
                attachment["content"] = encode_stream_to_base64(attachment["content"])

        return super().create(
            path=path,
            response_type=Draft,
            request_body=request_body,
            overrides=overrides,
        )

    def update(
        self,
        identifier: str,
        draft_id: str,
        request_body: UpdateDraftRequest,
        overrides: RequestOverrides = None,
    ) -> Response[Draft]:
        """
        Update a Draft.

        Args:
            identifier: The identifier of the grant to update the draft for.
            draft_id: The identifier of the draft to update.
            request_body: The request body to update the draft with.
            overrides: The request overrides to use for the request.

        Returns:
            The updated Draft.
        """
        path = f"/v3/grants/{identifier}/drafts/{urllib.parse.quote(draft_id, safe='')}"

        # Use form data only if the attachment size is greater than 3mb
        attachment_size = sum(
            attachment.get("size", 0)
            for attachment in request_body.get("attachments", [])
        )
        if attachment_size >= MAXIMUM_JSON_ATTACHMENT_SIZE:
            json_response = self._http_client._execute(
                method="PUT",
                path=path,
                data=_build_form_request(request_body),
                overrides=overrides,
            )

            return Response.from_dict(json_response, Draft)

        # Encode the content of the attachments to base64
        for attachment in request_body.get("attachments", []):
            if issubclass(type(attachment["content"]), io.IOBase):
                attachment["content"] = encode_stream_to_base64(attachment["content"])

        return super().update(
            path=path,
            response_type=Draft,
            request_body=request_body,
            overrides=overrides,
        )

    def destroy(
        self,
        identifier: str,
        draft_id: str,
        overrides: RequestOverrides = None,
    ) -> DeleteResponse:
        """
        Delete a Draft.

        Args:
            identifier: The identifier of the grant to delete the draft for.
            draft_id: The identifier of the draft to delete.
            overrides: The request overrides to use for the request.

        Returns:
            The deletion response.
        """
        return super().destroy(
            path=f"/v3/grants/{identifier}/drafts/{urllib.parse.quote(draft_id, safe='')}",
            overrides=overrides,
        )

    def send(
        self,
        identifier: str,
        draft_id: str,
        overrides: RequestOverrides = None,
    ) -> Response[Message]:
        """
        Send a Draft.

        Args:
            identifier: The identifier of the grant to send the draft for.
            draft_id: The identifier of the draft to send.
            overrides: The request overrides to use for the request.
        """
        json_response, headers = self._http_client._execute(
            method="POST",
            path=f"/v3/grants/{identifier}/drafts/{urllib.parse.quote(draft_id, safe='')}",
            overrides=overrides,
        )

        return Response.from_dict(json_response, Message, headers)

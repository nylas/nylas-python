from typing import Optional

from nylas.config import RequestOverrides
from nylas.handler.api_resources import (CreatableApiResource,
                                         DestroyableApiResource,
                                         FindableApiResource,
                                         ListableApiResource,
                                         UpdatablePatchApiResource)
from nylas.models.notetakers import (FindNotetakerQueryParams,
                                     InviteNotetakerRequest,
                                     ListNotetakerQueryParams,
                                     Notetaker, NotetakerMedia,
                                     NotetakerLeaveResponse,
                                     UpdateNotetakerRequest)
from nylas.models.response import DeleteResponse, ListResponse, Response


class Notetakers(
    ListableApiResource,
    FindableApiResource,
    CreatableApiResource,
    UpdatablePatchApiResource,
    DestroyableApiResource,
):
    """
    Nylas Notetakers API

    The Nylas Notetakers API allows you to invite Notetaker bots to meetings and manage their status.
    Notetaker states are represented by the NotetakerState enum, and meeting providers by the MeetingProvider enum.
    """

    def list(
        self,
        identifier: str = None,
        query_params: Optional[ListNotetakerQueryParams] = None,
        overrides: RequestOverrides = None,
    ) -> ListResponse[Notetaker]:
        """
        Return all Notetakers.

        Args:
            identifier: The identifier of the Grant to act upon. Optional.
            query_params: The query parameters to include in the request.
                You can use NotetakerState enum values for the state parameter:
                e.g., {"state": NotetakerState.SCHEDULED.value}
            overrides: The request overrides to use.

        Returns:
            The list of Notetakers.
        """
        path = (
            "/v3/notetakers"
            if identifier is None
            else f"/v3/grants/{identifier}/notetakers"
        )
        return super().list(
            path=path,
            response_type=Notetaker,
            query_params=query_params,
            overrides=overrides,
        )

    def find(
        self,
        notetaker_id: str,
        identifier: str = None,
        overrides: RequestOverrides = None,
        query_params: FindNotetakerQueryParams = None,
    ) -> Response[Notetaker]:
        """
        Return a Notetaker.

        Args:
            notetaker_id: The ID of the Notetaker to retrieve.
            identifier: The identifier of the Grant to act upon. Optional.
            overrides: The request overrides to use.
            query_params: The query parameters to include in the request.

        Returns:
            The Notetaker with properties like state (NotetakerState) and meeting_provider (MeetingProvider).
        """
        path = (
            f"/v3/notetakers/{notetaker_id}"
            if identifier is None
            else f"/v3/grants/{identifier}/notetakers/{notetaker_id}"
        )
        return super().find(
            path=path,
            response_type=Notetaker,
            query_params=query_params,
            overrides=overrides,
        )

    def invite(
        self,
        request_body: InviteNotetakerRequest,
        identifier: str = None,
        overrides: RequestOverrides = None,
    ) -> Response[Notetaker]:
        """
        Invite a Notetaker to a meeting.

        Args:
            request_body: The values to create the Notetaker with.
            identifier: The identifier of the Grant to act upon. Optional.
            overrides: The request overrides to use.

        Returns:
            The created Notetaker with state set to NotetakerState.SCHEDULED.
        """
        path = (
            "/v3/notetakers"
            if identifier is None
            else f"/v3/grants/{identifier}/notetakers"
        )
        return super().create(
            path=path,
            response_type=Notetaker,
            request_body=request_body,
            overrides=overrides,
        )

    def update(
        self,
        notetaker_id: str,
        request_body: UpdateNotetakerRequest,
        identifier: str = None,
        overrides: RequestOverrides = None,
    ) -> Response[Notetaker]:
        """
        Update a Notetaker.

        Args:
            notetaker_id: The ID of the Notetaker to update.
            request_body: The values to update the Notetaker with.
            identifier: The identifier of the Grant to act upon. Optional.
            overrides: The request overrides to use.

        Returns:
            The updated Notetaker.
        """
        path = (
            f"/v3/notetakers/{notetaker_id}"
            if identifier is None
            else f"/v3/grants/{identifier}/notetakers/{notetaker_id}"
        )
        return super().patch(
            path=path,
            response_type=Notetaker,
            request_body=request_body,
            overrides=overrides,
        )

    def leave(
        self,
        notetaker_id: str,
        identifier: str = None,
        overrides: RequestOverrides = None,
    ) -> Response[NotetakerLeaveResponse]:
        """
        Remove Notetaker from a meeting.

        Args:
            notetaker_id: The ID of the Notetaker to remove from the meeting.
            identifier: The identifier of the Grant to act upon. Optional.
            overrides: The request overrides to use.

        Returns:
            The response with information about the Notetaker that left,
            including the Notetaker ID and a message.
        """
        path = (
            f"/v3/notetakers/{notetaker_id}/leave"
            if identifier is None
            else f"/v3/grants/{identifier}/notetakers/{notetaker_id}/leave"
        )
        return super().create(
            path=path,
            response_type=NotetakerLeaveResponse,
            overrides=overrides,
        )

    def get_media(
        self,
        notetaker_id: str,
        identifier: str = None,
        overrides: RequestOverrides = None,
    ) -> Response[NotetakerMedia]:
        """
        Download Notetaker media.

        Args:
            notetaker_id: The ID of the Notetaker to get media from.
            identifier: The identifier of the Grant to act upon. Optional.
            overrides: The request overrides to use.

        Returns:
            The Notetaker media information including URLs for recordings and transcripts.
        """
        path = (
            f"/v3/notetakers/{notetaker_id}/media"
            if identifier is None
            else f"/v3/grants/{identifier}/notetakers/{notetaker_id}/media"
        )
        return super().find(
            path=path,
            response_type=NotetakerMedia,
            overrides=overrides,
        )

    def cancel(
        self,
        notetaker_id: str,
        identifier: str = None,
        overrides: RequestOverrides = None,
    ) -> DeleteResponse:
        """
        Cancel a scheduled Notetaker.

        Args:
            notetaker_id: The ID of the Notetaker to cancel.
            identifier: The identifier of the Grant to act upon. Optional.
            overrides: The request overrides to use.

        Returns:
            The deletion response.
        """
        path = (
            f"/v3/notetakers/{notetaker_id}/cancel"
            if identifier is None
            else f"/v3/grants/{identifier}/notetakers/{notetaker_id}/cancel"
        )
        return super().destroy(
            path=path,
            overrides=overrides,
        )

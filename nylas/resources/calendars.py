from typing import List

from nylas.config import RequestOverrides
from nylas.handler.api_resources import (
    ListableApiResource,
    FindableApiResource,
    CreatableApiResource,
    UpdatableApiResource,
    DestroyableApiResource,
)
from nylas.models.availability import GetAvailabilityResponse, GetAvailabilityRequest
from nylas.models.free_busy import (
    GetFreeBusyResponse,
    GetFreeBusyRequest,
    FreeBusyError,
    FreeBusy,
)
from nylas.models.calendars import (
    Calendar,
    CreateCalendarRequest,
    UpdateCalendarRequest,
    ListCalendarsQueryParams,
    FindCalendarQueryParams,
)
from nylas.models.response import Response, ListResponse, DeleteResponse


class Calendars(
    ListableApiResource,
    FindableApiResource,
    CreatableApiResource,
    UpdatableApiResource,
    DestroyableApiResource,
):
    """
    Nylas Calendar API

    The Nylas calendar API allows you to create new calendars or manage existing ones, as well as getting
    free/busy information for a calendar and getting availability for a calendar.

    A calendar can be accessed by one, or several people, and can contain events.
    """

    def list(
        self,
        identifier: str,
        query_params: ListCalendarsQueryParams = None,
        overrides: RequestOverrides = None,
    ) -> ListResponse[Calendar]:
        """
        Return all Calendars.

        Args:
            identifier: The identifier of the Grant to act upon.
            query_params: The query parameters to include in the request.
            overrides: The request overrides to use for the request.

        Returns:
            The list of Calendars.
        """

        return super().list(
            path=f"/v3/grants/{identifier}/calendars",
            query_params=query_params,
            response_type=Calendar,
            overrides=overrides,
        )

    def find(
        self,
        identifier: str,
        calendar_id: str,
        overrides: RequestOverrides = None,
        query_params: FindCalendarQueryParams = None,
    ) -> Response[Calendar]:
        """
        Return a Calendar.

        Args:
            identifier: The identifier of the Grant to act upon.
            calendar_id: The ID of the Calendar to retrieve.
                Use "primary" to refer to the primary Calendar associated with the Grant.
            overrides: The request overrides to use for the request.
            query_params: The query parameters to include in the request.

        Returns:
            The Calendar.
        """
        return super().find(
            path=f"/v3/grants/{identifier}/calendars/{calendar_id}",
            response_type=Calendar,
            query_params=query_params,
            overrides=overrides,
        )

    def create(
        self,
        identifier: str,
        request_body: CreateCalendarRequest,
        overrides: RequestOverrides = None,
    ) -> Response[Calendar]:
        """
        Create a Calendar.

        Args:
            identifier: The identifier of the Grant to act upon.
            request_body: The values to create the Calendar with.
            overrides: The request overrides to use for the request.

        Returns:
            The created Calendar.
        """
        return super().create(
            path=f"/v3/grants/{identifier}/calendars",
            response_type=Calendar,
            request_body=request_body,
            overrides=overrides,
        )

    def update(
        self,
        identifier: str,
        calendar_id: str,
        request_body: UpdateCalendarRequest,
        overrides: RequestOverrides = None,
    ) -> Response[Calendar]:
        """
        Update a Calendar.

        Args:
            identifier: The identifier of the Grant to act upon.
            calendar_id: The ID of the Calendar to update.
                Use "primary" to refer to the primary Calendar associated with the Grant.
            request_body: The values to update the Calendar with.
            overrides: The request overrides to use for the request.

        Returns:
            The updated Calendar.
        """
        return super().update(
            path=f"/v3/grants/{identifier}/calendars/{calendar_id}",
            response_type=Calendar,
            request_body=request_body,
            overrides=overrides,
        )

    def destroy(
        self, identifier: str, calendar_id: str, overrides: RequestOverrides = None
    ) -> DeleteResponse:
        """
        Delete a Calendar.

        Args:
            identifier: The identifier of the Grant to act upon.
            calendar_id: The ID of the Calendar to delete.
                Use "primary" to refer to the primary Calendar associated with the Grant.
            overrides: The request overrides to use for the request.

        Returns:
            The deletion response.
        """
        return super().destroy(
            path=f"/v3/grants/{identifier}/calendars/{calendar_id}", overrides=overrides
        )

    def get_availability(
        self, request_body: GetAvailabilityRequest, overrides: RequestOverrides = None
    ) -> Response[GetAvailabilityResponse]:
        """
        Get availability for a Calendar.

        Args:
            request_body: The request body to send to the API.
            overrides: The request overrides to use for the request.

        Returns:
            Response: The availability response from the API.
        """
        json_response, headers = self._http_client._execute(
            method="POST",
            path="/v3/calendars/availability",
            request_body=request_body,
            overrides=overrides,
        )

        return Response.from_dict(json_response, GetAvailabilityResponse, headers)

    def get_free_busy(
        self,
        identifier: str,
        request_body: GetFreeBusyRequest,
        overrides: RequestOverrides = None,
    ) -> Response[List[GetFreeBusyResponse]]:
        """
        Get free/busy info for a Calendar.

        Args:
            identifier: The grant ID or email account to get free/busy for.
            request_body: The request body to send to the API.
            overrides: The request overrides to use for the request.

        Returns:
            Response: The free/busy response from the API.
        """
        json_response, headers = self._http_client._execute(
            method="POST",
            path=f"/v3/grants/{identifier}/calendars/free-busy",
            request_body=request_body,
            overrides=overrides,
        )

        data = []
        request_id = json_response["request_id"]
        for item in json_response["data"]:
            if item.get("object") == "error":
                data.append(FreeBusyError.from_dict(item))
            else:
                data.append(FreeBusy.from_dict(item))

        return Response(data, request_id, headers)

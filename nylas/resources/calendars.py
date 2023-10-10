from nylas.handler.api_resources import (
    ListableApiResource,
    FindableApiResource,
    CreatableApiResource,
    UpdatableApiResource,
    DestroyableApiResource,
)
from nylas.models.availability import GetAvailabilityResponse, GetAvailabilityRequest
from nylas.models.free_busy import GetFreeBusyResponse, GetFreeBusyRequest
from nylas.models.calendars import (
    Calendar,
    CreateCalendarRequest,
    UpdateCalendarRequest,
    ListCalendersQueryParams,
)
from nylas.models.response import Response, ListResponse, DeleteResponse


class Calendars(
    ListableApiResource,
    FindableApiResource,
    CreatableApiResource,
    UpdatableApiResource,
    DestroyableApiResource,
):
    def list(
        self, identifier: str, query_params: ListCalendersQueryParams = None
    ) -> ListResponse[Calendar]:
        """
        Return all Calendars.

        Args:
            identifier: The identifier of the Grant to act upon.
            query_params: The query parameters to include in the request.

        Returns:
            The list of Calendars.
        """

        return super(Calendars, self).list(
            path=f"/v3/grants/{identifier}/calendars",
            query_params=query_params,
            response_type=Calendar,
        )

    def find(self, identifier: str, calendar_id: str) -> Response[Calendar]:
        """
        Return a Calendar.

        Args:
            identifier: The identifier of the Grant to act upon.
            calendar_id: The ID of the Calendar to retrieve. Use "primary" to refer to the primary Calendar associated with the Grant.

        Returns:
            The Calendar.
        """
        return super(Calendars, self).find(
            path=f"/v3/grants/{identifier}/calendars/{calendar_id}",
            response_type=Calendar,
        )

    def create(
        self, identifier: str, request_body: CreateCalendarRequest
    ) -> Response[Calendar]:
        """
        Create a Calendar.

        Args:
            identifier: The identifier of the Grant to act upon.
            request_body: The values to create the Calendar with.

        Returns:
            The created Calendar.
        """
        return super(Calendars, self).create(
            path=f"/v3/grants/{identifier}/calendars",
            response_type=Calendar,
            request_body=request_body,
        )

    def update(
        self, identifier: str, calendar_id: str, request_body: UpdateCalendarRequest
    ) -> Response[Calendar]:
        """
        Update a Calendar.

        Args:
            identifier: The identifier of the Grant to act upon.
            calendar_id: The ID of the Calendar to update. Use "primary" to refer to the primary Calendar associated with the Grant.
            request_body: The values to update the Calendar with.

        Returns:
            The updated Calendar.
        """
        return super(Calendars, self).update(
            path=f"/v3/grants/{identifier}/calendars/{calendar_id}",
            response_type=Calendar,
            request_body=request_body,
        )

    def destroy(self, identifier: str, calendar_id: str) -> DeleteResponse:
        """
        Delete a Calendar.

        Args:
            identifier: The identifier of the Grant to act upon.
            calendar_id: The ID of the Calendar to delete. Use "primary" to refer to the primary Calendar associated with the Grant.

        Returns:
            The deletion response.
        """
        return super(Calendars, self).destroy(
            path=f"/v3/grants/{identifier}/calendars/{calendar_id}"
        )

    def get_availability(
        self, identifier: str, request_body: GetAvailabilityRequest
    ) -> Response[GetAvailabilityResponse]:
        """
        Get availability for a Calendar.

        Args:
            identifier: The grant ID or email account to get availability for.
            request_body: The request body to send to the API.

        Returns:
            Response: The availability response from the API.
        """
        json_response = self._http_client._execute(
            method="POST",
            path=f"/v3/grants/{identifier}/calendar/availability",
            request_body=request_body,
        )

        return Response.from_dict(json_response, GetAvailabilityResponse)

    def get_free_busy(
        self, identifier: str, request_body: GetFreeBusyRequest
    ) -> Response[GetFreeBusyResponse]:
        """
        Get free/busy info for a Calendar.

        Args:
            identifier: The grant ID or email account to get free/busy for.
            request_body: The request body to send to the API.

        Returns:
            Response: The free/busy response from the API.
        """
        json_response = self._http_client._execute(
            method="POST",
            path=f"/v3/grants/{identifier}/calendars/free-busy",
            request_body=request_body,
        )

        return Response(json_response, GetFreeBusyResponse)

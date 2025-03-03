from nylas.config import RequestOverrides
from nylas.handler.api_resources import (
    ListableApiResource,
    FindableApiResource,
    CreatableApiResource,
    UpdatableApiResource,
    DestroyableApiResource,
)
from nylas.models.events import (
    Event,
    UpdateEventRequest,
    CreateEventRequest,
    FindEventQueryParams,
    ListEventQueryParams,
    ListImportEventsQueryParams,
    CreateEventQueryParams,
    UpdateEventQueryParams,
    DestroyEventQueryParams,
    SendRsvpQueryParams,
    SendRsvpRequest,
)
from nylas.models.response import (
    Response,
    ListResponse,
    DeleteResponse,
    RequestIdOnlyResponse,
)


class Events(
    ListableApiResource,
    FindableApiResource,
    CreatableApiResource,
    UpdatableApiResource,
    DestroyableApiResource,
):
    """
    Nylas Events API

    The Events API allows you to find, create, update, and delete events on any calendar on your Nylas account.
    """

    def list(
        self,
        identifier: str,
        query_params: ListEventQueryParams,
        overrides: RequestOverrides = None,
    ) -> ListResponse[Event]:
        """
        Return all Events.

        Args:
            identifier: The identifier of the Grant to act upon.
            query_params: The query parameters to include in the request.
            overrides: The request overrides to use for the request.

        Returns:
            The list of Events.
        """

        return super().list(
            path=f"/v3/grants/{identifier}/events",
            response_type=Event,
            query_params=query_params,
            overrides=overrides,
        )

    def list_import_events(
        self,
        identifier: str,
        query_params: ListImportEventsQueryParams,
        overrides: RequestOverrides = None,
    ) -> ListResponse[Event]:
        """
        Returns a list of recurring events, recurring event exceptions, and 
        single events from the specified calendar within a given time frame. 
        This is useful when you want to import, store, and synchronize events 
        from the time frame to your application

        Args:
            identifier: The identifier of the Grant to act upon.
            query_params: The query parameters to include in the request.
            overrides: The request overrides to use for the request.

        Returns:
            The list of imported Events.
        """

        return super().list(
            path=f"/v3/grants/{identifier}/events/import",
            response_type=Event,
            query_params=query_params,
            overrides=overrides,
        )

    def find(
        self,
        identifier: str,
        event_id: str,
        query_params: FindEventQueryParams,
        overrides: RequestOverrides = None,
    ) -> Response[Event]:
        """
        Return an Event.

        Args:
            identifier: The identifier of the Grant to act upon.
            event_id: The ID of the Event to retrieve.
            query_params: The query parameters to include in the request.
            overrides: The request overrides to use for the request.

        Returns:
            The Event.
        """

        return super().find(
            path=f"/v3/grants/{identifier}/events/{event_id}",
            response_type=Event,
            query_params=query_params,
            overrides=overrides,
        )

    def create(
        self,
        identifier: str,
        request_body: CreateEventRequest,
        query_params: CreateEventQueryParams,
        overrides: RequestOverrides = None,
    ) -> Response[Event]:
        """
        Create an Event.

        Args:
            identifier: The identifier of the Grant to act upon.
            request_body: The values to create the Event with.
            query_params: The query parameters to include in the request.
            overrides: The request overrides to use for the request.

        Returns:
            The created Event.
        """

        return super().create(
            path=f"/v3/grants/{identifier}/events",
            response_type=Event,
            request_body=request_body,
            query_params=query_params,
            overrides=overrides,
        )

    def update(
        self,
        identifier: str,
        event_id: str,
        request_body: UpdateEventRequest,
        query_params: UpdateEventQueryParams,
        overrides: RequestOverrides = None,
    ) -> Response[Event]:
        """
        Update an Event.

        Args:
            identifier: The identifier of the Grant to act upon.
            event_id: The ID of the Event to update.
            request_body: The values to update the Event with.
            query_params: The query parameters to include in the request.
            overrides: The request overrides to use for the request.

        Returns:
            The updated Event.
        """

        return super().update(
            path=f"/v3/grants/{identifier}/events/{event_id}",
            response_type=Event,
            request_body=request_body,
            query_params=query_params,
            overrides=overrides,
        )

    def destroy(
        self,
        identifier: str,
        event_id: str,
        query_params: DestroyEventQueryParams,
        overrides: RequestOverrides = None,
    ) -> DeleteResponse:
        """
        Delete an Event.

        Args:
            identifier: The identifier of the Grant to act upon.
            event_id: The ID of the Event to delete.
            query_params: The query parameters to include in the request.
            overrides: The request overrides to use for the request.

        Returns:
            The deletion response.
        """

        return super().destroy(
            path=f"/v3/grants/{identifier}/events/{event_id}",
            query_params=query_params,
            overrides=overrides,
        )

    def send_rsvp(
        self,
        identifier: str,
        event_id: str,
        request_body: SendRsvpRequest,
        query_params: SendRsvpQueryParams,
        overrides: RequestOverrides = None,
    ) -> RequestIdOnlyResponse:
        """
        Send an RSVP for an event.

        Args:
            identifier: The grant ID or email account to send RSVP for.
            event_id: The event ID to send RSVP for.
            query_params: The query parameters to send to the API.
            request_body: The request body to send to the API.
            overrides: The request overrides to use for the request.

        Returns:
            Response: The RSVP response from the API.
        """
        json_response, headers = self._http_client._execute(
            method="POST",
            path=f"/v3/grants/{identifier}/events/{event_id}/send-rsvp",
            query_params=query_params,
            request_body=request_body,
            overrides=overrides,
        )

        return RequestIdOnlyResponse.from_dict(json_response, headers)

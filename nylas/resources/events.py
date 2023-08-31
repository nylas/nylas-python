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
    def list(
        self, identifier: str, query_params: ListEventQueryParams
    ) -> ListResponse[Event]:
        return super(Events, self).list(
            path=f"/v3/grants/{identifier}/events",
            response_type=Event,
            query_params=query_params,
        )

    def find(
        self, identifier: str, event_id: str, query_params: FindEventQueryParams
    ) -> Response[Event]:
        return super(Events, self).find(
            path=f"/v3/grants/{identifier}/events/{event_id}",
            response_type=Event,
            query_params=query_params,
        )

    def create(
        self,
        identifier: str,
        request_body: CreateEventRequest,
        query_params: CreateEventQueryParams,
    ) -> Response[Event]:
        return super(Events, self).create(
            path=f"/v3/grants/{identifier}/events",
            response_type=Event,
            request_body=request_body,
            query_params=query_params,
        )

    def update(
        self,
        identifier: str,
        event_id: str,
        request_body: UpdateEventRequest,
        query_params: UpdateEventQueryParams,
    ) -> Response[Event]:
        return super(Events, self).update(
            path=f"/v3/grants/{identifier}/events/{event_id}",
            response_type=Event,
            request_body=request_body,
            query_params=query_params,
        )

    def destroy(
        self, identifier: str, event_id: str, query_params: DestroyEventQueryParams
    ) -> DeleteResponse:
        return super(Events, self).destroy(
            path=f"/v3/grants/{identifier}/events/{event_id}",
            query_params=query_params,
        )

    def send_rsvp(
        self,
        identifier: str,
        event_id: str,
        request_body: SendRsvpRequest,
        query_params: SendRsvpQueryParams,
    ) -> RequestIdOnlyResponse:
        """Send RSVP for an event.

        Args:
            identifier: The grant ID or email account to send RSVP for.
            event_id: The event ID to send RSVP for.
            query_params: The query parameters to send to the API.
            request_body: The request body to send to the API.

        Returns:
            Response: The RSVP response from the API.
        """
        json_response = self._http_client._execute(
            method="POST",
            path=f"/v3/grants/{identifier}/events/{event_id}/send-rsvp",
            query_params=query_params,
            request_body=request_body,
        )

        return RequestIdOnlyResponse.from_dict(json_response)

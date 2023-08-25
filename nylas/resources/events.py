from nylas.handler.api_resources import (
    ListableApiResource,
    FindableApiResource,
    CreatableApiResource,
    UpdatableApiResource,
    DestroyableApiResource,
)
from nylas.models.delete_response import DeleteResponse
from nylas.models.event import Event
from nylas.models.list_response import ListResponse
from nylas.models.response import Response


class Events(
    ListableApiResource,
    FindableApiResource,
    CreatableApiResource,
    UpdatableApiResource,
    DestroyableApiResource,
):
    def list(self, identifier: str, query_params: dict) -> ListResponse[Event]:
        return super(Events, self).list(
            path=f"/v3/grants/{identifier}/events",
            response_type=Event,
            query_params=query_params,
        )

    def find(
        self, identifier: str, event_id: str, query_params: dict
    ) -> Response[Event]:
        return super(Events, self).find(
            path=f"/v3/grants/{identifier}/events/{event_id}",
            response_type=Event,
            query_params=query_params,
        )

    def create(
        self, identifier: str, request_body: dict, query_params: dict
    ) -> Response[Event]:
        return super(Events, self).create(
            path=f"/v3/grants/{identifier}/events",
            response_type=Event,
            request_body=request_body,
            query_params=query_params,
        )

    def update(
        self, identifier: str, event_id: str, request_body: dict, query_params: dict
    ) -> Response[Event]:
        return super(Events, self).update(
            path=f"/v3/grants/{identifier}/events/{event_id}",
            response_type=Event,
            request_body=request_body,
            query_params=query_params,
        )

    def destroy(
        self, identifier: str, event_id: str, query_params: dict
    ) -> DeleteResponse:
        return super(Events, self).destroy(
            path=f"/v3/grants/{identifier}/events/{event_id}",
            query_params=query_params,
        )

    def send_rsvp(
        self, identifier: str, event_id: str, request_body: dict, query_params: dict
    ) -> Response:
        """Send RSVP for an event.

        Args:
            identifier (str): The grant ID or email account to send RSVP for.
            event_id (str): The event ID to send RSVP for.
            query_params (dict): The query parameters to send to the API.
            request_body (dict): The request body to send to the API.

        Returns:
            Response: The RSVP response from the API.
        """
        json_response = self._http_client._execute(
            method="POST",
            path=f"/v3/grants/{identifier}/events/{event_id}/send-rsvp",
            query_params=query_params,
            request_body=request_body,
        )

        # TODO::Create model for RSVP response
        return Response.from_dict(json_response)

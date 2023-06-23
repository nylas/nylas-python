from nylas.handler.grants_api_resources import (
    ListableGrantsApiResource,
    FindableGrantsApiResource,
    CreatableGrantsApiResource,
    UpdatableGrantsApiResource,
    DestroyableGrantsApiResource,
)
from nylas.model.response import Response


class Events(
    ListableGrantsApiResource,
    FindableGrantsApiResource,
    CreatableGrantsApiResource,
    UpdatableGrantsApiResource,
    DestroyableGrantsApiResource,
):
    def __init__(self, http_client):
        super(Events, self).__init__("events", http_client)

    def send_rsvp(
        self, identifier: str, event_id: str, query_params: dict, request_body: dict
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
        json_response = self._http_client.post(
            "/v1/grants/{}/events/{}/rsvp".format(identifier, event_id),
            query_params=query_params,
            request_body=request_body,
        )

        return Response.from_dict(json_response)

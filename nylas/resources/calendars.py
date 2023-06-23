from nylas.handler.grants_api_resources import (
    ListableGrantsApiResource,
    FindableGrantsApiResource,
    CreatableGrantsApiResource,
    UpdatableGrantsApiResource,
    DestroyableGrantsApiResource,
)
from nylas.model.response import Response


class Calendars(
    ListableGrantsApiResource,
    FindableGrantsApiResource,
    CreatableGrantsApiResource,
    UpdatableGrantsApiResource,
    DestroyableGrantsApiResource,
):
    def __init__(self, http_client):
        super(Calendars, self).__init__("calendars", http_client)

    def get_availability(self, identifier: str, request_body: dict) -> Response:
        """Get availability for a calendar.

        Args:
            identifier (str): The grant ID or email account to get availability for.
            request_body (dict): The request body to send to the API.

        Returns:
            Response: The availability response from the API.
        """
        json_response = self._http_client.post(
            "/v3/grants/{}/calendar/availability".format(identifier),
            request_body=request_body,
        )

        return Response.from_dict(json_response)

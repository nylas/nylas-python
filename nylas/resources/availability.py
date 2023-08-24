from nylas.models.availability import GetAvailabilityResponse
from nylas.models.response import Response
from nylas.resources.resource import Resource


class Availability(Resource):
    def get_availability(
        self, identifier: str, request_body: dict
    ) -> Response[GetAvailabilityResponse]:
        """Get availability for a calendar.

        Args:
            identifier (str): The grant ID or email account to get availability for.
            request_body (dict): The request body to send to the API.

        Returns:
            Response: The availability response from the API.
        """
        json_response = self._http_client._execute(
            method="POST",
            path="/v3/grants/{}/calendar/availability".format(identifier),
            request_body=request_body,
        )

        return Response.from_dict(json_response, GetAvailabilityResponse)

from nylas.config import RequestOverrides
from nylas.models.availability import GetAvailabilityResponse
from nylas.models.response import Response
from nylas.models.scheduler import GetAvailabilityQueryParams
from nylas.resources.bookings import Bookings
from nylas.resources.configurations import Configurations
from nylas.resources.sessions import Sessions


class Scheduler:
    """
    Class representation of a Nylas Scheduler API.
    """

    def __init__(self, http_client):
        self.http_client = http_client

    @property
    def configurations(self) -> Configurations:
        """
        Access the Configurations API.

        Returns:
            The Configurations API.
        """
        return Configurations(self.http_client)

    @property
    def bookings(self) -> Bookings:
        """
        Access the Bookings API.

        Returns:
            The Bookings API.
        """
        return Bookings(self.http_client)

    @property
    def sessions(self) -> Sessions:
        """
        Access the Sessions API.

        Returns:
            The Sessions API.
        """
        return Sessions(self.http_client)

    def get_availability(
        self,
        query_params: GetAvailabilityQueryParams,
        overrides: RequestOverrides = None,
    ) -> Response[GetAvailabilityResponse]:
        """
        Get availability for a Configuration.

        Args:
            query_params: The query parameters to include in the request.
            overrides: The request overrides to use for the request.

        Returns:
            Response: The availability response from the API.
        """
        json_response, headers = self.http_client._execute(
            "GET",
            "/v3/scheduling/availability",
            query_params=query_params,
            overrides=overrides,
        )

        return Response.from_dict(json_response, GetAvailabilityResponse, headers)

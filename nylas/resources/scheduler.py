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

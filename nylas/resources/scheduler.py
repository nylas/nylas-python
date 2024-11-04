from configurations import Configurations
from bookings import Bookings

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


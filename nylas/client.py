from nylas.config import DEFAULT_SERVER_URL
from nylas.handler.http_client import HttpClient
from nylas.resources.applications import Applications
from nylas.resources.auth import Auth
from nylas.resources.calendars import Calendars
from nylas.resources.events import Events
from nylas.resources.webhooks import Webhooks


class Client(object):
    """
    API client for the Nylas API.

    Attributes:
        api_key: The Nylas API key to use for authentication
        api_uri: The URL to use for communicating with the Nylas API
        http_client: The HTTP client to use for requests to the Nylas API
    """

    def __init__(
        self, api_key: str, api_uri: str = DEFAULT_SERVER_URL, timeout: int = 30
    ):
        """
        Initialize the Nylas API client.

        Args:
            api_key: The Nylas API key to use for authentication
            api_uri: The URL to use for communicating with the Nylas API
            timeout: The timeout for requests to the Nylas API, in seconds
        """
        self.api_key = api_key
        self.api_uri = api_uri
        self.http_client = HttpClient(self.api_uri, self.api_key, timeout)

    @property
    def auth(self) -> Auth:
        """
        Access the Auth API.

        Returns:
            The Auth API.
        """
        return Auth(self.http_client)

    @property
    def applications(self) -> Applications:
        """
        Access the Applications API.

        Returns:
            The Applications API.
        """
        return Applications(self.http_client)

    @property
    def calendars(self) -> Calendars:
        """
        Access the Calendars API.

        Returns:
            The Calendars API.
        """
        return Calendars(self.http_client)

    @property
    def events(self) -> Events:
        """
        Access the Events API.

        Returns:
            The Events API.
        """
        return Events(self.http_client)

    @property
    def webhooks(self) -> Webhooks:
        """
        Access the Webhooks API.

        Returns:
            The Webhooks API.
        """
        return Webhooks(self.http_client)

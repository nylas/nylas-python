from nylas.config import DEFAULT_SERVER_URL
from nylas.handler.http_client import HttpClient
from nylas.resources.applications import Applications
from nylas.resources.attachments import Attachments
from nylas.resources.auth import Auth
from nylas.resources.calendars import Calendars
from nylas.resources.connectors import Connectors
from nylas.resources.events import Events
from nylas.resources.folders import Folders
from nylas.resources.messages import Messages
from nylas.resources.threads import Threads
from nylas.resources.webhooks import Webhooks
from nylas.resources.contacts import Contacts
from nylas.resources.drafts import Drafts
from nylas.resources.grants import Grants
from nylas.resources.scheduler import Scheduler
from nylas.resources.notetakers import Notetakers


class Client:
    """
    API client for the Nylas API.

    Attributes:
        api_key: The Nylas API key to use for authentication
        api_uri: The URL to use for communicating with the Nylas API
        http_client: The HTTP client to use for requests to the Nylas API
    """

    def __init__(
        self, api_key: str, api_uri: str = DEFAULT_SERVER_URL, timeout: int = 90
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
    def attachments(self) -> Attachments:
        """
        Access the Attachments API.

        Returns:
            The Attachments API.
        """
        return Attachments(self.http_client)

    @property
    def connectors(self) -> Connectors:
        """
        Access the Connectors API.

        Returns:
            The Connectors API.
        """
        return Connectors(self.http_client)

    @property
    def calendars(self) -> Calendars:
        """
        Access the Calendars API.

        Returns:
            The Calendars API.
        """
        return Calendars(self.http_client)

    @property
    def contacts(self) -> Contacts:
        """
        Access the Contacts API.

        Returns:
            The Contacts API.
        """
        return Contacts(self.http_client)

    @property
    def drafts(self) -> Drafts:
        """
        Access the Drafts API.

        Returns:
            The Drafts API.
        """
        return Drafts(self.http_client)

    @property
    def events(self) -> Events:
        """
        Access the Events API.

        Returns:
            The Events API.
        """
        return Events(self.http_client)

    @property
    def folders(self) -> Folders:
        """
        Access the Folders API.

        Returns:
            The Folders API.
        """
        return Folders(self.http_client)

    @property
    def grants(self) -> Grants:
        """
        Access the Grants API.

        Returns:
            The Grants API.
        """
        return Grants(self.http_client)

    @property
    def messages(self) -> Messages:
        """
        Access the Messages API.

        Returns:
            The Messages API.
        """
        return Messages(self.http_client)

    @property
    def threads(self) -> Threads:
        """
        Access the Threads API.

        Returns:
            The Threads API.
        """
        return Threads(self.http_client)

    @property
    def webhooks(self) -> Webhooks:
        """
        Access the Webhooks API.

        Returns:
            The Webhooks API.
        """
        return Webhooks(self.http_client)

    @property
    def scheduler(self) -> Scheduler:
        """
        Access the Scheduler API.

        Returns:
            The Scheduler API.
        """
        return Scheduler(self.http_client)

    @property
    def notetakers(self) -> Notetakers:
        """
        Access the Notetakers API.

        Returns:
            The Notetakers API.
        """
        return Notetakers(self.http_client)

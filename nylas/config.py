from enum import Enum
from typing import TypedDict

from typing_extensions import NotRequired


class Region(str, Enum):
    """
    Enum representing the regions supported by the Nylas API
    """

    US = "us"
    EU = "eu"


class RequestOverrides(TypedDict):
    """
    Overrides to use for an outgoing request to the Nylas API

    Attributes:
        api_key: The API key to use for the request.
        api_uri: The API URI to use for the request.
        timeout: The timeout to use for the request.
        headers: Additional headers to include in the request.
    """

    api_key: NotRequired[str]
    api_uri: NotRequired[str]
    timeout: NotRequired[int]
    headers: NotRequired[dict]


DEFAULT_REGION = Region.US
""" The default Nylas API region. """

REGION_CONFIG = {
    Region.US: {
        "nylasApiUrl": "https://api.us.nylas.com",
    },
    Region.EU: {
        "nylasApiUrl": "https://api.eu.nylas.com",
    },
}
""" The available preset configuration values for each Nylas API region. """

DEFAULT_SERVER_URL = REGION_CONFIG[DEFAULT_REGION]["nylasApiUrl"]
""" The default Nylas API URL. """

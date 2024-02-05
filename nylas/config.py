from enum import Enum


class Region(str, Enum):
    """
    Enum representing the regions supported by the Nylas API
    """

    US = "us"
    EU = "eu"


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

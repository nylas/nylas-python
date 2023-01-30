from enum import Enum


class Region(str, Enum):
    """
    Enum representing the regions supported by the Nylas API
    """

    US = "us"
    IRELAND = "ireland"


DEFAULT_REGION = Region.US

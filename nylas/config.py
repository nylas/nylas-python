from enum import Enum


class Region(str, Enum):
    """
    Enum representing the regions supported by the Nylas API
    """

    US = 'us',
    CANADA = 'canada'
    IRELAND = 'ireland'
    AUSTRALIA = 'australia'
    STAGING = 'staging'


DEFAULT_REGION = Region.US

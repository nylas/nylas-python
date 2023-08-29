from dataclasses import dataclass
from typing import Dict, Any, Optional

from dataclasses_json import dataclass_json
from typing_extensions import TypedDict, NotRequired


@dataclass_json
@dataclass
class Calendar:
    id: str
    grant_id: str
    name: str
    timezone: str
    read_only: bool
    is_owned_by_user: bool
    object: str = "calendar"
    description: Optional[str] = None
    location: Optional[str] = None
    hex_color: Optional[str] = None
    hex_foreground_color: Optional[str] = None
    is_primary: Optional[bool] = None
    metadata: Optional[Dict[str, Any]] = None


class ListCalendersQueryParams(TypedDict):
    """
    Interface of the query parameters for listing calendars.

    Attributes:
        limit: The maximum number of objects to return.
            This field defaults to 50. The maximum allowed value is 200.
        pageToken: An identifier that specifies which page of data to return.
            This value should be taken from the [ListResponse.nextCursor] response field.
        metadataPair: Pass in your metadata key and value pair to search for metadata.
    """

    limit: Optional[int]
    pageToken: Optional[str]
    metadataPair: Optional[Dict[str, str]]


class CreateCalendarRequest(TypedDict):
    """
    Interface of a Nylas create calendar request

    Attributes:
        name: Name of the Calendar.
        description: Description of the calendar.
        location: Geographic location of the calendar as free-form text.
        timezone: IANA time zone database formatted string (e.g. America/New_York).
        metadata: A list of key-value pairs storing additional data.
    """

    name: str
    description: NotRequired[str]
    location: NotRequired[str]
    timezone: NotRequired[str]
    metadata: NotRequired[Dict[str, str]]


class UpdateCalendarRequest(CreateCalendarRequest):
    """
    Interface of a Nylas update calendar request

    Attributes:
        hexColor: The background color of the calendar in the hexadecimal format (e.g. #0099EE).
            Empty indicates default color.
        hexForegroundColor: The background color of the calendar in the hexadecimal format (e.g. #0099EE).
            Empty indicates default color. (Google only)
    """

    hexColor: NotRequired[str]
    hexForegroundColor: NotRequired[str]

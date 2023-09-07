from dataclasses import dataclass
from typing import Dict, Any, Optional

from dataclasses_json import dataclass_json
from typing_extensions import TypedDict, NotRequired


@dataclass_json
@dataclass
class Calendar:
    """
    Class representation of a Nylas calendar object

    Attributes:
        id: Globally unique object identifier.
        grant_id: Grant ID of the Nylas account.
        name: Name of the calendar.
        timezone: IANA time zone database formatted string (e.g. America/New_York).
        read_only: If the event participants are able to edit the event.
        is_owned_by_user: If the calendar is owned by the user account.
        object: The type of object.
        description: Description of the calendar.
        location: Geographic location of the calendar as free-form text.
        hex_color: The background color of the calendar in the hexadecimal format (e.g. #0099EE).
            Empty indicates default color.
        hex_foreground_color: The background color of the calendar in the hexadecimal format (e.g. #0099EE).
            Empty indicates default color. (Google only)
        is_primary: If the calendar is the primary calendar.
        metadata: A list of key-value pairs storing additional data.
    """

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
        page_token: An identifier that specifies which page of data to return.
            This value should be taken from the next_cursor field of a ListResponse.
        metadata_pair: Pass in your metadata key and value pair to search for metadata.
    """

    limit: NotRequired[int]
    page_token: NotRequired[str]
    metadata_pair: NotRequired[Dict[str, str]]


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

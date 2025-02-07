from dataclasses import dataclass
from typing import Dict, Any, Optional

from dataclasses_json import dataclass_json
from typing_extensions import TypedDict, NotRequired

from nylas.models.list_query_params import ListQueryParams


@dataclass_json
@dataclass
class Calendar:
    """
    Class representation of a Nylas Calendar object.

    Attributes:
        id: Globally unique object identifier.
        grant_id: Grant ID representing the user's account.
        name: Name of the Calendar.
        timezone: IANA time zone database-formatted string (for example, "America/New_York").
            This value is only supported for Google and Virtual Calendars.
        read_only: If the event participants are able to edit the Event.
        is_owned_by_user: If the Calendar is owned by the user account.
        object: The type of object.
        description: Description of the Calendar.
        location: Geographic location of the Calendar as free-form text.
        hex_color: The background color of the calendar in the hexadecimal format (for example, "#0099EE").
            If not defined, the default color is used.
        hex_foreground_color: The background color of the calendar in the hexadecimal format (for example, "#0099EE").
            If not defined, the default color is used (Google only).
        is_primary: If the Calendar is the account's primary calendar.
        metadata: A list of key-value pairs storing additional data.
    """

    id: str
    grant_id: str
    name: str
    read_only: bool
    is_owned_by_user: bool
    object: str = "calendar"
    timezone: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    hex_color: Optional[str] = None
    hex_foreground_color: Optional[str] = None
    is_primary: Optional[bool] = None
    metadata: Optional[Dict[str, Any]] = None


class ListCalendarsQueryParams(ListQueryParams):
    """
    Interface of the query parameters for listing calendars.

    Attributes:
        limit (NotRequired[int]): The maximum number of objects to return.
            This field defaults to 50. The maximum allowed value is 200.
        page_token (NotRequired[str]): An identifier that specifies which page of data to return.
            This value should be taken from a ListResponse object's next_cursor parameter.
        metadata_pair: Pass in your metadata key-value pair to search for metadata.
        select (NotRequired[str]): Comma-separated list of fields to return in the response.
            This allows you to receive only the portion of object data that you're interested in.
    """

    metadata_pair: NotRequired[Dict[str, str]]


class FindCalendarQueryParams(TypedDict):
    """
    Interface of the query parameters for finding a calendar.

    Attributes:
        select: Comma-separated list of fields to return in the response.
            This allows you to receive only the portion of object data that you're interested in.
    """

    select: NotRequired[str]


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

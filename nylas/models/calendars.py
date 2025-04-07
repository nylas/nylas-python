from dataclasses import dataclass
from typing import Dict, Any, Optional, List
from enum import Enum

from dataclasses_json import dataclass_json
from typing_extensions import TypedDict, NotRequired

from nylas.models.list_query_params import ListQueryParams


class EventSelection(str, Enum):
    """
    Enum representing the different types of events to include for notetaking.

    Values:
        INTERNAL: Events where the host domain matches all participants' domain names
        EXTERNAL: Events where the host domain differs from any participant's domain name
        OWN_EVENTS: Events where the host is the same as the user's grant
        PARTICIPANT_ONLY: Events where the user's grant is a participant but not the host
        ALL: When all options are included, all events with meeting links will have Notetakers
    """
    INTERNAL = "internal"
    EXTERNAL = "external"
    OWN_EVENTS = "own_events"
    PARTICIPANT_ONLY = "participant_only"
    ALL = "all"


@dataclass_json
@dataclass
class NotetakerParticipantFilter:
    """
    Class representation of Notetaker participant filter settings.

    Attributes:
        participants_gte: Only have meeting bot join meetings with greater than or equal to this number of participants.
        participants_lte: Only have meeting bot join meetings with less than or equal to this number of participants.
    """
    participants_gte: Optional[int] = None
    participants_lte: Optional[int] = None


@dataclass_json
@dataclass
class NotetakerRules:
    """
    Class representation of Notetaker rules for joining meetings.

    Attributes:
        event_selection: Types of events to include for notetaking.
        participant_filter: Filters to apply based on the number of participants.
    """
    event_selection: Optional[List[EventSelection]] = None
    participant_filter: Optional[NotetakerParticipantFilter] = None


@dataclass_json
@dataclass
class NotetakerMeetingSettings:
    """
    Class representation of Notetaker meeting settings.

    Attributes:
        video_recording: When true, Notetaker records the meeting's video.
        audio_recording: When true, Notetaker records the meeting's audio.
        transcription: When true, Notetaker transcribes the meeting's audio.
    """
    video_recording: Optional[bool] = True
    audio_recording: Optional[bool] = True
    transcription: Optional[bool] = True


@dataclass_json
@dataclass
class CalendarNotetaker:
    """
    Class representation of Notetaker settings for a calendar.

    Attributes:
        name: The display name for the Notetaker bot.
        meeting_settings: Notetaker Meeting Settings.
        rules: Rules for when the Notetaker should join a meeting.
    """
    name: Optional[str] = "Nylas Notetaker"
    meeting_settings: Optional[NotetakerMeetingSettings] = None
    rules: Optional[NotetakerRules] = None


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
        notetaker: Notetaker meeting bot settings for the calendar.
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
    notetaker: Optional[CalendarNotetaker] = None


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


class NotetakerCalendarSettings(TypedDict):
    """
    Interface for Notetaker meeting settings for a calendar.

    Attributes:
        video_recording: When true, Notetaker records the meeting's video.
        audio_recording: When true, Notetaker records the meeting's audio.
        transcription: When true, Notetaker transcribes the meeting's audio.
    """
    video_recording: NotRequired[bool]
    audio_recording: NotRequired[bool]
    transcription: NotRequired[bool]


class NotetakerCalendarParticipantFilter(TypedDict):
    """
    Interface for Notetaker participant filter settings.

    Attributes:
        participants_gte: Only have meeting bot join meetings with greater than or equal to this number of participants.
        participants_lte: Only have meeting bot join meetings with less than or equal to this number of participants.
    """
    participants_gte: NotRequired[int]
    participants_lte: NotRequired[int]


class NotetakerCalendarRules(TypedDict):
    """
    Interface for Notetaker rules for joining meetings.

    Attributes:
        event_selection: Types of events to include for notetaking.
        participant_filter: Filters to apply based on the number of participants.
    """
    event_selection: NotRequired[List[EventSelection]]
    participant_filter: NotRequired[NotetakerCalendarParticipantFilter]


class NotetakerCalendarRequest(TypedDict):
    """
    Interface for Notetaker settings in a calendar request.

    Attributes:
        name: The display name for the Notetaker bot.
        meeting_settings: Notetaker Meeting Settings.
        rules: Rules for when the Notetaker should join a meeting.
    """
    name: NotRequired[str]
    meeting_settings: NotRequired[NotetakerCalendarSettings]
    rules: NotRequired[NotetakerCalendarRules]


class CreateCalendarRequest(TypedDict):
    """
    Interface of a Nylas create calendar request

    Attributes:
        name: Name of the Calendar.
        description: Description of the calendar.
        location: Geographic location of the calendar as free-form text.
        timezone: IANA time zone database formatted string (e.g. America/New_York).
        metadata: A list of key-value pairs storing additional data.
        notetaker: Notetaker meeting bot settings.
    """

    name: str
    description: NotRequired[str]
    location: NotRequired[str]
    timezone: NotRequired[str]
    metadata: NotRequired[Dict[str, str]]
    notetaker: NotRequired[NotetakerCalendarRequest]


class UpdateCalendarRequest(CreateCalendarRequest):
    """
    Interface of a Nylas update calendar request

    Attributes:
        hexColor: The background color of the calendar in the hexadecimal format (e.g. #0099EE).
            Empty indicates default color.
        hexForegroundColor: The background color of the calendar in the hexadecimal format (e.g. #0099EE).
            Empty indicates default color. (Google only)
        notetaker: Notetaker meeting bot settings.
    """

    hexColor: NotRequired[str]
    hexForegroundColor: NotRequired[str]
    notetaker: NotRequired[NotetakerCalendarRequest]

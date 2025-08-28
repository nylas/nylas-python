from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Union, Literal

from dataclasses_json import dataclass_json, config
from typing_extensions import TypedDict, NotRequired

from nylas.models.list_query_params import ListQueryParams

Status = Literal["confirmed", "tentative", "cancelled"]
""" Literal representing the status of an Event. """

Visibility = Literal["default", "public", "private"]
""" Literal representation of visibility of the Event. """

ParticipantStatus = Literal["noreply", "yes", "no", "maybe"]
""" Literal representing the status of an Event participant. """

SendRsvpStatus = Literal["yes", "no", "maybe"]
""" Literal representing the status of an RSVP. """

EventType = Literal["default", "outOfOffice", "focusTime", "workingLocation"]
""" Literal representing the event type to filter by. """


@dataclass_json
@dataclass
class Participant:
    """
    Interface representing an Event participant.

    Attributes:
        email: Participant's email address.
        name: Participant's name.
        status: Participant's status.
        comment: Comment by the participant.
        phone_number: Participant's phone number.
    """

    email: str
    status: Optional[ParticipantStatus] = None
    name: Optional[str] = None
    comment: Optional[str] = None
    phone_number: Optional[str] = None


class EmailName(TypedDict):
    """
    Interface representing an email address and optional name.

    Attributes:
        email: Email address.
        name: Full name.
    """

    email: str
    name: NotRequired[str]


@dataclass_json
@dataclass
class Time:
    """
    Class representation of a specific point in time.
    A meeting at 2pm would be represented as a time subobject.

    Attributes:
        time: A UNIX timestamp representing the time of occurrence.
        timezone: If timezone is present, then the value for time will be read with timezone.
            Timezone using IANA formatted string. (e.g. "America/New_York")
    """

    time: int
    timezone: Optional[str] = None
    object: str = "time"


@dataclass_json
@dataclass
class Timespan:
    """
    Class representation of a time span with start and end times.
    An hour lunch meeting would be represented as timespan subobjects.

    Attributes:
        start_time: The Event's start time.
        end_time: The Event's end time.
        start_timezone: The timezone of the start time, represented by an IANA-formatted string
            (for example, "America/New_York").
        end_timezone: The timezone of the end time, represented by an IANA-formatted string
            (for example, "America/New_York").
    """

    start_time: int
    end_time: int
    start_timezone: Optional[str] = None
    end_timezone: Optional[str] = None
    object: str = "timespan"


@dataclass_json
@dataclass
class Date:
    """
    Class representation of an entire day spans without specific times.
    Your birthday and holidays would be represented as date subobjects.

    Attributes:
        date: Date of occurrence in ISO 8601 format.
    """

    date: str
    object: str = "date"


@dataclass_json
@dataclass
class Datespan:
    """
    Class representation of a specific dates without clock-based start or end times.
    A business quarter or academic semester would be represented as datespan subobjects.

    Attributes:
        start_date: The start date in ISO 8601 format.
        end_date: The end date in ISO 8601 format.
    """

    start_date: str
    end_date: str
    object: str = "datespan"


When = Union[Time, Timespan, Date, Datespan]
""" Union type representing the different types of Event time configurations. """


def _decode_when(when: dict) -> When:
    """
    Decode a when object into a When object.

    Args:
        when: The when object to decode.

    Returns:
        The decoded When object.
    """
    if "object" not in when:
        raise ValueError("Invalid when object, no 'object' field found.")

    if when["object"] == "time":
        return Time.from_dict(when)

    if when["object"] == "timespan":
        return Timespan.from_dict(when)

    if when["object"] == "date":
        return Date.from_dict(when)

    if when["object"] == "datespan":
        return Datespan.from_dict(when)

    raise ValueError(
        f"Invalid when object, unknown 'object' field found: {when['object']}"
    )


ConferencingProvider = Literal[
    "Google Meet", "Zoom Meeting", "Microsoft Teams", "GoToMeeting", "WebEx", "unknown"
]
""" Literal for the different conferencing providers. """


@dataclass_json
@dataclass
class DetailsConfig:
    """
    Class representation of a conferencing details config object

    Attributes:
        meeting_code: The conferencing meeting code. Used for Zoom.
        password: The conferencing meeting password. Used for Zoom.
        url: The conferencing meeting url.
        pin: The conferencing meeting pin. Used for Google Meet.
        phone: The conferencing meeting phone numbers. Used for Google Meet.
    """

    meeting_code: Optional[str] = None
    password: Optional[str] = None
    url: Optional[str] = None
    pin: Optional[str] = None
    phone: Optional[List[str]] = None


@dataclass_json
@dataclass
class Details:
    """
    Class representation of a conferencing details object

    Attributes:
        provider: The conferencing provider
        details: The conferencing details
    """

    provider: ConferencingProvider
    details: Dict[str, Any]


@dataclass_json
@dataclass
class Autocreate:
    """
    Class representation of a conferencing autocreate object

    Attributes:
        provider: The conferencing provider
        autocreate: Empty dict to indicate an intention to autocreate a video link.
            Additional provider settings may be included in autocreate.settings, but Nylas does not validate these.
    """

    provider: ConferencingProvider
    autocreate: Dict[str, Any]


Conferencing = Union[Details, Autocreate]
""" Union type representing the different types of conferencing configurations. """


def _decode_conferencing(conferencing: dict) -> Union[Conferencing, None]:
    """
    Decode a conferencing object into a Conferencing object.

    Args:
        conferencing: The conferencing object to decode.

    Returns:
        The decoded Conferencing object, or None if empty or incomplete.
    """
    if not conferencing:
        return None

    # Handle details case - must have provider to be valid
    if "details" in conferencing and "provider" in conferencing:
        return Details.from_dict(conferencing)

    # Handle autocreate case - must have provider to be valid
    if "autocreate" in conferencing and "provider" in conferencing:
        return Autocreate.from_dict(conferencing)

    # Handle case where provider exists but details/autocreate doesn't
    if "provider" in conferencing:
        # Create a Details object with empty details
        details_dict = {
            "provider": conferencing["provider"],
            "details": (
                conferencing.get("conf_settings", {})
                if "conf_settings" in conferencing
                else {}
            ),
        }
        return Details.from_dict(details_dict)

    # Handle unknown or incomplete conferencing objects by returning None
    # This provides backwards compatibility for malformed conferencing data
    return None


@dataclass_json
@dataclass
class ReminderOverride:
    """
    Class representation of a reminder override object.

    Attributes:
        reminder_minutes: The user's preferred Event reminder time, in minutes.
            Reminder minutes are in the following format: "[20]".
        reminder_method: The user's preferred method for Event reminders (Google only).
    """

    reminder_minutes: Optional[int] = None
    reminder_method: Optional[str] = None


@dataclass_json
@dataclass
class Reminders:
    """
    Class representation of a reminder object.

    Attributes:
        use_default: Whether to use the default reminder settings for the calendar.
        overrides: A list of reminders for the event if use_default is set to false.
            If left empty or omitted while use_default is set to false, the event will have no reminders.
    """

    use_default: bool
    overrides: Optional[List[ReminderOverride]] = None


@dataclass_json
@dataclass
class NotetakerMeetingSettings:
    """
    Class representing Notetaker meeting settings.

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
class EventNotetaker:
    """
    Class representing Notetaker settings for an event.

    Attributes:
        id: The Notetaker bot ID.
        name: The display name for the Notetaker bot.
        meeting_settings: Notetaker Meeting Settings.
    """

    id: Optional[str] = None
    name: Optional[str] = "Nylas Notetaker"
    meeting_settings: Optional[NotetakerMeetingSettings] = None


@dataclass_json
@dataclass
class Event:
    """
    Class representation of a Nylas Event object.

    Attributes:
        id: Globally unique object identifier.
        grant_id: Grant ID representing the user's account.
        calendar_id: The Event's Calendar ID.
        busy: Whether to show this Event's time block as available on shared or public calendars.
        read_only: If the Event's participants are able to edit the Event.
        created_at: Unix timestamp representing the Event's creation time.
        updated_at: Unix timestamp representing the time when the Event was last updated.
        participants: List of participants invited to the Event. Participants may be people, rooms, or resources.
        when: Representation of an Event's time and duration.
        conferencing: Representation of an Event's conferencing details.
        object: The type of object.
        description: The Event's description.
        location: The Event's location (for example, a physical address or a meeting room).
        ical_uid: Unique ID for iCalendar standard, allowing you to identify events across calendaring systems.
            Recurring events may share the same value. Can be "null" for events synced before the year 2020.
        title: The Event's title.
        html_link: A link to the Event in the provider's UI.
        hide_participants: Whether participants of the Event should be hidden.
        metadata: List of key-value pairs storing additional data.
        creator: The user who created the Event.
        organizer: The organizer of the Event.
        recurrence: A list of RRULE and EXDATE strings.
        reminders: List of reminders for the Event.
        status: The Event's status.
        visibility: The Event's visibility (private or public).
        capacity: Sets the maximum number of participants that may attend the event.
        master_event_id: For recurring events, this field contains the main (master) event's ID.
        notetaker: Notetaker meeting bot settings.
    """

    id: str
    grant_id: str
    calendar_id: str
    busy: bool
    participants: List[Participant]
    when: When = field(metadata=config(decoder=_decode_when))
    conferencing: Optional[Conferencing] = field(
        default=None, metadata=config(decoder=_decode_conferencing)
    )
    object: str = "event"
    visibility: Optional[Visibility] = None
    read_only: Optional[bool] = None
    description: Optional[str] = None
    location: Optional[str] = None
    ical_uid: Optional[str] = None
    title: Optional[str] = None
    html_link: Optional[str] = None
    hide_participants: Optional[bool] = None
    metadata: Optional[Dict[str, Any]] = None
    creator: Optional[EmailName] = None
    organizer: Optional[EmailName] = None
    recurrence: Optional[List[str]] = None
    reminders: Optional[Reminders] = None
    status: Optional[Status] = None
    capacity: Optional[int] = None
    created_at: Optional[int] = None
    updated_at: Optional[int] = None
    master_event_id: Optional[str] = None
    notetaker: Optional[EventNotetaker] = None


class CreateParticipant(TypedDict):
    """
    Interface representing a participant for event creation.

    Attributes:
        email: Participant's email address.
        name: Participant's name.
        comment: Comment by the participant.
        phone_number: Participant's phone number.
    """

    email: str
    name: NotRequired[str]
    comment: NotRequired[str]
    phone_number: NotRequired[str]


class UpdateParticipant(TypedDict):
    """
    Interface representing a participant for updating an event.

    Attributes:
        email: Participant's email address.
        name: Participant's name.
        comment: Comment by the participant.
        phoneNumber: Participant's phone number.
    """

    email: NotRequired[str]
    name: NotRequired[str]
    comment: NotRequired[str]
    phoneNumber: NotRequired[str]


class WritableDetailsConfig(TypedDict):
    """
    Interface representing a writable conferencing details config object

    Attributes:
        meeting_code: The conferencing meeting code. Used for Zoom.
        password: The conferencing meeting password. Used for Zoom.
        url: The conferencing meeting url.
        pin: The conferencing meeting pin. Used for Google Meet.
        phone: The conferencing meeting phone numbers. Used for Google Meet.
    """

    meeting_code: NotRequired[str]
    password: NotRequired[str]
    url: NotRequired[str]
    pin: NotRequired[str]
    phone: NotRequired[List[str]]


class WriteableReminderOverride(TypedDict):
    """
    Interface representing a writable reminder override object.

    Attributes:
        reminder_minutes: The user's preferred Event reminder time, in minutes.
            Reminder minutes are in the following format: "[20]".
        reminder_method: The user's preferred method for Event reminders (Google only).
    """

    reminder_minutes: NotRequired[int]
    reminder_method: NotRequired[str]


class CreateReminders(TypedDict):
    """
    Interface representing a reminder object for event creation.

    Attributes:
        use_default: Whether to use the default reminder settings for the calendar.
        overrides: A list of reminders for the event if use_default is set to false.
            If left empty or omitted while use_default is set to false, the event will have no reminders.
    """

    use_default: bool
    overrides: NotRequired[List[WriteableReminderOverride]]


class UpdateReminders(TypedDict):
    """
    Interface representing a reminder object for updating an event.

    Attributes:
        use_default: Whether to use the default reminder settings for the calendar.
        overrides: A list of reminders for the event if use_default is set to false.
            If left empty or omitted while use_default is set to false, the event will have no reminders.
    """

    use_default: NotRequired[bool]
    overrides: NotRequired[List[WriteableReminderOverride]]


class CreateDetails(TypedDict):
    """
    Interface representing a conferencing details object for event creation

    Attributes:
        provider: The conferencing provider
        details: The conferencing details
    """

    provider: ConferencingProvider
    details: WritableDetailsConfig


class UpdateDetails(TypedDict):
    """
    Interface representing a conferencing details object for updating an event

    Attributes:
        provider: The conferencing provider
        details: The conferencing details
    """

    provider: NotRequired[ConferencingProvider]
    details: NotRequired[WritableDetailsConfig]


class CreateAutocreate(TypedDict):
    """
    Interface representing a conferencing autocreate object for event creation

    Attributes:
        provider: The conferencing provider
        autocreate: Empty dict to indicate an intention to autocreate a video link.
            Additional provider settings may be included in autocreate.settings, but Nylas does not validate these.
    """

    provider: ConferencingProvider
    autocreate: Dict[str, Any]


class UpdateAutocreate(TypedDict):
    """
    Interface representing a conferencing autocreate object for event creation

    Attributes:
        provider: The conferencing provider
        autocreate: Empty dict to indicate an intention to autocreate a video link.
            Additional provider settings may be included in autocreate.settings, but Nylas does not validate these.
    """

    provider: NotRequired[ConferencingProvider]
    autocreate: NotRequired[Dict[str, Any]]


CreateConferencing = Union[CreateDetails, CreateAutocreate]
""" Union type representing the different types of conferencing configurations for Event creation. """

UpdateConferencing = Union[UpdateDetails, UpdateAutocreate]
""" Union type representing the different types of conferencing configurations for updating an Event."""


# When
class CreateTime(TypedDict):
    """
    Interface representing a specific point in time for event creation.
    A meeting at 2pm would be represented as a time subobject.

    Attributes:
        time: A UNIX timestamp representing the time of occurrence.
        timezone: If timezone is present, then the value for time will be read with timezone.
            Timezone using IANA formatted string. (e.g. "America/New_York")
    """

    time: int
    timezone: NotRequired[str]


class UpdateTime(TypedDict):
    """
    Interface representing a specific point in time for updating an event.
    A meeting at 2pm would be represented as a time subobject.

    Attributes:
        time: A UNIX timestamp representing the time of occurrence.
        timezone: If timezone is present, then the value for time will be read with timezone.
            Timezone using IANA formatted string. (e.g. "America/New_York")
    """

    time: NotRequired[int]
    timezone: NotRequired[str]


class CreateTimespan(TypedDict):
    """
    Interface representing a time span with start and end times for event creation.
    An hour lunch meeting would be represented as timespan subobjects.

    Attributes:
        start_time: The start time of the event.
        end_time: The end time of the event.
        start_timezone: The timezone of the start time. Timezone using IANA formatted string. (e.g. "America/New_York")
        end_timezone: The timezone of the end time. Timezone using IANA formatted string. (e.g. "America/New_York")
    """

    start_time: int
    end_time: int
    start_timezone: NotRequired[str]
    end_timezone: NotRequired[str]


class UpdateTimespan(TypedDict):
    """
    Interface representing a time span with start and end times for updating an event.
    An hour lunch meeting would be represented as timespan subobjects.

    Attributes:
        start_time: The start time of the event.
        end_time: The end time of the event.
        start_timezone: The timezone of the start time. Timezone using IANA formatted string. (e.g. "America/New_York")
        end_timezone: The timezone of the end time. Timezone using IANA formatted string. (e.g. "America/New_York")
    """

    start_time: NotRequired[int]
    end_time: NotRequired[int]
    start_timezone: NotRequired[str]
    end_timezone: NotRequired[str]


class CreateDate(TypedDict):
    """
    Interface representing an entire day spans without specific times for event creation.
    Your birthday and holidays would be represented as date subobjects.

    Attributes:
        date: Date of occurrence in ISO 8601 format.
    """

    date: str


class UpdateDate(TypedDict):
    """
    Interface representing an entire day spans without specific times for updating an event.
    Your birthday and holidays would be represented as date subobjects.

    Attributes:
        date: Date of occurrence in ISO 8601 format.
    """

    date: NotRequired[str]


class CreateDatespan(TypedDict):
    """
    Interface representing a specific dates without clock-based start or end times for event creation.
    A business quarter or academic semester would be represented as datespan subobjects.

    Attributes:
        start_date: The start date in ISO 8601 format.
        end_date: The end date in ISO 8601 format.
    """

    start_date: str
    end_date: str


class UpdateDatespan(TypedDict):
    """
    Interface representing a specific dates without clock-based start or end times for updating an event.
    A business quarter or academic semester would be represented as datespan subobjects.

    Attributes:
        start_date: The start date in ISO 8601 format.
        end_date: The end date in ISO 8601 format.
    """

    start_date: NotRequired[str]
    end_date: NotRequired[str]


CreateWhen = Union[CreateTime, CreateTimespan, CreateDate, CreateDatespan]
""" Union type representing the different types of event time configurations for Event creation. """

UpdateWhen = Union[UpdateTime, UpdateTimespan, UpdateDate, UpdateDatespan]
""" Union type representing the different types of event time configurations for updating an Event."""


class EventNotetakerSettings(TypedDict):
    """
    Interface representing Notetaker meeting settings for an event.

    Attributes:
        video_recording: When true, Notetaker records the meeting's video.
        audio_recording: When true, Notetaker records the meeting's audio.
        transcription: When true, Notetaker transcribes the meeting's audio.
    """

    video_recording: NotRequired[bool]
    audio_recording: NotRequired[bool]
    transcription: NotRequired[bool]


class EventNotetakerRequest(TypedDict):
    """
    Interface representing Notetaker settings for an event.

    Attributes:
        id: The Notetaker bot ID.
        name: The display name for the Notetaker bot.
        meeting_settings: Notetaker Meeting Settings.
    """

    id: NotRequired[str]
    name: NotRequired[str]
    meeting_settings: NotRequired[EventNotetakerSettings]


class CreateEventNotetaker(TypedDict):
    """
    Class representing Notetaker settings for an event.

    Attributes:
        name: The display name for the Notetaker bot.
        meeting_settings: Notetaker Meeting Settings.
    """

    name: Optional[str] = "Nylas Notetaker"
    meeting_settings: Optional[EventNotetakerSettings] = None

class CreateEventRequest(TypedDict):
    """
    Interface representing a request to create an event.

    Attributes:
        when: When the event occurs.
        title: The title of the event.
        busy: Whether the event is busy or free.
        description: The description of the event.
        location: The location of the event.
        conferencing: The conferencing details of the event.
        reminders: A list of reminders to send for the event.
            If left empty or omitted, the event uses the provider defaults.
        metadata: Metadata associated with the event.
        participants: The participants of the event.
        recurrence: The recurrence rules of the event.
        visibility: The visibility of the event.
        capacity: The capacity of the event.
        hide_participants: Whether to hide participants of the event.
        notetaker: Notetaker meeting bot settings.
    """

    when: CreateWhen
    title: NotRequired[str]
    busy: NotRequired[bool]
    description: NotRequired[str]
    location: NotRequired[str]
    conferencing: NotRequired[CreateConferencing]
    reminders: NotRequired[CreateReminders]
    metadata: NotRequired[Dict[str, Any]]
    participants: NotRequired[List[CreateParticipant]]
    recurrence: NotRequired[List[str]]
    visibility: NotRequired[Visibility]
    capacity: NotRequired[int]
    hide_participants: NotRequired[bool]
    notetaker: NotRequired[CreateEventNotetaker]


class UpdateEventRequest(TypedDict):
    """
    Interface representing a request to update an event.

    Attributes:
        when: When the event occurs.
        title: The title of the event.
        busy: Whether the event is busy or free.
        description: The description of the event.
        location: The location of the event.
        conferencing: The conferencing details of the event.
        reminders: A list of reminders to send for the event.
        metadata: Metadata associated with the event.
        participants: The participants of the event.
        recurrence: The recurrence rules of the event.
        visibility: The visibility of the event.
        capacity: The capacity of the event.
        hide_participants: Whether to hide participants of the event.
        notetaker: Notetaker meeting bot settings.
    """

    when: NotRequired[UpdateWhen]
    title: NotRequired[str]
    busy: NotRequired[bool]
    description: NotRequired[str]
    location: NotRequired[str]
    conferencing: NotRequired[UpdateConferencing]
    reminders: NotRequired[UpdateReminders]
    metadata: NotRequired[Dict[str, Any]]
    participants: NotRequired[List[UpdateParticipant]]
    recurrence: NotRequired[List[str]]
    visibility: NotRequired[Visibility]
    capacity: NotRequired[int]
    hide_participants: NotRequired[bool]
    notetaker: NotRequired[EventNotetakerRequest]


class ListEventQueryParams(ListQueryParams):
    """
    Interface representing the query parameters for listing events.

    Attributes:
        calendar_id: Specify calendar ID of the event. "primary" is a supported value
            indicating the user's primary calendar.
        show_cancelled: Return events that have a status of cancelled.
            If an event is recurring, then it returns no matter the value set.
            Different providers have different semantics for cancelled events.
        title: Return events matching the specified title.
        description: Return events matching the specified description.
        location: Return events matching the specified location.
        start: Return events starting after the specified unix timestamp.
            Defaults to the current timestamp. Not respected by metadata filtering.
        end: Return events ending before the specified unix timestamp.
            Defaults to a month from now. Not respected by metadata filtering.
        metadata_pair: Pass in your metadata key and value pair to search for metadata.
        expand_recurring: If true, the response will include an event for each occurrence of a recurring event within
            the requested time range.
            If false, only a single primary event will be returned for each recurring event.
            Cannot be used when filtering on metadata. Defaults to false.
        busy: Returns events with a busy status of true.
        order_by: Order results by the specified field.
            Currently only start is supported.
        event_type (NotRequired[List[EventType]]): (Google only) Filter events by event type.
            You can pass the query parameter multiple times to select or exclude multiple event types.
        master_event_id (NotRequired[str]): Filter for instances of recurring events with the
            specified master_event_id. Not respected by metadata filtering.
        tentative_as_busy: When set to false, treats tentative calendar events as busy:false.
            Only applicable for Microsoft and EWS calendar providers. Defaults to true.
        select: Comma-separated list of fields to return in the response.
            This allows you to receive only the portion of object data that you're interested in.
        limit (NotRequired[int]): The maximum number of objects to return.
            This field defaults to 50. The maximum allowed value is 200.
        page_token (NotRequired[str]): An identifier that specifies which page of data to return.
            This value should be taken from a ListResponse object's next_cursor parameter.
    """

    calendar_id: str
    show_cancelled: NotRequired[bool]
    title: NotRequired[str]
    description: NotRequired[str]
    location: NotRequired[str]
    start: NotRequired[int]
    end: NotRequired[int]
    metadata_pair: NotRequired[Dict[str, Any]]
    expand_recurring: NotRequired[bool]
    busy: NotRequired[bool]
    order_by: NotRequired[str]
    event_type: NotRequired[List[EventType]]
    master_event_id: NotRequired[str]
    select: NotRequired[str]
    tentative_as_busy: NotRequired[bool]


class CreateEventQueryParams(TypedDict):
    """
    Interface representing of the query parameters for creating an event.

    Attributes:
        calendar_id: The ID of the calendar to create the event in.
        notify_participants: Email notifications containing the calendar event is sent to all event participants.
        tentative_as_busy: When set to false, treats tentative calendar events as busy:false.
            Only applicable for Microsoft and EWS calendar providers. Defaults to true.
    """

    calendar_id: str
    notify_participants: NotRequired[bool]
    tentative_as_busy: NotRequired[bool]


class FindEventQueryParams(TypedDict):
    """
    Interface representing of the query parameters for finding an event.

    Attributes:
        calendar_id: Calendar ID to find the event in.
            "primary" is a supported value indicating the user's primary calendar.
        tentative_as_busy: When set to false, treats tentative calendar events as busy:false.
            Only applicable for Microsoft and EWS calendar providers. Defaults to true.
    """

    calendar_id: str
    tentative_as_busy: NotRequired[bool]


UpdateEventQueryParams = CreateEventQueryParams
""" Interface representing of the query parameters for updating an Event. """

DestroyEventQueryParams = CreateEventQueryParams
""" Interface representing of the query parameters for destroying an Event. """


class SendRsvpQueryParams(TypedDict):
    """
    Interface representing of the query parameters for an event.

    Attributes:
        calendar_id: Calendar ID to find the event in.
            "primary" is a supported value indicating the user's primary calendar.
    """

    calendar_id: str


class SendRsvpRequest(TypedDict):
    """
    Interface representing a request to send an RSVP.

    Attributes:
        status: The status of the RSVP.
    """

    status: SendRsvpStatus


class ListImportEventsQueryParams(ListQueryParams):
    """
    Interface representing the query parameters for listing imported events.

    Attributes:
        calendar_id: Specify calendar ID to import events to. "primary" is a supported value
            indicating the user's primary calendar.
        start: Filter for events that start at or after the specified time, in Unix timestamp format.
        end: Filter for events that end at or before the specified time, in Unix timestamp format.
        select: Comma-separated list of fields to return in the response.
            This allows you to receive only the portion of object data that you're interested in.
        page_token: An identifier that specifies which page of data to return.
            This value should be taken from a ListResponse object's next_cursor parameter.
    """

    calendar_id: str
    start: NotRequired[int]
    end: NotRequired[int]
    select: NotRequired[str]
    page_token: NotRequired[str]

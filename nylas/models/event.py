from dataclasses import dataclass
from typing import Dict, Any, List, Optional, Union, Literal

from dataclasses_json import dataclass_json
from typing_extensions import TypedDict, NotRequired

Status = Literal["confirmed", "tentative", "cancelled"]
Visibility = Literal["public", "private"]
ParticipantStatus = Literal["noreply", "yes", "no", "maybe"]


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
        phoneNumber: Participant's phone number.
    """

    email: str
    status: ParticipantStatus
    name: Optional[str]
    comment: Optional[str]
    phoneNumber: Optional[str]


@dataclass_json
@dataclass
class EmailName:
    """
    Interface representing an email address and optional name.

    Attributes:
        email: Email address.
        name: Full name.
    """

    email: str
    name: Optional[str]


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
    timezone: str


@dataclass_json
@dataclass
class Timespan:
    """
    Class representation of a time span with start and end times.
    An hour lunch meeting would be represented as timespan subobjects.

    Attributes:
        startTime: The start time of the event.
        endTime: The end time of the event.
        startTimezone: The timezone of the start time. Timezone using IANA formatted string. (e.g. "America/New_York")
        endTimezone: The timezone of the end time. Timezone using IANA formatted string. (e.g. "America/New_York")
    """

    startTime: int
    endTime: int
    startTimezone: Optional[str]
    endTimezone: Optional[str]


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


@dataclass_json
@dataclass
class Datespan:
    """
    Class representation of a specific dates without clock-based start or end times.
    A business quarter or academic semester would be represented as datespan subobjects.

    Attributes:
        startDate: The start date in ISO 8601 format.
        endDate: The end date in ISO 8601 format.
    """

    startDate: str
    endDate: str


When = Union[Time, Timespan, Date, Datespan]
ConferencingProvider = Literal[
    "Google Meet", "Zoom Meeting", "Microsoft Teams", "GoToMeeting", "WebEx"
]


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


@dataclass_json
@dataclass
class Reminder:
    """
    Class representation of a reminder object.

    Attributes:
        reminderMinutes: The number of minutes before the event start time when a user wants a reminder for this event.
            Reminder minutes are in the following format: "[20]".
        reminderMethod: Method to remind the user about the event. (Google only).
    """

    reminderMinutes: str
    reminderMethod: str


@dataclass_json
@dataclass
class Event:
    id: str
    grant_id: str
    calendar_id: str
    busy: bool
    read_only: bool
    created_at: int
    updated_at: int
    participants: List[Participant]
    when: When
    conferencing: Conferencing
    object: str = "event"
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
    reminders: Optional[List[Reminder]] = None
    status: Optional[Status] = None
    visibility: Optional[Visibility] = None


class CreateParticipant(TypedDict):
    """
    Interface representing a participant for event creation.

    Attributes:
        email: Participant's email address.
        name: Participant's name.
        status: Participant's status.
        comment: Comment by the participant.
        phoneNumber: Participant's phone number.
    """

    email: str
    status: NotRequired[ParticipantStatus]
    name: NotRequired[str]
    comment: NotRequired[str]
    phoneNumber: NotRequired[str]


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
UpdateConferencing = Union[UpdateDetails, UpdateAutocreate]


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
UpdateWhen = Union[UpdateTime, UpdateTimespan, UpdateDate, UpdateDatespan]


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
        reminder_minutes: The number of minutes before the event start time when a user wants a reminder for this event.
            Reminder minutes are in the following format: "[20]".
        reminder_method: Method to remind the user about the event. (Google only).
        metadata: Metadata associated with the event.
        participants: The participants of the event.
        recurrence: The recurrence rules of the event.
        calendar_id: The ID of the calendar to create the event in.
        read_only: Whether the event is read-only.
        visibility: The visibility of the event.
        capacity: The capacity of the event.
        hide_participants: Whether to hide participants of the event.
    """

    when: CreateWhen
    title: NotRequired[str]
    busy: NotRequired[bool]
    description: NotRequired[str]
    location: NotRequired[str]
    conferencing: NotRequired[CreateConferencing]
    reminder_minutes: NotRequired[str]
    reminder_method: NotRequired[str]
    metadata: NotRequired[Dict[str, Any]]
    participants: NotRequired[List[CreateParticipant]]
    recurrence: NotRequired[List[str]]
    calendar_id: NotRequired[str]
    read_only: NotRequired[bool]
    visibility: NotRequired[Visibility]
    capacity: NotRequired[int]
    hide_participants: NotRequired[bool]


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
        reminder_minutes: The number of minutes before the event start time when a user wants a reminder for this event.
            Reminder minutes are in the following format: "[20]".
        reminder_method: Method to remind the user about the event. (Google only).
        metadata: Metadata associated with the event.
        participants: The participants of the event.
        recurrence: The recurrence rules of the event.
        calendar_id: The ID of the calendar to create the event in.
        read_only: Whether the event is read-only.
        visibility: The visibility of the event.
        capacity: The capacity of the event.
        hide_participants: Whether to hide participants of the event.
    """

    when: NotRequired[UpdateWhen]
    title: NotRequired[str]
    busy: NotRequired[bool]
    description: NotRequired[str]
    location: NotRequired[str]
    conferencing: NotRequired[UpdateConferencing]
    reminder_minutes: NotRequired[str]
    reminder_method: NotRequired[str]
    metadata: NotRequired[Dict[str, Any]]
    participants: NotRequired[List[UpdateParticipant]]
    recurrence: NotRequired[List[str]]
    calendar_id: NotRequired[str]
    read_only: NotRequired[bool]
    visibility: NotRequired[Visibility]
    capacity: NotRequired[int]
    hide_participants: NotRequired[bool]

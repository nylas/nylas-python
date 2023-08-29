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


class CreateEventRequest(TypedDict):
    """
    Interface representing a request to create an event.
    """

    when: str
    title: NotRequired[str]
    busy: NotRequired[bool]
    description: NotRequired[str]
    location: NotRequired[str]
    conferencing: NotRequired[str]
    reminderMinutes: NotRequired[str]
    reminderMethod: NotRequired[str]
    metadata: NotRequired[Dict[str, Any]]
    participants: NotRequired[List[Participant]]
    recurrence: NotRequired[List[str]]
    calendarId: NotRequired[str]
    readOnly: NotRequired[bool]
    visibility: NotRequired[str]
    capacity: NotRequired[int]
    hideParticipants: NotRequired[bool]

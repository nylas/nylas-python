from dataclasses import dataclass
from typing import Dict, Any, List, Optional

from dataclasses_json import dataclass_json
from typing_extensions import TypedDict, NotRequired, get_type_hints


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
    status: str
    name: Optional[str]
    comment: Optional[str]
    phoneNumber: Optional[str]


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
    # when: When
    # conferencing: Conferencing
    description: str
    location: str
    message_id: str
    owner: str
    ical_uid: str
    title: str
    html_link: str
    hide_participants: bool
    metadata: Dict[str, Any]
    # creator: EmailName
    # organizer: EmailName
    # recurrence: Recurrence
    # reminders: Reminder[]
    # status: Status
    # visibility: Visibility
    object: str = "event"


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

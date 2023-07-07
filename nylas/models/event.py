from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class Event:
    id: str
    grant_id: str
    calendar_id: str
    busy: bool
    read_only: bool
    created_at: int
    updated_at: int
    # participants: Participant[]
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

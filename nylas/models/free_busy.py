from dataclasses import dataclass
from typing import List, Union

from dataclasses_json import dataclass_json
from typing_extensions import TypedDict


@dataclass_json
@dataclass
class FreeBusyError:
    """
    Interface for a Nylas free/busy call error

    Attributes:
        email: The email address of the participant who had an error.
        error: The provider's error message.
    """

    email: str
    error: str


@dataclass_json
@dataclass
class TimeSlot:
    """
    Interface for a Nylas free/busy time slot

    Attributes:
        start_time: Unix timestamp for the start of the slot.
        end_time: Unix timestamp for the end of the slot.
        status: The status of the slot. Typically "busy"
    """

    start_time: int
    end_time: int
    status: str


@dataclass_json
@dataclass
class FreeBusy:
    """
    Interface for an individual Nylas free/busy response

    Attributes:
        email: The email address of the participant.
        time_slots: List of time slots for the participant.
    """

    email: str
    time_slots: List[TimeSlot]


GetFreeBusyResponse = List[Union[FreeBusy, FreeBusyError]]
""" Interface for a Nylas get free/busy response """


class GetFreeBusyRequest(TypedDict):
    """
    Interface for a Nylas get free/busy request

    Attributes:
        start_time: Unix timestamp for the start time to check free/busy for.
        end_time: Unix timestamp for the end time to check free/busy for.
        emails: List of email addresses to check free/busy for.
    """

    start_time: int
    end_time: int
    emails: List[str]

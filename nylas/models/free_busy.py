from dataclasses import dataclass
from typing import List, Union

from dataclasses_json import dataclass_json
from typing_extensions import TypedDict


@dataclass_json
@dataclass
class Error:
    email: str
    error: str


@dataclass_json
@dataclass
class TimeSlot:
    """
    Interface for a Nylas free/busy time slot

    Attributes:
        emails: The emails of the participants who are available for the time slot.
        start_time: Unix timestamp for the start of the slot.
        end_time: Unix timestamp for the end of the slot.
    """

    start_time: int
    end_time: int
    status: str


@dataclass_json
@dataclass
class FreeBusy:
    email: str
    time_slots: List[TimeSlot]


@dataclass_json
@dataclass
class GetFreeBusyResponse:
    """
    Interface for a Nylas get free/busy response

    """

    data: List[Union[FreeBusy, Error]]


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

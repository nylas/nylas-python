from dataclasses import dataclass
from typing import List, Optional, Literal

from dataclasses_json import dataclass_json

# AvailabilityMethod = Literal["max-fairness", "max-availability"]


@dataclass_json
@dataclass
class TimeSlot:
    accounts: List[str]
    start_time: int
    end_time: int


@dataclass_json
@dataclass
class GetAvailabilityResponse:
    order: List[str]
    time_slots: List[TimeSlot]


# @dataclass_json
# @dataclass
# class MeetingBuffer:
#     before: int
#     after: int
#
#
# @dataclass_json
# @dataclass
# class OpenHours:
#     days: List[int]
#     timezone: str
#     start: str
#     end: str
#
#
# @dataclass_json
# @dataclass
# class AvailabilityRules:
#     availability_method: Optional[AvailabilityMethod] = None
#     buffer: Optional[MeetingBuffer] = None
#     default_open_hours: Optional[List[OpenHours]] = None
#     round_robin_event_id: Optional[str] = None
#
#
# @dataclass_json
# @dataclass
# class Participant:
#     email: str
#     calendar_ids: Optional[List[str]] = None
#     open_hours: Optional[List[OpenHours]] = None
#
#
# @dataclass_json
# @dataclass
# class GetAvailabilityRequest:
#     start_time: int
#     end_time: int
#     participants: List[Participant]
#     duration_minutes: int
#     interval_minutes: Optional[int] = None
#     round_to_30_minutes: Optional[bool] = None
#     availability_rules: Optional[AvailabilityRules] = None

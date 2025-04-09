from dataclasses import dataclass, field
from typing import List, Literal

from dataclasses_json import dataclass_json
from typing_extensions import TypedDict, NotRequired

AvailabilityMethod = Literal["max-fairness", "max-availability"]
""" Literal representing the method used to determine availability for a meeting. """


@dataclass_json
@dataclass
class TimeSlot:
    """
    Interface for a Nylas availability time slot

    Attributes:
        emails: The emails of the participants who are available for the time slot.
        start_time: Unix timestamp for the start of the slot.
        end_time: Unix timestamp for the end of the slot.
    """

    emails: List[str]
    start_time: int
    end_time: int


@dataclass_json
@dataclass
class GetAvailabilityResponse:
    """
    Interface for a Nylas get availability response

    Attributes:
        order: This property is only populated for round-robin events.
            It will contain the order in which the accounts would be next in line to attend the proposed meeting.
        time_slots: The available time slots where a new meeting can be created for the requested preferences.
    """

    time_slots: List[TimeSlot]
    order: List[str] = field(default_factory=list)


class MeetingBuffer(TypedDict):
    """
    Interface for the meeting buffer object within an availability request.

    Attributes:
        before: The amount of buffer time in increments of 5 minutes to add before existing meetings.
            Defaults to 0.
        after: The amount of buffer time in increments of 5 minutes to add after existing meetings.
            Defaults to 0.
    """

    before: int
    after: int


class OpenHours(TypedDict):
    """
    Interface of a participant's open hours.

    Attributes:
        days: The days of the week that the open hour settings will be applied to.
            Sunday corresponds to 0 and Saturday corresponds to 6.
        timezone: IANA time zone database formatted string (e.g. America/New_York).
        start: Start time in 24-hour time format. Leading 0's are left off.
        end: End time in 24-hour time format. Leading 0's are left off.
        extdates: A list of dates that will be excluded from the open hours.
            Dates should be formatted as YYYY-MM-DD.
    """

    days: List[int]
    timezone: str
    start: str
    end: str
    exdates: NotRequired[List[str]]


class AvailabilityRules(TypedDict):
    """
    Interface for the availability rules for a Nylas calendar.

    Attributes:
        availability_method: The method used to determine availability for a meeting.
        buffer: The buffer to add to the start and end of a meeting.
        default_open_hours: A default set of open hours to apply to all participants.
            You can overwrite these open hours for individual participants by specifying open_hours on
            the participant object.
        round_robin_group_id: The ID on events that Nylas considers when calculating the order of
            round-robin participants.
            This is used for both max-fairness and max-availability methods.
        tentative_as_busy: Controls whether tentative calendar events should be treated as busy time.
            When set to false, tentative events will be considered as free in availability calculations.
            Defaults to true. Only applicable for Microsoft and EWS calendar providers.
    """

    availability_method: NotRequired[AvailabilityMethod]
    buffer: NotRequired[MeetingBuffer]
    default_open_hours: NotRequired[List[OpenHours]]
    round_robin_group_id: NotRequired[str]
    tentative_as_busy: NotRequired[bool]


class AvailabilityParticipant(TypedDict):
    """
    Interface of participant details to check availability for.

    Attributes:
        email: The email address of the participant.
        calendar_ids: An optional list of the calendar IDs associated with each participant's email address.
            If not provided, Nylas uses the primary calendar ID.
        open_hours: Open hours for this participant. The endpoint searches for free time slots during these open hours.
    """

    email: str
    calendar_ids: NotRequired[List[str]]
    open_hours: NotRequired[List[OpenHours]]


class GetAvailabilityRequest(TypedDict):
    """
    Interface for a Nylas get availability request

    Attributes:
        start_time: Unix timestamp for the start time to check availability for.
        end_time: Unix timestamp for the end time to check availability for.
        participants: Participant details to check availability for.
        duration_minutes: The total number of minutes the event should last.
        interval_minutes: Nylas checks from the nearest interval of the passed start time.
            For example, to schedule 30-minute meetings with 15 minutes between them.
            If you have a meeting starting at 9:59, the API returns times starting at 10:00. 10:00-10:30, 10:15-10:45.
        round_to_30_minutes: When set to true, the availability time slots will start at 30 minutes past or on the hour.
            For example, a free slot starting at 16:10 is considered available only from 16:30.
            Note: This field is deprecated, use round_to instead.
        availability_rules: The rules to apply when checking availability.
        round_to: The number of minutes to round the time slots to.
            This allows for rounding to any multiple of 5 minutes, up to a maximum of 60 minutes.
            The default value is set to 15 minutes.
            When this variable is assigned a value, it overrides the behavior of the roundTo30Minutes flag,if it was set
    """

    start_time: int
    end_time: int
    participants: List[AvailabilityParticipant]
    duration_minutes: int
    interval_minutes: NotRequired[int]
    round_to_30_minutes: NotRequired[bool]
    availability_rules: NotRequired[AvailabilityRules]
    round_to: NotRequired[int]

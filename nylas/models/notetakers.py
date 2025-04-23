from dataclasses import dataclass
from enum import Enum
from typing import Optional

from dataclasses_json import dataclass_json
from typing_extensions import NotRequired, TypedDict

from nylas.models.list_query_params import ListQueryParams


class NotetakerState(str, Enum):
    """
    Enum representing the possible states of a Notetaker bot.

    Values:
        SCHEDULED: The Notetaker is scheduled to join a meeting.
        CONNECTING: The Notetaker is connecting to the meeting.
        WAITING_FOR_ENTRY: The Notetaker is waiting to be admitted to the meeting.
        FAILED_ENTRY: The Notetaker failed to join the meeting.
        ATTENDING: The Notetaker is currently in the meeting.
        MEDIA_PROCESSING: The Notetaker is processing media from the meeting.
        MEDIA_AVAILABLE: The Notetaker has processed media available for download.
        MEDIA_ERROR: An error occurred while processing the media.
        MEDIA_DELETED: The meeting media has been deleted.
    """

    SCHEDULED = "scheduled"
    CONNECTING = "connecting"
    WAITING_FOR_ENTRY = "waiting_for_entry"
    FAILED_ENTRY = "failed_entry"
    ATTENDING = "attending"
    MEDIA_PROCESSING = "media_processing"
    MEDIA_AVAILABLE = "media_available"
    MEDIA_ERROR = "media_error"
    MEDIA_DELETED = "media_deleted"


class NotetakerOrderBy(str, Enum):
    """
    Enum representing the possible fields to order Notetaker bots by.

    Values:
        NAME: Order by the Notetaker's name.
        JOIN_TIME: Order by the Notetaker's join time.
        CREATED_AT: Order by when the Notetaker was created.
    """

    NAME = "name"
    JOIN_TIME = "join_time"
    CREATED_AT = "created_at"


class NotetakerOrderDirection(str, Enum):
    """
    Enum representing the possible directions to order Notetaker bots by.

    Values:
        ASC: Ascending order.
        DESC: Descending order.
    """

    ASC = "asc"
    DESC = "desc"


class MeetingProvider(str, Enum):
    """
    Enum representing the possible meeting providers for Notetaker.

    Values:
        GOOGLE_MEET: Google Meet meetings
        ZOOM: Zoom meetings
        MICROSOFT_TEAMS: Microsoft Teams meetings
    """

    GOOGLE_MEET = "Google Meet"
    ZOOM = "Zoom Meeting"
    MICROSOFT_TEAMS = "Microsoft Teams"


class NotetakerMeetingSettingsRequest(TypedDict):
    """
    Interface representing Notetaker meeting settings for request objects.

    Attributes:
        video_recording: When true, Notetaker records the meeting's video.
        audio_recording: When true, Notetaker records the meeting's audio.
        transcription: When true, Notetaker transcribes the meeting's audio.
            If transcription is true, audio_recording must also be true.
    """

    video_recording: Optional[bool]
    audio_recording: Optional[bool]
    transcription: Optional[bool]


@dataclass_json
@dataclass
class NotetakerMeetingSettings:
    """
    Class representing Notetaker meeting settings.

    Attributes:
        video_recording: When true, Notetaker records the meeting's video.
        audio_recording: When true, Notetaker records the meeting's audio.
        transcription: When true, Notetaker transcribes the meeting's audio.
            If transcription is true, audio_recording must also be true.
    """

    video_recording: bool = True
    audio_recording: bool = True
    transcription: bool = True


@dataclass_json
@dataclass
class NotetakerMediaRecording:
    """
    Class representing a Notetaker media recording.

    Attributes:
        size: The size of the file in bytes.
        name: The name of the file.
        type: The MIME type of the file.
        created_at: Unix timestamp when the file was uploaded to the storage server.
        expires_at: Unix timestamp when the file will be deleted.
        url: A link to download the file.
        ttl: Time-to-live in seconds until the file will be deleted off Nylas' storage server.
    """

    size: int
    name: str
    type: str
    created_at: int
    expires_at: int
    url: str
    ttl: int


@dataclass_json
@dataclass
class NotetakerMedia:
    """
    Class representing Notetaker media.

    Attributes:
        recording: The meeting recording (video/mp4).
        transcript: The meeting transcript (application/json).
    """

    recording: Optional[NotetakerMediaRecording] = None
    transcript: Optional[NotetakerMediaRecording] = None


@dataclass_json
@dataclass
class Notetaker:
    """
    Class representing a Nylas Notetaker.

    Attributes:
        id: The Notetaker ID.
        name: The display name for the Notetaker bot.
        join_time: When Notetaker joined the meeting, in Unix timestamp format.
        meeting_link: The meeting link.
        meeting_provider: The meeting provider.
        state: The current state of the Notetaker bot.
        meeting_settings: Notetaker Meeting Settings.
        message: A message describing the API response (only included in some responses).
    """

    id: str
    name: str
    join_time: int
    meeting_link: str
    state: NotetakerState
    meeting_settings: NotetakerMeetingSettings
    meeting_provider: Optional[MeetingProvider] = None
    message: Optional[str] = None
    object: str = "notetaker"

    def is_state(self, state: NotetakerState) -> bool:
        """
        Check if the notetaker is in a specific state.

        Args:
            state: The NotetakerState to check against.

        Returns:
            True if the notetaker is in the specified state, False otherwise.
        """
        return self.state == state

    def is_scheduled(self) -> bool:
        """Check if the notetaker is in the scheduled state."""
        return self.is_state(NotetakerState.SCHEDULED)

    def is_attending(self) -> bool:
        """Check if the notetaker is currently attending a meeting."""
        return self.is_state(NotetakerState.ATTENDING)

    def has_media_available(self) -> bool:
        """Check if the notetaker has media available for download."""
        return self.is_state(NotetakerState.MEDIA_AVAILABLE)


class InviteNotetakerRequest(TypedDict):
    """
    Interface representing the Nylas notetaker creation request.

    Attributes:
        meeting_link: A meeting invitation link that Notetaker uses to join the meeting.
        join_time: When Notetaker should join the meeting, in Unix timestamp format.
            If empty, Notetaker joins the meeting immediately.
        name: The display name for the Notetaker bot.
        meeting_settings: Notetaker Meeting Settings.
    """

    meeting_link: str
    join_time: NotRequired[int]
    name: NotRequired[str]
    meeting_settings: NotRequired[NotetakerMeetingSettingsRequest]


class UpdateNotetakerRequest(TypedDict):
    """
    Interface representing the Nylas notetaker update request.

    Attributes:
        join_time: When Notetaker should join the meeting, in Unix timestamp format.
        name: The display name for the Notetaker bot.
        meeting_settings: Notetaker Meeting Settings.
    """

    join_time: NotRequired[int]
    name: NotRequired[str]
    meeting_settings: NotRequired[NotetakerMeetingSettingsRequest]


class ListNotetakerQueryParams(ListQueryParams):
    """
    Interface representing the query parameters for listing notetakers.

    Attributes:
        state: Filter for Notetaker bots with the specified meeting state.
            Use the NotetakerState enum.
            Example: state=NotetakerState.SCHEDULED
        join_time_start: Filter for Notetaker bots that have join times that start at or after a specific time,
            in Unix timestamp format.
        join_time_end: Filter for Notetaker bots that have join times that end at or are before a specific time,
            in Unix timestamp format.
        limit: The maximum number of objects to return. This field defaults to 50. The maximum allowed value is 200.
        page_token: An identifier that specifies which page of data to return.
        prev_page_token: An identifier that specifies which page of data to return.
        order_by: The field to order the Notetaker bots by. Defaults to created_at.
            Use the NotetakerOrderBy enum.
            Example: order_by=NotetakerOrderBy.NAME
        order_direction: The direction to order the Notetaker bots by. Defaults to asc.
            Use the NotetakerOrderDirection enum.
            Example: order_direction=NotetakerOrderDirection.DESC
    """

    state: NotRequired[NotetakerState]
    join_time_start: NotRequired[int]
    join_time_end: NotRequired[int]
    order_by: NotRequired[NotetakerOrderBy]
    order_direction: NotRequired[NotetakerOrderDirection]

    def __post_init__(self):
        """Convert enums to string values for API requests."""
        super().__post_init__()
        # Convert state enum to string if present
        if hasattr(self, "state") and isinstance(self.state, NotetakerState):
            self.state = self.state.value
        # Convert order_by enum to string if present
        if hasattr(self, "order_by") and isinstance(self.order_by, NotetakerOrderBy):
            self.order_by = self.order_by.value
        # Convert order_direction enum to string if present
        if hasattr(self, "order_direction") and isinstance(
            self.order_direction, NotetakerOrderDirection
        ):
            self.order_direction = self.order_direction.value


class FindNotetakerQueryParams(TypedDict):
    """
    Interface representing the query parameters for finding a notetaker.

    Attributes:
        select: Comma-separated list of fields to return in the response.
            Use this to limit the fields returned in the response.
    """

    select: NotRequired[str]


@dataclass_json
@dataclass
class NotetakerLeaveResponse:
    """
    Class representing a Notetaker leave response.

    Attributes:
        id: The Notetaker ID.
        message: A message describing the API response.
    """

    id: str
    message: str
    object: str = "notetaker_leave_response"

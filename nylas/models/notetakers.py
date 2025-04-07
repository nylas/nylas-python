from dataclasses import dataclass
from typing import Optional, List
from enum import Enum

from dataclasses_json import dataclass_json
from typing_extensions import TypedDict, NotRequired

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


@dataclass_json
@dataclass
class NotetakerMeetingSettings:
    """
    Class representing Notetaker meeting settings.

    Attributes:
        video_recording: When true, Notetaker records the meeting's video.
        audio_recording: When true, Notetaker records the meeting's audio.
        transcription: When true, Notetaker transcribes the meeting's audio. If transcription is true, audio_recording must also be true.
    """
    video_recording: Optional[bool] = True
    audio_recording: Optional[bool] = True
    transcription: Optional[bool] = True


@dataclass_json
@dataclass
class NotetakerMediaRecording:
    """
    Class representing a Notetaker media recording.

    Attributes:
        url: A link to the meeting recording.
        size: The size of the file, in MB.
    """
    url: str
    size: int


@dataclass_json
@dataclass
class NotetakerMedia:
    """
    Class representing Notetaker media.

    Attributes:
        recording: The meeting recording.
        transcript: The meeting transcript.
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
    Class representation of the Nylas notetaker creation request.

    Attributes:
        meeting_link: A meeting invitation link that Notetaker uses to join the meeting.
        join_time: When Notetaker should join the meeting, in Unix timestamp format. If empty, Notetaker joins the meeting immediately.
        name: The display name for the Notetaker bot.
        meeting_settings: Notetaker Meeting Settings.
    """
    meeting_link: str
    join_time: NotRequired[int]
    name: NotRequired[str]
    meeting_settings: NotRequired[dict]


class UpdateNotetakerRequest(TypedDict):
    """
    Class representation of the Nylas notetaker update request.

    Attributes:
        join_time: When Notetaker should join the meeting, in Unix timestamp format.
        name: The display name for the Notetaker bot.
        meeting_settings: Notetaker Meeting Settings.
    """
    join_time: NotRequired[int]
    name: NotRequired[str]
    meeting_settings: NotRequired[dict]


class ListNotetakerQueryParams(ListQueryParams):
    """
    Interface representing the query parameters for listing notetakers.

    Attributes:
        state: Filter for Notetaker bots with the specified meeting state.
            Use the NotetakerState enum.
            Example: state=NotetakerState.SCHEDULED
        join_time_from: Filter for Notetaker bots that are scheduled to join meetings after the specified time.
        join_time_until: Filter for Notetaker bots that are scheduled to join meetings until the specified time.
        limit: The maximum number of objects to return. This field defaults to 50. The maximum allowed value is 200.
        page_token: An identifier that specifies which page of data to return.
        prev_page_token: An identifier that specifies which page of data to return.
    """
    state: NotRequired[NotetakerState]
    join_time_from: NotRequired[int]
    join_time_until: NotRequired[int]
    
    def __post_init__(self):
        """Convert NotetakerState enum to string value for API requests."""
        super().__post_init__()
        # Convert state enum to string if present
        if hasattr(self, 'state') and isinstance(self.state, NotetakerState):
            self.state = self.state.value


class FindNotetakerQueryParams(TypedDict):
    """
    Interface representing the query parameters for finding a notetaker.

    Attributes:
        select: Comma-separated list of fields to return in the response.
            Use this to limit the fields returned in the response.
    """
    select: NotRequired[str] 
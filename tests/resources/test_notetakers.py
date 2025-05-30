from nylas.resources.notetakers import Notetakers
from nylas.models.notetakers import (
    Notetaker,
    NotetakerMedia,
    NotetakerState,
    MeetingProvider,
    ListNotetakerQueryParams,
    NotetakerLeaveResponse,
    NotetakerOrderBy,
    NotetakerOrderDirection,
)


class TestNotetaker:
    def test_notetaker_deserialization(self):
        notetaker_json = {
            "id": "notetaker-123",
            "name": "Nylas Notetaker",
            "join_time": 1656090000,
            "meeting_link": "https://meet.google.com/abc-def-ghi",
            "meeting_provider": "Google Meet",
            "state": "scheduled",
            "object": "notetaker",
            "meeting_settings": {
                "video_recording": True,
                "audio_recording": True,
                "transcription": True,
            },
        }

        notetaker = Notetaker.from_dict(notetaker_json)

        assert notetaker.id == "notetaker-123"
        assert notetaker.name == "Nylas Notetaker"
        assert notetaker.join_time == 1656090000
        assert notetaker.meeting_link == "https://meet.google.com/abc-def-ghi"
        assert notetaker.meeting_provider == MeetingProvider.GOOGLE_MEET
        assert notetaker.state == NotetakerState.SCHEDULED
        assert notetaker.object == "notetaker"
        assert notetaker.meeting_settings.video_recording is True
        assert notetaker.meeting_settings.audio_recording is True
        assert notetaker.meeting_settings.transcription is True

    def test_notetaker_state_enum(self):
        """Test that the NotetakerState enum works correctly."""
        # Test all enum values
        states = [
            ("scheduled", NotetakerState.SCHEDULED),
            ("connecting", NotetakerState.CONNECTING),
            ("waiting_for_entry", NotetakerState.WAITING_FOR_ENTRY),
            ("failed_entry", NotetakerState.FAILED_ENTRY),
            ("attending", NotetakerState.ATTENDING),
            ("media_processing", NotetakerState.MEDIA_PROCESSING),
            ("media_available", NotetakerState.MEDIA_AVAILABLE),
            ("media_error", NotetakerState.MEDIA_ERROR),
            ("media_deleted", NotetakerState.MEDIA_DELETED),
        ]

        for state_str, state_enum in states:
            notetaker_json = {
                "id": "notetaker-123",
                "name": "Nylas Notetaker",
                "join_time": 1656090000,
                "meeting_link": "https://meet.google.com/abc-def-ghi",
                "state": state_str,
                "meeting_settings": {
                    "video_recording": True,
                    "audio_recording": True,
                    "transcription": True,
                },
            }

            notetaker = Notetaker.from_dict(notetaker_json)
            assert notetaker.state == state_enum
            assert notetaker.state.value == state_str

    def test_list_notetakers(self, http_client_list_response):
        notetakers = Notetakers(http_client_list_response)

        notetakers.list(identifier="abc-123", query_params=None)

        http_client_list_response._execute.assert_called_once_with(
            "GET",
            "/v3/grants/abc-123/notetakers",
            None,
            None,
            None,
            overrides=None,
        )

    def test_list_notetakers_without_identifier(self, http_client_list_response):
        notetakers = Notetakers(http_client_list_response)

        notetakers.list(query_params=None)

        http_client_list_response._execute.assert_called_once_with(
            "GET", "/v3/notetakers", None, None, None, overrides=None
        )

    def test_list_notetakers_with_query_params(self, http_client_list_response):
        notetakers = Notetakers(http_client_list_response)

        notetakers.list(
            identifier="abc-123",
            query_params={"state": NotetakerState.SCHEDULED, "limit": 20},
        )

        http_client_list_response._execute.assert_called_once_with(
            "GET",
            "/v3/grants/abc-123/notetakers",
            None,
            {"state": "scheduled", "limit": 20},
            None,
            overrides=None,
        )

    def test_list_notetakers_with_enum_query_params(self, http_client_list_response):
        """Test that the NotetakerState enum can be used directly in query params."""
        notetakers = Notetakers(http_client_list_response)

        # Create query params using the enum directly
        query_params = ListNotetakerQueryParams(
            state=NotetakerState.SCHEDULED, limit=20
        )

        notetakers.list(identifier="abc-123", query_params=query_params)

        # Verify the enum is converted to string in the API call
        http_client_list_response._execute.assert_called_once_with(
            "GET",
            "/v3/grants/abc-123/notetakers",
            None,
            {"state": "scheduled", "limit": 20},
            None,
            overrides=None,
        )

    def test_find_notetaker(self, http_client_response):
        notetakers = Notetakers(http_client_response)

        notetakers.find(identifier="abc-123", notetaker_id="notetaker-123")

        http_client_response._execute.assert_called_once_with(
            "GET",
            "/v3/grants/abc-123/notetakers/notetaker-123",
            None,
            None,
            None,
            overrides=None,
        )

    def test_find_notetaker_without_identifier(self, http_client_response):
        notetakers = Notetakers(http_client_response)

        notetakers.find(notetaker_id="notetaker-123")

        http_client_response._execute.assert_called_once_with(
            "GET",
            "/v3/notetakers/notetaker-123",
            None,
            None,
            None,
            overrides=None,
        )

    def test_invite_notetaker(self, http_client_response):
        notetakers = Notetakers(http_client_response)
        request_body = {
            "meeting_link": "https://meet.google.com/abc-def-ghi",
            "join_time": 1656090000,
            "name": "Custom Notetaker",
            "meeting_settings": {
                "video_recording": True,
                "audio_recording": True,
                "transcription": True,
            },
        }

        notetakers.invite(identifier="abc-123", request_body=request_body)

        http_client_response._execute.assert_called_once_with(
            "POST",
            "/v3/grants/abc-123/notetakers",
            None,
            None,
            request_body,
            overrides=None,
        )

    def test_invite_notetaker_without_identifier(self, http_client_response):
        notetakers = Notetakers(http_client_response)
        request_body = {
            "meeting_link": "https://meet.google.com/abc-def-ghi",
            "join_time": 1656090000,
            "name": "Custom Notetaker",
            "meeting_settings": {
                "video_recording": True,
                "audio_recording": True,
                "transcription": True,
            },
        }

        notetakers.invite(request_body=request_body)

        http_client_response._execute.assert_called_once_with(
            "POST",
            "/v3/notetakers",
            None,
            None,
            request_body,
            overrides=None,
        )

    def test_update_notetaker(self, http_client_response):
        notetakers = Notetakers(http_client_response)
        request_body = {
            "name": "Updated Notetaker",
            "join_time": 1656100000,
            "meeting_settings": {
                "video_recording": False,
                "audio_recording": True,
                "transcription": True,
            },
        }

        notetakers.update(
            identifier="abc-123",
            notetaker_id="notetaker-123",
            request_body=request_body,
        )

        http_client_response._execute.assert_called_once_with(
            "PATCH",
            "/v3/grants/abc-123/notetakers/notetaker-123",
            None,
            None,
            request_body,
            overrides=None,
        )

    def test_update_notetaker_without_identifier(self, http_client_response):
        notetakers = Notetakers(http_client_response)
        request_body = {"name": "Updated Notetaker", "join_time": 1656100000}

        notetakers.update(
            notetaker_id="notetaker-123",
            request_body=request_body,
        )

        http_client_response._execute.assert_called_once_with(
            "PATCH",
            "/v3/notetakers/notetaker-123",
            None,
            None,
            request_body,
            overrides=None,
        )

    def test_leave_meeting(self, http_client_response):
        notetakers = Notetakers(http_client_response)

        notetakers.leave(
            identifier="abc-123",
            notetaker_id="notetaker-123",
        )

        http_client_response._execute.assert_called_once_with(
            "POST",
            "/v3/grants/abc-123/notetakers/notetaker-123/leave",
            None,
            None,
            None,
            overrides=None,
        )

    def test_leave_meeting_without_identifier(self, http_client_response):
        notetakers = Notetakers(http_client_response)

        notetakers.leave(
            notetaker_id="notetaker-123",
        )

        http_client_response._execute.assert_called_once_with(
            "POST",
            "/v3/notetakers/notetaker-123/leave",
            None,
            None,
            None,
            overrides=None,
        )

    def test_get_media(self, http_client_response):
        notetakers = Notetakers(http_client_response)

        notetakers.get_media(
            identifier="abc-123",
            notetaker_id="notetaker-123",
        )

        http_client_response._execute.assert_called_once_with(
            "GET",
            "/v3/grants/abc-123/notetakers/notetaker-123/media",
            None,
            None,
            None,
            overrides=None,
        )

    def test_get_media_without_identifier(self, http_client_response):
        notetakers = Notetakers(http_client_response)

        notetakers.get_media(
            notetaker_id="notetaker-123",
        )

        http_client_response._execute.assert_called_once_with(
            "GET",
            "/v3/notetakers/notetaker-123/media",
            None,
            None,
            None,
            overrides=None,
        )

    def test_cancel_notetaker(self, http_client_delete_response):
        notetakers = Notetakers(http_client_delete_response)

        notetakers.cancel(
            identifier="abc-123",
            notetaker_id="notetaker-123",
        )

        http_client_delete_response._execute.assert_called_once_with(
            "DELETE",
            "/v3/grants/abc-123/notetakers/notetaker-123/cancel",
            None,
            None,
            None,
            overrides=None,
        )

    def test_cancel_notetaker_without_identifier(self, http_client_delete_response):
        notetakers = Notetakers(http_client_delete_response)

        notetakers.cancel(
            notetaker_id="notetaker-123",
        )

        http_client_delete_response._execute.assert_called_once_with(
            "DELETE",
            "/v3/notetakers/notetaker-123/cancel",
            None,
            None,
            None,
            overrides=None,
        )

    def test_media_deserialization(self):
        media_json = {
            "recording": {
                "size": 21550491,
                "name": "meeting_recording.mp4",
                "type": "video/mp4",
                "created_at": 1744222418,
                "expires_at": 1744481618,
                "url": "url_for_recording",
                "ttl": 259106,
            },
            "transcript": {
                "size": 862,
                "name": "raw_transcript.json",
                "type": "application/json",
                "created_at": 1744222418,
                "expires_at": 1744481618,
                "url": "url_for_transcript",
                "ttl": 259106,
            },
        }

        media = NotetakerMedia.from_dict(media_json)

        assert media.recording.url == "url_for_recording"
        assert media.recording.size == 21550491
        assert media.recording.name == "meeting_recording.mp4"
        assert media.recording.type == "video/mp4"
        assert media.recording.created_at == 1744222418
        assert media.recording.expires_at == 1744481618
        assert media.recording.ttl == 259106

        assert media.transcript.url == "url_for_transcript"
        assert media.transcript.size == 862
        assert media.transcript.name == "raw_transcript.json"
        assert media.transcript.type == "application/json"
        assert media.transcript.created_at == 1744222418
        assert media.transcript.expires_at == 1744481618
        assert media.transcript.ttl == 259106

    def test_meeting_provider_enum(self):
        """Test that the MeetingProvider enum works correctly."""
        # Test all enum values
        providers = [
            ("Google Meet", MeetingProvider.GOOGLE_MEET),
            ("Zoom Meeting", MeetingProvider.ZOOM),
            ("Microsoft Teams", MeetingProvider.MICROSOFT_TEAMS),
        ]

        for provider_str, provider_enum in providers:
            notetaker_json = {
                "id": "notetaker-123",
                "name": "Nylas Notetaker",
                "join_time": 1656090000,
                "meeting_link": "https://meet.example.com",
                "meeting_provider": provider_str,
                "state": "scheduled",
                "meeting_settings": {
                    "video_recording": True,
                    "audio_recording": True,
                    "transcription": True,
                },
            }

            notetaker = Notetaker.from_dict(notetaker_json)
            assert notetaker.meeting_provider == provider_enum
            assert notetaker.meeting_provider.value == provider_str

    def test_state_enum_comparison(self):
        """Test that enum values can be compared directly."""
        # Create a notetaker with a state enum
        notetaker_json = {
            "id": "notetaker-123",
            "name": "Nylas Notetaker",
            "join_time": 1656090000,
            "meeting_link": "https://meet.google.com/abc-def-ghi",
            "state": "scheduled",
            "meeting_settings": {
                "video_recording": True,
                "audio_recording": True,
                "transcription": True,
            },
        }

        notetaker = Notetaker.from_dict(notetaker_json)

        # Check direct comparison with enum
        assert notetaker.state == NotetakerState.SCHEDULED

        # Value of the enum matches original string
        assert notetaker.state.value == "scheduled"

    def test_meeting_provider_enum_comparison(self):
        """Test that meeting provider enum values can be compared directly."""
        # Create a notetaker with a meeting provider enum
        notetaker_json = {
            "id": "notetaker-123",
            "name": "Nylas Notetaker",
            "join_time": 1656090000,
            "meeting_link": "https://meet.google.com/abc-def-ghi",
            "meeting_provider": "Google Meet",
            "state": "scheduled",
            "meeting_settings": {
                "video_recording": True,
                "audio_recording": True,
                "transcription": True,
            },
        }

        notetaker = Notetaker.from_dict(notetaker_json)

        # Check direct comparison with enum
        assert notetaker.meeting_provider == MeetingProvider.GOOGLE_MEET

        # Value of the enum matches original string
        assert notetaker.meeting_provider.value == "Google Meet"

    def test_notetaker_helper_methods(self):
        """Test the helper methods for checking state and provider."""
        # Test with a scheduled notetaker
        scheduled_notetaker = Notetaker.from_dict(
            {
                "id": "notetaker-123",
                "name": "Nylas Notetaker",
                "join_time": 1656090000,
                "meeting_link": ("https://meet.google.com/abc-def-ghi"),
                "meeting_provider": "Google Meet",
                "state": "scheduled",
                "meeting_settings": {
                    "video_recording": True,
                    "audio_recording": True,
                    "transcription": True,
                },
            }
        )

        assert scheduled_notetaker.is_state(NotetakerState.SCHEDULED) is True
        assert scheduled_notetaker.is_scheduled() is True
        assert scheduled_notetaker.is_attending() is False
        assert scheduled_notetaker.has_media_available() is False

        # Test with an attending notetaker
        attending_notetaker = Notetaker.from_dict(
            {
                "id": "notetaker-456",
                "name": "Nylas Notetaker",
                "join_time": 1656090000,
                "meeting_link": "https://zoom.us/j/123456789",
                "meeting_provider": "Zoom Meeting",
                "state": "attending",
                "meeting_settings": {
                    "video_recording": True,
                    "audio_recording": True,
                    "transcription": True,
                },
            }
        )

        assert attending_notetaker.is_state(NotetakerState.ATTENDING) is True
        assert attending_notetaker.is_scheduled() is False
        assert attending_notetaker.is_attending() is True
        assert attending_notetaker.has_media_available() is False

        # Test with a media available notetaker
        media_available_notetaker = Notetaker.from_dict(
            {
                "id": "notetaker-789",
                "name": "Nylas Notetaker",
                "join_time": 1656090000,
                "meeting_link": ("https://teams.microsoft.com/l/meetup-join/123"),
                "meeting_provider": "Microsoft Teams",
                "state": "media_available",
                "meeting_settings": {
                    "video_recording": True,
                    "audio_recording": True,
                    "transcription": True,
                },
            }
        )

        assert (
            media_available_notetaker.is_state(NotetakerState.MEDIA_AVAILABLE) is True
        )
        assert media_available_notetaker.is_scheduled() is False
        assert media_available_notetaker.is_attending() is False
        assert media_available_notetaker.has_media_available() is True

    def test_list_notetakers_with_time_filters(self, http_client_list_response):
        """Test that join_time_start and join_time_end query parameters work correctly."""
        # Using Unix timestamps for Jan 1, 2024 and Jan 2, 2024
        start_time = 1704067200  # Jan 1, 2024
        end_time = 1704153600  # Jan 2, 2024

        # Create query params with time filters
        query_params = ListNotetakerQueryParams(
            join_time_start=start_time, join_time_end=end_time, limit=20
        )

        notetakers = Notetakers(http_client_list_response)

        notetakers.list(identifier="abc-123", query_params=query_params)

        # Verify the API call includes the time filter parameters
        http_client_list_response._execute.assert_called_once_with(
            "GET",
            "/v3/grants/abc-123/notetakers",
            None,
            {
                "join_time_start": start_time,
                "join_time_end": end_time,
                "limit": 20,
            },
            None,
            overrides=None,
        )

    def test_notetaker_leave_response_deserialization(self):
        """Test deserialization of the NotetakerLeaveResponse model."""
        leave_response_json = {
            "id": "notetaker-123",
            "message": "Notetaker has left the meeting",
            "object": "notetaker_leave_response",
        }

        leave_response = NotetakerLeaveResponse.from_dict(leave_response_json)

        assert leave_response.id == "notetaker-123"
        assert leave_response.message == "Notetaker has left the meeting"
        assert leave_response.object == "notetaker_leave_response"

    def test_list_notetakers_with_order_params(self, http_client_list_response):
        notetakers = Notetakers(http_client_list_response)

        notetakers.list(
            identifier="abc-123",
            query_params={
                "order_by": NotetakerOrderBy.NAME,
                "order_direction": NotetakerOrderDirection.DESC,
            },
        )

        http_client_list_response._execute.assert_called_once_with(
            "GET",
            "/v3/grants/abc-123/notetakers",
            None,
            {"order_by": "name", "order_direction": "desc"},
            None,
            overrides=None,
        )

    def test_list_notetakers_with_default_order(self, http_client_list_response):
        notetakers = Notetakers(http_client_list_response)

        notetakers.list(identifier="abc-123")

        http_client_list_response._execute.assert_called_once_with(
            "GET",
            "/v3/grants/abc-123/notetakers",
            None,
            None,
            None,
            overrides=None,
        )

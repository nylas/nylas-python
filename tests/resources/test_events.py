import json
from unittest.mock import Mock, patch

import pytest

from nylas.resources.events import Events
from nylas.models.errors import NylasApiError
from nylas.models.events import Event
from nylas.models.events_batch import (
    BatchCreateEventOperation,
    BatchUpdateEventOperation,
    BatchDeleteEventOperation,
)


class TestEvent:
    def test_event_deserialization(self):
        event_json = {
            "busy": True,
            "calendar_id": "7d93zl2palhxqdy6e5qinsakt",
            "conferencing": {
                "provider": "Zoom Meeting",
                "details": {
                    "meeting_code": "code-123456",
                    "password": "password-123456",
                    "url": "https://zoom.us/j/1234567890?pwd=1234567890",
                },
            },
            "created_at": 1661874192,
            "description": "Description of my new calendar",
            "hide_participants": False,
            "grant_id": "41009df5-bf11-4c97-aa18-b285b5f2e386",
            "html_link": "https://www.google.com/calendar/event?eid=bTMzcGJrNW4yYjk4bjk3OWE4Ef3feD2VuM29fMjAyMjA2MjdUMjIwMDAwWiBoYWxsYUBueWxhcy5jb20",
            "id": "5d3qmne77v32r8l4phyuksl2x_20240603T180000Z",
            "master_event_id": "5d3qmne77v32r8l4phyuksl2x",
            "location": "Roller Rink",
            "metadata": {"your_key": "your_value"},
            "object": "event",
            "organizer": {"email": "organizer@example.com", "name": ""},
            "participants": [
                {
                    "comment": "Aristotle",
                    "email": "aristotle@example.com",
                    "name": "Aristotle",
                    "phone_number": "+1 23456778",
                    "status": "maybe",
                }
            ],
            "resources": [
                {
                    "email": "room-a@example.com",
                    "name": "Conference Room A",
                    "capacity": 10,
                    "building": "Headquarters",
                    "floor_name": "Main",
                    "floor_section": "West Wing",
                    "floor_number": 3,
                }
            ],
            "read_only": False,
            "reminders": {
                "use_default": False,
                "overrides": [{"reminder_minutes": 10, "reminder_method": "email"}],
            },
            "recurrence": ["RRULE:FREQ=WEEKLY;BYDAY=MO", "EXDATE:20211011T000000Z"],
            "status": "confirmed",
            "title": "Birthday Party",
            "updated_at": 1661874192,
            "visibility": "private",
            "when": {
                "start_time": 1661874192,
                "end_time": 1661877792,
                "start_timezone": "America/New_York",
                "end_timezone": "America/New_York",
                "object": "timespan",
            },
        }

        event = Event.from_dict(event_json)

        assert event.busy is True
        assert event.calendar_id == "7d93zl2palhxqdy6e5qinsakt"
        assert event.conferencing.provider == "Zoom Meeting"
        assert event.conferencing.details["meeting_code"] == "code-123456"
        assert event.conferencing.details["password"] == "password-123456"
        assert (
            event.conferencing.details["url"]
            == "https://zoom.us/j/1234567890?pwd=1234567890"
        )
        assert event.created_at == 1661874192
        assert event.description == "Description of my new calendar"
        assert event.hide_participants is False
        assert event.grant_id == "41009df5-bf11-4c97-aa18-b285b5f2e386"
        assert (
            event.html_link
            == "https://www.google.com/calendar/event?eid=bTMzcGJrNW4yYjk4bjk3OWE4Ef3feD2VuM29fMjAyMjA2MjdUMjIwMDAwWiBoYWxsYUBueWxhcy5jb20"
        )
        assert event.id == "5d3qmne77v32r8l4phyuksl2x_20240603T180000Z"
        assert event.master_event_id == "5d3qmne77v32r8l4phyuksl2x"
        assert event.location == "Roller Rink"
        assert event.metadata == {"your_key": "your_value"}
        assert event.object == "event"
        assert event.participants[0].comment == "Aristotle"
        assert event.participants[0].email == "aristotle@example.com"
        assert event.participants[0].name == "Aristotle"
        assert event.participants[0].phone_number == "+1 23456778"
        assert event.participants[0].status == "maybe"
        assert event.resources[0].email == "room-a@example.com"
        assert event.resources[0].name == "Conference Room A"
        assert event.resources[0].capacity == 10
        assert event.resources[0].building == "Headquarters"
        assert event.resources[0].floor_name == "Main"
        assert event.resources[0].floor_section == "West Wing"
        assert event.resources[0].floor_number == 3
        assert event.read_only is False
        assert event.reminders.use_default is False
        assert event.reminders.overrides[0].reminder_minutes == 10
        assert event.reminders.overrides[0].reminder_method == "email"
        assert event.recurrence[0] == "RRULE:FREQ=WEEKLY;BYDAY=MO"
        assert event.recurrence[1] == "EXDATE:20211011T000000Z"
        assert event.status == "confirmed"
        assert event.title == "Birthday Party"
        assert event.updated_at == 1661874192
        assert event.visibility == "private"
        assert event.when.start_time == 1661874192
        assert event.when.end_time == 1661877792
        assert event.when.start_timezone == "America/New_York"
        assert event.when.end_timezone == "America/New_York"
        assert event.when.object == "timespan"

    def test_list_events(self, http_client_list_response):
        events = Events(http_client_list_response)

        events.list(
            identifier="abc-123",
            query_params={
                "calendar_id": "abc-123",
                "limit": 20,
            },
        )

        http_client_list_response._execute.assert_called_once_with(
            "GET",
            "/v3/grants/abc-123/events",
            None,
            {
                "calendar_id": "abc-123",
                "limit": 20,
            },
            None,
            overrides=None,
        )

    def test_list_events_with_query_params(self, http_client_list_response):
        events = Events(http_client_list_response)

        events.list(identifier="abc-123", query_params={"limit": 20})

        http_client_list_response._execute.assert_called_once_with(
            "GET",
            "/v3/grants/abc-123/events",
            None,
            {"limit": 20},
            None,
            overrides=None,
        )

    def test_list_events_with_select_param(self, http_client_list_response):
        events = Events(http_client_list_response)

        # Set up mock response data
        http_client_list_response._execute.return_value = {
            "request_id": "abc-123",
            "data": [{
                "id": "event-123",
                "title": "Team Meeting",
                "description": "Weekly team sync",
                "when": {
                    "start_time": 1625097600,
                    "end_time": 1625101200
                }
            }]
        }

        # Call the API method
        result = events.list(
            identifier="abc-123",
            query_params={
                "select": "id,title,description,when"
            }
        )

        # Verify API call
        http_client_list_response._execute.assert_called_with(
            "GET",
            "/v3/grants/abc-123/events",
            None,
            {"select": "id,title,description,when"},
            None,
            overrides=None,
        )

        # The actual response validation is handled by the mock in conftest.py
        assert result is not None

    def test_list_import_events(self, http_client_list_response):
        events = Events(http_client=http_client_list_response)
        events.list_import_events(
            identifier="grant-123",
            query_params={"calendar_id": "primary"},
        )

        http_client_list_response._execute.assert_called_once_with(
            "GET",
            "/v3/grants/grant-123/events/import",
            None,
            {"calendar_id": "primary"},
            None,
            overrides=None,
        )

    def test_list_import_events_with_select_param(self, http_client_list_response):
        events = Events(http_client=http_client_list_response)
        events.list_import_events(
            identifier="grant-123",
            query_params={"calendar_id": "primary", "select": "id,title,participants"},
        )

        http_client_list_response._execute.assert_called_once_with(
            "GET",
            "/v3/grants/grant-123/events/import",
            None,
            {"calendar_id": "primary", "select": "id,title,participants"},
            None,
            overrides=None,
        )
        
    def test_list_import_events_with_limit(self, http_client_list_response):
        events = Events(http_client=http_client_list_response)
        events.list_import_events(
            identifier="grant-123",
            query_params={"calendar_id": "primary", "limit": 100},
        )

        http_client_list_response._execute.assert_called_once_with(
            "GET",
            "/v3/grants/grant-123/events/import",
            None,
            {"calendar_id": "primary", "limit": 100},
            None,
            overrides=None,
        )
        
    def test_list_import_events_with_time_filters(self, http_client_list_response):
        events = Events(http_client=http_client_list_response)
        # Using Unix timestamps for Jan 1, 2023 and Dec 31, 2023
        start_time = 1672531200  # Jan 1, 2023
        end_time = 1704067199  # Dec 31, 2023
        
        events.list_import_events(
            identifier="grant-123",
            query_params={
                "calendar_id": "primary",
                "start": start_time,
                "end": end_time
            },
        )

        http_client_list_response._execute.assert_called_once_with(
            "GET",
            "/v3/grants/grant-123/events/import",
            None,
            {
                "calendar_id": "primary",
                "start": start_time,
                "end": end_time
            },
            None,
            overrides=None,
        )
        
    def test_list_import_events_with_all_params(self, http_client_list_response):
        events = Events(http_client=http_client_list_response)
        # Using Unix timestamps for Jan 1, 2023 and Dec 31, 2023
        start_time = 1672531200  # Jan 1, 2023
        end_time = 1704067199  # Dec 31, 2023
        
        events.list_import_events(
            identifier="grant-123",
            query_params={
                "calendar_id": "primary",
                "limit": 50,
                "start": start_time,
                "end": end_time,
                "select": "id,title,participants,when",
                "page_token": "next-page-token-123"
            },
        )

        http_client_list_response._execute.assert_called_once_with(
            "GET",
            "/v3/grants/grant-123/events/import",
            None,
            {
                "calendar_id": "primary",
                "limit": 50,
                "start": start_time,
                "end": end_time,
                "select": "id,title,participants,when",
                "page_token": "next-page-token-123"
            },
            None,
            overrides=None,
        )

    def test_find_event(self, http_client_response):
        events = Events(http_client_response)

        events.find(
            identifier="abc-123",
            event_id="event-123",
            query_params={"calendar_id": "abc-123"},
        )

        http_client_response._execute.assert_called_once_with(
            "GET",
            "/v3/grants/abc-123/events/event-123",
            None,
            {"calendar_id": "abc-123"},
            None,
            overrides=None,
        )

    def test_find_event_with_select_param(self, http_client_response):
        events = Events(http_client_response)

        # Set up mock response data
        http_client_response._execute.return_value = ({
            "request_id": "abc-123",
            "data": {
                "id": "event-123",
                "title": "Team Meeting",
                "description": "Weekly team sync",
                "when": {
                    "start_time": 1625097600,
                    "end_time": 1625101200
                }
            }
        }, {"X-Test-Header": "test"})

        # Call the API method
        result = events.find(
            identifier="abc-123",
            event_id="event-123",
            query_params={
                "calendar_id": "abc-123",
                "select": "id,title,description,when"
            }
        )

        # Verify API call
        http_client_response._execute.assert_called_with(
            "GET",
            "/v3/grants/abc-123/events/event-123",
            None,
            {
                "calendar_id": "abc-123",
                "select": "id,title,description,when"
            },
            None,
            overrides=None,
        )

        # The actual response validation is handled by the mock in conftest.py
        assert result is not None

    def test_create_event(self, http_client_response):
        events = Events(http_client_response)
        request_body = {
            "when": {
                "start_time": 1661874192,
                "end_time": 1661877792,
                "start_timezone": "America/New_York",
                "end_timezone": "America/New_York",
            },
            "description": "Description of my new event",
            "location": "Los Angeles, CA",
            "metadata": {"your-key": "value"},
            "resources": [
                {
                    "email": "room-a@example.com",
                    "name": "Conference Room A",
                    "capacity": 10,
                    "building": "Headquarters",
                    "floor_name": "Main",
                    "floor_section": "West Wing",
                    "floor_number": 3,
                }
            ],
        }

        events.create(
            identifier="abc-123",
            request_body=request_body,
            query_params={"calendar_id": "abc-123"},
        )

        http_client_response._execute.assert_called_once_with(
            "POST",
            "/v3/grants/abc-123/events",
            None,
            {"calendar_id": "abc-123"},
            request_body,
            overrides=None,
        )

    def test_update_event(self, http_client_response):
        events = Events(http_client_response)
        request_body = {
            "when": {
                "start_time": 1661874192,
                "end_time": 1661877792,
                "start_timezone": "America/New_York",
                "end_timezone": "America/New_York",
            },
            "description": "Updated description of my event",
            "location": "Los Angeles, CA",
            "metadata": {"your-key": "value"},
            "resources": [
                {
                    "email": "room-a@example.com",
                    "name": "Conference Room A",
                    "capacity": 10,
                    "building": "Headquarters",
                    "floor_name": "Main",
                    "floor_section": "West Wing",
                    "floor_number": 3,
                }
            ],
        }

        events.update(
            identifier="abc-123",
            event_id="event-123",
            request_body=request_body,
            query_params={"calendar_id": "abc-123"},
        )

        http_client_response._execute.assert_called_once_with(
            "PUT",
            "/v3/grants/abc-123/events/event-123",
            None,
            {"calendar_id": "abc-123"},
            request_body,
            overrides=None,
        )

    def test_destroy_event(self, http_client_delete_response):
        events = Events(http_client_delete_response)

        events.destroy(
            identifier="abc-123",
            event_id="event-123",
            query_params={"calendar_id": "abc-123"},
        )

        http_client_delete_response._execute.assert_called_once_with(
            "DELETE",
            "/v3/grants/abc-123/events/event-123",
            None,
            {"calendar_id": "abc-123"},
            None,
            overrides=None,
        )

    def test_send_rsvp(self, http_client_response):
        events = Events(http_client_response)
        request_body = {"status": "yes"}

        events.send_rsvp(
            identifier="abc-123",
            event_id="event-123",
            request_body=request_body,
            query_params={"calendar_id": "abc-123"},
        )

        http_client_response._execute.assert_called_once_with(
            method="POST",
            path="/v3/grants/abc-123/events/event-123/send-rsvp",
            request_body=request_body,
            query_params={"calendar_id": "abc-123"},
            overrides=None,
        )

    def test_event_with_notetaker_deserialization(self):
        event_json = {
            "id": "event-123",
            "grant_id": "grant-123",
            "calendar_id": "calendar-123",
            "busy": True,
            "participants": [
                {"email": "test@example.com", "name": "Test User", "status": "yes"}
            ],
            "when": {
                "start_time": 1497916800,
                "end_time": 1497920400,
                "object": "timespan"
            },
            "title": "Test Event with Notetaker",
            "notetaker": {
                "id": "notetaker-123",
                "name": "Custom Notetaker",
                "meeting_settings": {
                    "video_recording": True,
                    "audio_recording": True,
                    "transcription": True
                }
            }
        }

        event = Event.from_dict(event_json)

        assert event.id == "event-123"
        assert event.grant_id == "grant-123"
        assert event.calendar_id == "calendar-123"
        assert event.busy is True
        assert event.title == "Test Event with Notetaker"
        assert event.notetaker is not None
        assert event.notetaker.id == "notetaker-123"
        assert event.notetaker.name == "Custom Notetaker"
        assert event.notetaker.meeting_settings is not None
        assert event.notetaker.meeting_settings.video_recording is True
        assert event.notetaker.meeting_settings.audio_recording is True
        assert event.notetaker.meeting_settings.transcription is True

    def test_create_event_with_notetaker(self, http_client_response):
        events = Events(http_client_response)
        request_body = {
            "title": "Test Event with Notetaker",
            "when": {
                "start_time": 1497916800,
                "end_time": 1497920400
            },
            "participants": [
                {"email": "test@example.com", "name": "Test User"}
            ],
            "notetaker": {
                "name": "Custom Notetaker",
                "meeting_settings": {
                    "video_recording": True,
                    "audio_recording": True,
                    "transcription": True
                }
            }
        }
        query_params = {"calendar_id": "calendar-123"}

        events.create(
            identifier="abc-123",
            request_body=request_body,
            query_params=query_params
        )

        http_client_response._execute.assert_called_once_with(
            "POST",
            "/v3/grants/abc-123/events",
            None,
            query_params,
            request_body,
            overrides=None,
        )

    def test_update_event_with_notetaker(self, http_client_response):
        events = Events(http_client_response)
        request_body = {
            "title": "Updated Test Event",
            "notetaker": {
                "id": "notetaker-123",
                "name": "Updated Notetaker",
                "meeting_settings": {
                    "video_recording": False,
                    "audio_recording": True,
                    "transcription": False
                }
            }
        }
        query_params = {"calendar_id": "calendar-123"}

        events.update(
            identifier="abc-123",
            event_id="event-123",
            request_body=request_body,
            query_params=query_params
        )

        http_client_response._execute.assert_called_once_with(
            "PUT",
            "/v3/grants/abc-123/events/event-123",
            None,
            query_params,
            request_body,
            overrides=None,
        )

    def test_event_with_empty_conferencing_deserialization(self):
        """Test event deserialization with empty conferencing object."""
        event_json = {
            "id": "test-event-id",
            "grant_id": "test-grant-id",
            "calendar_id": "test-calendar-id",
            "busy": True,
            "participants": [
                {"email": "test@example.com", "name": "Test User", "status": "yes"}
            ],
            "when": {
                "start_time": 1497916800,
                "end_time": 1497920400,
                "object": "timespan"
            },
            "conferencing": {},  # Empty conferencing object
            "title": "Test Event with Empty Conferencing"
        }

        event = Event.from_dict(event_json)
        
        assert event.id == "test-event-id"
        assert event.title == "Test Event with Empty Conferencing"
        assert event.conferencing is None

    def test_event_with_incomplete_conferencing_details_deserialization(self):
        """Test event deserialization with conferencing details missing provider."""
        event_json = {
            "id": "test-event-id",
            "grant_id": "test-grant-id",
            "calendar_id": "test-calendar-id",
            "busy": True,
            "participants": [
                {"email": "test@example.com", "name": "Test User", "status": "yes"}
            ],
            "when": {
                "start_time": 1497916800,
                "end_time": 1497920400,
                "object": "timespan"
            },
            "conferencing": {
                "details": {
                    "meeting_code": "code-123456",
                    "password": "password-123456",
                    "url": "https://zoom.us/j/1234567890?pwd=1234567890",
                }
            },  # Details without provider
            "title": "Test Event with Incomplete Conferencing Details"
        }

        event = Event.from_dict(event_json)
        
        assert event.id == "test-event-id"
        assert event.title == "Test Event with Incomplete Conferencing Details"
        assert event.conferencing is None

    def test_event_with_incomplete_conferencing_autocreate_deserialization(self):
        """Test event deserialization with conferencing autocreate missing provider."""
        event_json = {
            "id": "test-event-id",
            "grant_id": "test-grant-id",
            "calendar_id": "test-calendar-id",
            "busy": True,
            "participants": [
                {"email": "test@example.com", "name": "Test User", "status": "yes"}
            ],
            "when": {
                "start_time": 1497916800,
                "end_time": 1497920400,
                "object": "timespan"
            },
            "conferencing": {
                "autocreate": {}
            },  # Autocreate without provider
            "title": "Test Event with Incomplete Conferencing Autocreate"
        }

        event = Event.from_dict(event_json)
        
        assert event.id == "test-event-id"
        assert event.title == "Test Event with Incomplete Conferencing Autocreate"
        assert event.conferencing is None

    def test_event_with_unknown_conferencing_fields_deserialization(self):
        """Test event deserialization with conferencing containing unknown fields."""
        event_json = {
            "id": "test-event-id",
            "grant_id": "test-grant-id",
            "calendar_id": "test-calendar-id",
            "busy": True,
            "participants": [
                {"email": "test@example.com", "name": "Test User", "status": "yes"}
            ],
            "when": {
                "start_time": 1497916800,
                "end_time": 1497920400,
                "object": "timespan"
            },
            "conferencing": {
                "unknown_field": "value"
            },  # Unknown conferencing fields
            "title": "Test Event with Unknown Conferencing Fields"
        }

        event = Event.from_dict(event_json)
        
        assert event.id == "test-event-id"
        assert event.title == "Test Event with Unknown Conferencing Fields"
        assert event.conferencing is None

    def test_event_without_resources_deserialization(self):
        """Test event deserialization when the resources field is absent."""
        event_json = {
            "id": "test-event-id",
            "grant_id": "test-grant-id",
            "calendar_id": "test-calendar-id",
            "busy": True,
            "participants": [
                {"email": "test@example.com", "name": "Test User", "status": "yes"}
            ],
            "when": {
                "start_time": 1497916800,
                "end_time": 1497920400,
                "object": "timespan",
            },
            "title": "Test Event without Resources",
        }

        event = Event.from_dict(event_json)

        assert event.id == "test-event-id"
        assert event.resources is None

    def test_event_with_empty_resources_deserialization(self):
        """Test event deserialization when the resources field is an empty list."""
        event_json = {
            "id": "test-event-id",
            "grant_id": "test-grant-id",
            "calendar_id": "test-calendar-id",
            "busy": True,
            "participants": [
                {"email": "test@example.com", "name": "Test User", "status": "yes"}
            ],
            "when": {
                "start_time": 1497916800,
                "end_time": 1497920400,
                "object": "timespan",
            },
            "resources": [],
            "title": "Test Event with Empty Resources",
        }

        event = Event.from_dict(event_json)

        assert event.id == "test-event-id"
        assert event.resources == []

    def test_event_with_partial_resource_deserialization(self):
        """Test event deserialization when a resource only has some fields set."""
        event_json = {
            "id": "test-event-id",
            "grant_id": "test-grant-id",
            "calendar_id": "test-calendar-id",
            "busy": True,
            "participants": [
                {"email": "test@example.com", "name": "Test User", "status": "yes"}
            ],
            "when": {
                "start_time": 1497916800,
                "end_time": 1497920400,
                "object": "timespan",
            },
            "resources": [
                {"email": "room-b@example.com", "name": "Conference Room B"}
            ],
            "title": "Test Event with Partial Resource",
        }

        event = Event.from_dict(event_json)

        assert event.resources[0].email == "room-b@example.com"
        assert event.resources[0].name == "Conference Room B"
        assert event.resources[0].capacity is None
        assert event.resources[0].building is None
        assert event.resources[0].floor_name is None
        assert event.resources[0].floor_section is None
        assert event.resources[0].floor_number is None

    def test_event_with_multiple_resources_deserialization(self):
        """Test event deserialization with multiple resources."""
        event_json = {
            "id": "test-event-id",
            "grant_id": "test-grant-id",
            "calendar_id": "test-calendar-id",
            "busy": True,
            "participants": [
                {"email": "test@example.com", "name": "Test User", "status": "yes"}
            ],
            "when": {
                "start_time": 1497916800,
                "end_time": 1497920400,
                "object": "timespan",
            },
            "resources": [
                {
                    "email": "room-a@example.com",
                    "name": "Conference Room A",
                    "capacity": 10,
                    "building": "Headquarters",
                    "floor_name": "Main",
                    "floor_section": "West Wing",
                    "floor_number": 3,
                },
                {
                    "email": "room-b@example.com",
                    "name": "Conference Room B",
                    "capacity": 4,
                    "building": "Annex",
                    "floor_name": "Ground",
                    "floor_section": "East Wing",
                    "floor_number": 1,
                },
            ],
            "title": "Test Event with Multiple Resources",
        }

        event = Event.from_dict(event_json)

        assert len(event.resources) == 2
        assert event.resources[0].email == "room-a@example.com"
        assert event.resources[0].capacity == 10
        assert event.resources[1].email == "room-b@example.com"
        assert event.resources[1].name == "Conference Room B"
        assert event.resources[1].capacity == 4
        assert event.resources[1].building == "Annex"
        assert event.resources[1].floor_number == 1

    def test_create_event_with_empty_resources(self, http_client_response):
        """Test creating an event passes through an empty resources list."""
        events = Events(http_client_response)
        request_body = {
            "when": {
                "start_time": 1661874192,
                "end_time": 1661877792,
            },
            "title": "Event with empty resources",
            "resources": [],
        }

        events.create(
            identifier="abc-123",
            request_body=request_body,
            query_params={"calendar_id": "abc-123"},
        )

        http_client_response._execute.assert_called_once_with(
            "POST",
            "/v3/grants/abc-123/events",
            None,
            {"calendar_id": "abc-123"},
            request_body,
            overrides=None,
        )

    def test_update_event_with_partial_resource(self, http_client_response):
        """Test updating an event passes through a resource with only some fields."""
        events = Events(http_client_response)
        request_body = {
            "resources": [
                {"email": "room-b@example.com", "name": "Conference Room B"}
            ],
        }

        events.update(
            identifier="abc-123",
            event_id="event-123",
            request_body=request_body,
            query_params={"calendar_id": "abc-123"},
        )

        http_client_response._execute.assert_called_once_with(
            "PUT",
            "/v3/grants/abc-123/events/event-123",
            None,
            {"calendar_id": "abc-123"},
            request_body,
            overrides=None,
        )


BATCH_OPERATIONS = [
    {
        "method": "create",
        "body": {
            "title": "Standup",
            "when": {"start_time": 1798794000, "end_time": 1798795800},
        },
    },
    {"method": "update", "event_id": "event-1", "body": {"title": "Renamed"}},
    {"method": "delete", "event_id": "event-2"},
]


def _event_json(event_id, title):
    return {
        "id": event_id,
        "grant_id": "abc-123",
        "calendar_id": "primary",
        "busy": True,
        "participants": [],
        "when": {
            "start_time": 1798794000,
            "end_time": 1798795800,
            "object": "timespan",
        },
        "title": title,
        "object": "event",
    }


def _http_response(status_code, body):
    response = Mock()
    response.status_code = status_code
    response.json.return_value = body
    response.headers = {"X-Test-Header": "test"}
    response.url = "https://test.nylas.com/v3/grants/abc-123/events/batch"
    return response


class TestEventBatch:
    def _batch(self, http_client, status_code, body, operations=None):
        events = Events(http_client)
        with patch("requests.request", return_value=_http_response(status_code, body)):
            return events.batch(
                identifier="abc-123",
                request_body={"operations": operations or BATCH_OPERATIONS},
                query_params={"calendar_id": "primary"},
            )

    def test_batch_events_request(self, http_client):
        events = Events(http_client)
        body = {"request_id": "req-123", "data": [{"status": 200}] * 3}

        with patch(
            "requests.request", return_value=_http_response(200, body)
        ) as mock_request:
            events.batch(
                identifier="abc-123",
                request_body={"operations": BATCH_OPERATIONS},
                query_params={
                    "calendar_id": "primary",
                    "notify_participants": False,
                    "select": "id,title",
                },
                overrides={"timeout": 60},
            )

        mock_request.assert_called_once()
        method, url = mock_request.call_args.args
        assert method == "POST"
        assert url == (
            "https://test.nylas.com/v3/grants/abc-123/events/batch"
            "?calendar_id=primary&notify_participants=False&select=id%2Ctitle"
        )
        assert (
            mock_request.call_args.kwargs["headers"]["Content-type"]
            == "application/json"
        )
        assert mock_request.call_args.kwargs["timeout"] == 60
        assert json.loads(mock_request.call_args.kwargs["data"]) == {
            "operations": [
                {
                    "method": "create",
                    "body": {
                        "title": "Standup",
                        "when": {"start_time": 1798794000, "end_time": 1798795800},
                    },
                },
                {
                    "method": "update",
                    "event_id": "event-1",
                    "body": {"title": "Renamed"},
                },
                {"method": "delete", "event_id": "event-2"},
            ]
        }

    def test_batch_events_all_succeeded(self, http_client):
        response = self._batch(
            http_client,
            200,
            {
                "request_id": "req-123",
                "data": [
                    {"status": 200, "data": _event_json("new-event", "Standup")},
                    {"status": 200, "data": _event_json("event-1", "Renamed")},
                    {"status": 200},
                ],
            },
        )

        assert response.request_id == "req-123"
        assert response.headers == {"X-Test-Header": "test"}
        created, updated, deleted = response.data
        assert created.status == 200
        assert isinstance(created.data, Event)
        assert created.data.id == "new-event"
        assert created.data.title == "Standup"
        assert created.data.when.start_time == 1798794000
        assert created.error is None
        assert updated.status == 200
        assert isinstance(updated.data, Event)
        assert updated.data.id == "event-1"
        assert updated.data.title == "Renamed"
        assert updated.error is None
        assert deleted.status == 200
        assert deleted.data is None
        assert deleted.error is None

    def test_batch_events_multi_status_returns_results(self, http_client):
        response = self._batch(
            http_client,
            207,
            {
                "request_id": "req-123",
                "data": [
                    {
                        "status": 500,
                        "error": {
                            "type": "api_error",
                            "message": "Failed to save the event metadata.",
                        },
                        "provider_event_created": True,
                    },
                    {
                        "status": 429,
                        "error": {
                            "type": "rate_limit_error",
                            "message": "Too many requests.",
                            "provider_error": {"error": {"code": 429}},
                        },
                        "retry_after": 30,
                    },
                    {"status": 200},
                ],
            },
        )

        assert response.request_id == "req-123"
        created, updated, deleted = response.data
        assert created.status == 500
        assert created.data is None
        assert created.error.type == "api_error"
        assert created.error.message == "Failed to save the event metadata."
        assert created.provider_event_created is True
        assert created.retry_after is None
        assert updated.status == 429
        assert updated.data is None
        assert updated.error.type == "rate_limit_error"
        assert updated.error.message == "Too many requests."
        assert updated.error.provider_error == {"error": {"code": 429}}
        assert updated.retry_after == 30
        assert updated.provider_event_created is None
        assert deleted.status == 200
        assert deleted.error is None

    def test_batch_events_multi_status_all_failed_returns_results(self, http_client):
        response = self._batch(
            http_client,
            207,
            {
                "request_id": "req-123",
                "data": [
                    {
                        "status": 503,
                        "error": {
                            "type": "internal_error",
                            "message": "Not attempted. It is safe to retry.",
                        },
                    },
                    {
                        "status": 404,
                        "error": {
                            "type": "not_found_error",
                            "message": "Event not found.",
                        },
                    },
                    {
                        "status": 404,
                        "error": {
                            "type": "not_found_error",
                            "message": "Event not found.",
                        },
                    },
                ],
            },
        )

        assert [result.status for result in response.data] == [503, 404, 404]
        assert all(result.data is None for result in response.data)
        assert response.data[0].error.type == "internal_error"
        assert response.data[1].error.type == "not_found_error"
        assert response.data[2].error.type == "not_found_error"

    def test_batch_events_retry_after_zero(self, http_client):
        response = self._batch(
            http_client,
            207,
            {
                "request_id": "req-123",
                "data": [
                    {
                        "status": 429,
                        "error": {
                            "type": "rate_limit_error",
                            "message": "Too many requests.",
                        },
                        "retry_after": 0,
                    }
                ],
            },
            operations=[{"method": "delete", "event_id": "event-2"}],
        )

        assert response.data[0].retry_after is not None
        assert response.data[0].retry_after == 0

    def test_batch_events_invalid_request_raises_api_error(self, http_client):
        events = Events(http_client)
        operations = [
            {"method": "delete", "event_id": f"event-{index}"} for index in range(51)
        ]
        body = {
            "request_id": "req-123",
            "error": {
                "type": "invalid_request_error",
                "message": "operations cannot exceed 50",
            },
        }

        with patch(
            "requests.request", return_value=_http_response(400, body)
        ) as mock_request:
            with pytest.raises(NylasApiError) as error:
                events.batch(
                    identifier="abc-123",
                    request_body={"operations": operations},
                    query_params={"calendar_id": "primary"},
                )

        mock_request.assert_called_once()
        assert error.value.status_code == 400
        assert error.value.request_id == "req-123"
        assert error.value.type == "invalid_request_error"
        assert str(error.value) == "operations cannot exceed 50"

    def test_batch_events_results_match_operation_order(self, http_client):
        operations = [
            {"method": "delete", "event_id": "event-2"},
            {"method": "update", "event_id": "event-1", "body": {"title": "Renamed"}},
            {"method": "delete", "event_id": "event-3"},
            {"method": "create", "body": BATCH_OPERATIONS[0]["body"]},
        ]

        response = self._batch(
            http_client,
            207,
            {
                "request_id": "req-123",
                "data": [
                    {"status": 200},
                    {"status": 200, "data": _event_json("event-1", "Renamed")},
                    {
                        "status": 404,
                        "error": {
                            "type": "not_found_error",
                            "message": "Event event-3 not found.",
                        },
                    },
                    {"status": 200, "data": _event_json("new-event", "Standup")},
                ],
            },
            operations=operations,
        )

        assert len(response.data) == len(operations)
        assert response.data[0].status == 200
        assert response.data[0].data is None
        assert response.data[1].data.id == "event-1"
        assert response.data[2].error.message == "Event event-3 not found."
        assert response.data[3].data.id == "new-event"

    @pytest.mark.filterwarnings("ignore:Missing value of non-optional type")
    def test_batch_events_with_select_returns_partial_events(self, http_client):
        response = self._batch(
            http_client,
            200,
            {
                "request_id": "req-123",
                "data": [
                    {"status": 200, "data": {"id": "new-event", "title": "Standup"}}
                ],
            },
            operations=[BATCH_OPERATIONS[0]],
        )

        assert isinstance(response.data[0].data, Event)
        assert response.data[0].data.id == "new-event"
        assert response.data[0].data.title == "Standup"
        assert response.data[0].data.when is None

    def test_batch_operation_types_require_event_id_and_body(self):
        assert BatchCreateEventOperation.__required_keys__ == frozenset(
            {"method", "body"}
        )
        assert BatchUpdateEventOperation.__required_keys__ == frozenset(
            {"method", "event_id", "body"}
        )
        assert BatchDeleteEventOperation.__required_keys__ == frozenset(
            {"method", "event_id"}
        )

from nylas.resources.events import Events
from nylas.models.events import Event


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

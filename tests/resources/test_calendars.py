from nylas.resources.calendars import Calendars

from nylas.models.calendars import Calendar, EventSelection


class TestCalendar:
    def test_calendar_deserialization(self):
        calendar_json = {
            "grant_id": "abc-123-grant-id",
            "description": "Description of my new calendar",
            "hex_color": "#039BE5",
            "hex_foreground_color": "#039BE5",
            "id": "5d3qmne77v32r8l4phyuksl2x",
            "is_owned_by_user": True,
            "is_primary": True,
            "location": "Los Angeles, CA",
            "metadata": {"your-key": "value"},
            "name": "My New Calendar",
            "object": "calendar",
            "read_only": False,
            "timezone": "America/Los_Angeles",
        }

        cal = Calendar.from_dict(calendar_json)

        assert cal.grant_id == "abc-123-grant-id"
        assert cal.description == "Description of my new calendar"
        assert cal.hex_color == "#039BE5"
        assert cal.hex_foreground_color == "#039BE5"
        assert cal.id == "5d3qmne77v32r8l4phyuksl2x"
        assert cal.is_owned_by_user is True
        assert cal.is_primary is True
        assert cal.location == "Los Angeles, CA"
        assert cal.metadata == {"your-key": "value"}
        assert cal.name == "My New Calendar"
        assert cal.object == "calendar"
        assert cal.read_only is False
        assert cal.timezone == "America/Los_Angeles"

    def test_calendar_with_notetaker_deserialization(self):
        calendar_json = {
            "grant_id": "abc-123-grant-id",
            "description": "Description of my new calendar",
            "id": "5d3qmne77v32r8l4phyuksl2x",
            "is_owned_by_user": True,
            "name": "My New Calendar",
            "object": "calendar",
            "read_only": False,
            "notetaker": {
                "name": "My Notetaker",
                "meeting_settings": {
                    "video_recording": True,
                    "audio_recording": True,
                    "transcription": True
                },
                "rules": {
                    "event_selection": ["internal", "external"],
                    "participant_filter": {
                        "participants_gte": 3,
                        "participants_lte": 10
                    }
                }
            }
        }

        cal = Calendar.from_dict(calendar_json)

        assert cal.grant_id == "abc-123-grant-id"
        assert cal.id == "5d3qmne77v32r8l4phyuksl2x"
        assert cal.is_owned_by_user is True
        assert cal.name == "My New Calendar"
        assert cal.object == "calendar"
        assert cal.read_only is False
        assert cal.notetaker is not None
        assert cal.notetaker.name == "My Notetaker"
        assert cal.notetaker.meeting_settings is not None
        assert cal.notetaker.meeting_settings.video_recording is True
        assert cal.notetaker.meeting_settings.audio_recording is True
        assert cal.notetaker.meeting_settings.transcription is True
        assert cal.notetaker.rules is not None
        assert len(cal.notetaker.rules.event_selection) == 2
        assert EventSelection.INTERNAL in cal.notetaker.rules.event_selection
        assert EventSelection.EXTERNAL in cal.notetaker.rules.event_selection
        assert cal.notetaker.rules.participant_filter is not None
        assert cal.notetaker.rules.participant_filter.participants_gte == 3
        assert cal.notetaker.rules.participant_filter.participants_lte == 10

    def test_list_calendars(self, http_client_list_response):
        calendars = Calendars(http_client_list_response)

        calendars.list(identifier="abc-123")

        http_client_list_response._execute.assert_called_once_with(
            "GET", "/v3/grants/abc-123/calendars", None, None, None, overrides=None
        )

    def test_list_calendars_with_query_params(self, http_client_list_response):
        calendars = Calendars(http_client_list_response)

        calendars.list(identifier="abc-123", query_params={"limit": 20})

        http_client_list_response._execute.assert_called_once_with(
            "GET",
            "/v3/grants/abc-123/calendars",
            None,
            {"limit": 20},
            None,
            overrides=None,
        )

    def test_list_calendars_with_select_param(self, http_client_list_response):
        calendars = Calendars(http_client_list_response)

        # Set up mock response data
        http_client_list_response._execute.return_value = {
            "request_id": "abc-123",
            "data": [{
                "id": "calendar-123",
                "name": "My Calendar",
                "description": "My calendar description"
            }]
        }

        # Call the API method
        result = calendars.list(
            identifier="abc-123",
            query_params={
                "select": "id,name,description"
            }
        )

        # Verify API call
        http_client_list_response._execute.assert_called_with(
            "GET",
            "/v3/grants/abc-123/calendars",
            None,
            {"select": "id,name,description"},
            None,
            overrides=None,
        )

        # The actual response validation is handled by the mock in conftest.py
        assert result is not None

    def test_find_calendar(self, http_client_response):
        calendars = Calendars(http_client_response)

        calendars.find(identifier="abc-123", calendar_id="calendar-123")

        http_client_response._execute.assert_called_once_with(
            "GET",
            "/v3/grants/abc-123/calendars/calendar-123",
            None,
            None,
            None,
            overrides=None,
        )

    def test_find_calendar_with_select_param(self, http_client_response):
        calendars = Calendars(http_client_response)

        # Set up mock response data
        http_client_response._execute.return_value = ({
            "request_id": "abc-123",
            "data": {
                "id": "calendar-123",
                "name": "My Calendar",
                "description": "My calendar description"
            }
        }, {"X-Test-Header": "test"})

        # Call the API method
        result = calendars.find(
            identifier="abc-123",
            calendar_id="calendar-123",
            query_params={"select": "id,name,description"}
        )

        # Verify API call
        http_client_response._execute.assert_called_with(
            "GET",
            "/v3/grants/abc-123/calendars/calendar-123",
            None,
            {"select": "id,name,description"},
            None,
            overrides=None,
        )

        # The actual response validation is handled by the mock in conftest.py
        assert result is not None

    def test_create_calendar(self, http_client_response):
        calendars = Calendars(http_client_response)
        request_body = {
            "name": "My New Calendar",
            "description": "Description of my new calendar",
            "location": "Los Angeles, CA",
            "timezone": "America/Los_Angeles",
            "metadata": {"your-key": "value"},
        }

        calendars.create(identifier="abc-123", request_body=request_body)

        http_client_response._execute.assert_called_once_with(
            "POST",
            "/v3/grants/abc-123/calendars",
            None,
            None,
            request_body,
            overrides=None,
        )

    def test_create_calendar_with_notetaker(self, http_client_response):
        calendars = Calendars(http_client_response)
        request_body = {
            "name": "My New Calendar",
            "description": "Description of my new calendar",
            "location": "Los Angeles, CA",
            "timezone": "America/Los_Angeles",
            "notetaker": {
                "name": "My Notetaker",
                "meeting_settings": {
                    "video_recording": True,
                    "audio_recording": True,
                    "transcription": True
                },
                "rules": {
                    "event_selection": [EventSelection.INTERNAL.value, EventSelection.EXTERNAL.value],
                    "participant_filter": {
                        "participants_gte": 3,
                        "participants_lte": 10
                    }
                }
            }
        }

        calendars.create(identifier="abc-123", request_body=request_body)

        http_client_response._execute.assert_called_once_with(
            "POST",
            "/v3/grants/abc-123/calendars",
            None,
            None,
            request_body,
            overrides=None,
        )

    def test_update_calendar(self, http_client_response):
        calendars = Calendars(http_client_response)
        request_body = {
            "name": "My Updated Calendar",
            "description": "Description of my updated calendar",
            "location": "Los Angeles, CA",
            "timezone": "America/Los_Angeles",
            "metadata": {"your-key": "value"},
        }

        calendars.update(
            identifier="abc-123", calendar_id="calendar-123", request_body=request_body
        )

        http_client_response._execute.assert_called_once_with(
            "PUT",
            "/v3/grants/abc-123/calendars/calendar-123",
            None,
            None,
            request_body,
            overrides=None,
        )

    def test_update_calendar_with_notetaker(self, http_client_response):
        calendars = Calendars(http_client_response)
        request_body = {
            "name": "My Updated Calendar",
            "notetaker": {
                "name": "Updated Notetaker",
                "meeting_settings": {
                    "video_recording": False,
                    "audio_recording": True,
                    "transcription": False
                },
                "rules": {
                    "event_selection": [EventSelection.ALL.value],
                    "participant_filter": {
                        "participants_gte": 2
                    }
                }
            }
        }

        calendars.update(
            identifier="abc-123", calendar_id="calendar-123", request_body=request_body
        )

        http_client_response._execute.assert_called_once_with(
            "PUT",
            "/v3/grants/abc-123/calendars/calendar-123",
            None,
            None,
            request_body,
            overrides=None,
        )

    def test_destroy_calendar(self, http_client_delete_response):
        calendars = Calendars(http_client_delete_response)

        calendars.destroy(identifier="abc-123", calendar_id="calendar-123")

        http_client_delete_response._execute.assert_called_once_with(
            "DELETE",
            "/v3/grants/abc-123/calendars/calendar-123",
            None,
            None,
            None,
            overrides=None,
        )

    def test_get_availability(self, http_client_response):
        calendars = Calendars(http_client_response)
        request_body = {
            "start_time": 1497916800,
            "end_time": 1498003200,
            "duration_minutes": 30,
            "interval_minutes": 30,
            "free_busy": [
                {
                    "email": "test@gmail.com",
                }
            ],
            "open_hours": [
                {
                    "days": ["monday", "wednesday"],
                    "timezone": "America/New_York",
                    "start": "08:00",
                    "end": "18:00",
                    "restrictions": [
                        {
                            "days": ["monday"],
                            "start": "12:00",
                            "end": "13:00",
                        }
                    ],
                }
            ],
            "duration_minutes": 60,
            "interval_minutes": 30,
            "round_to_30_minutes": True,
            "availability_rules": {
                "availability_method": "max-availability",
                "buffer": {"before": 10, "after": 10},
                "default_open_hours": [
                    {
                        "days": [0],
                        "timezone": "America/Los_Angeles",
                        "start": "09:00",
                        "end": "17:00",
                        "exdates": ["2021-03-01"],
                    }
                ],
                "round_robin_group_id": "event-123",
                "tentative_as_busy": False
            },
        }

        calendars.get_availability(request_body,overrides=None,)

        http_client_response._execute.assert_called_once_with(
            "POST",
            "/v3/calendars/availability",
            None,
            None,
            request_body,
            overrides=None,
        )

    def test_get_free_busy(self, http_client_free_busy):
        calendars = Calendars(http_client_free_busy)
        free_busy_request = {
            "emails": ["test@gmail.com", "test2@gmail.com"],
            "start_time": 1497916800,
            "end_time": 1498003200,
        }

        # Http client is mocked in conftest.py, specific
        # mock for free busy is configured there
        calendars.get_free_busy(
            identifier="abc123", request_body=free_busy_request, overrides=None
        )

        http_client_free_busy._execute.assert_called_once_with(
            "POST",
            "/v3/grants/abc123/calendars/free-busy",
            None,
            None,
            free_busy_request,
            overrides=None,
        )


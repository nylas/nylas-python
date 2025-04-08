from nylas.resources.calendars import Calendars

from nylas.models.calendars import Calendar


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
            "start_time": 1614556800,
            "end_time": 1614643200,
            "participants": [
                {
                    "email": "test@gmail.com",
                    "calendar_ids": ["calendar-123"],
                    "open_hours": [
                        {
                            "days": [0],
                            "timezone": "America/Los_Angeles",
                            "start": "09:00",
                            "end": "17:00",
                            "exdates": ["2021-03-01"],
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
            method="POST",
            path="/v3/calendars/availability",
            request_body=request_body,
            overrides=None,
        )

    def test_get_free_busy(self, http_client_free_busy):
        calendars = Calendars(http_client_free_busy)
        request_body = {
            "start_time": 1614556800,
            "end_time": 1614643200,
            "emails": ["test@gmail.com"],
        }

        response = calendars.get_free_busy(
            identifier="abc-123", request_body=request_body
        )

        http_client_free_busy._execute.assert_called_once_with(
            method="POST",
            path="/v3/grants/abc-123/calendars/free-busy",
            request_body=request_body,
            overrides=None,
        )
        assert len(response.data) == 2
        assert response.request_id == "dd3ec9a2-8f15-403d-b269-32b1f1beb9f5"
        assert response.data[0].email == "user1@example.com"
        assert len(response.data[0].time_slots) == 2
        assert response.data[0].time_slots[0].start_time == 1690898400
        assert response.data[0].time_slots[0].end_time == 1690902000
        assert response.data[0].time_slots[0].status == "busy"
        assert response.data[0].time_slots[1].start_time == 1691064000
        assert response.data[0].time_slots[1].end_time == 1691067600
        assert response.data[0].time_slots[1].status == "busy"
        assert response.data[1].email == "user2@example.com"
        assert (
            response.data[1].error
            == "Unable to resolve e-mail address user2@example.com to an Active Directory object."
        )

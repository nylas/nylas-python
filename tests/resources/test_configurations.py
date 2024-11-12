from nylas.resources.configurations import Configurations

from nylas.models.scheduler import Configuration

class TestConfiguration:
    def test_configuration_deserialization(self):
        configuration_json = {
            "id": "abc-123-configuration-id",
            "slug": None,
            "participants": [
                {
                    "email": "test@nylas.com",
                    "is_organizer": True,
                    "name": "Test",
                    "availability": {
                        "calendar_ids": [
                            "primary"
                        ],
                        "open_hours": [
                            {
                                "days": [
                                    0,
                                    1,
                                    2,
                                    3,
                                    4,
                                    5,
                                    6
                                ],
                                "exdates": None,
                                "timezone": "",
                                "start": "09:00",
                                "end": "17:00"
                            }
                        ]
                    },
                    "booking": {
                        "calendar_id": "primary"
                    },
                    "timezone": ""
                }
            ],
            "requires_session_auth": False,
            "availability": {
                "duration_minutes": 30,
                "interval_minutes": 15,
                "round_to": 15,
                "availability_rules": {
                    "availability_method": "collective",
                    "buffer": {
                        "before": 60,
                        "after": 0
                    },
                    "default_open_hours": [
                        {
                            "days": [
                                0,
                                1,
                                2,
                                5,
                                6
                            ],
                            "exdates": None,
                            "timezone": "",
                            "start": "09:00",
                            "end": "18:00"
                        }
                    ],
                    "round_robin_group_id": ""
                }
            },
            "event_booking": {
                "title": "Updated Title",
                "timezone": "utc",
                "description": "",
                "location": "none",
                "booking_type": "booking",
                "conferencing": {
                    "provider": "Microsoft Teams",
                    "autocreate": {
                        "conf_grant_id": "",
                        "conf_settings": None
                    }
                },
                "hide_participants": None,
                "disable_emails": None
            },
            "scheduler": {
                "available_days_in_future": 7,
                "min_cancellation_notice": 60,
                "min_booking_notice": 120,
                "confirmation_redirect_url": "",
                "hide_rescheduling_options": False,
                "hide_cancellation_options": False,
                "hide_additional_guests": True,
                "cancellation_policy": "",
                "email_template": {
                    "booking_confirmed": {}
                }
            },
            "appearance": {
                "submit_button_label": "submit",
                "thank_you_message": "thank you for your business. your booking was successful."
            }
        }

        configuration = Configuration.from_dict(configuration_json)

        assert configuration.id == "abc-123-configuration-id"
        assert configuration.slug == None
        assert configuration.participants[0].email == "test@nylas.com"
        assert configuration.participants[0].is_organizer == True
        assert configuration.participants[0].name == "Test"
        assert configuration.participants[0].availability.calendar_ids == ["primary"]
        assert configuration.participants[0].availability.open_hours[0]["days"] == [0, 1, 2, 3, 4, 5, 6]
        assert configuration.participants[0].availability.open_hours[0]["exdates"] == None
        assert configuration.participants[0].availability.open_hours[0]["timezone"] == ""
        assert configuration.participants[0].booking.calendar_id == "primary"
        assert configuration.participants[0].timezone == ""
        assert configuration.requires_session_auth == False
        assert configuration.availability.duration_minutes == 30
        assert configuration.availability.interval_minutes == 15
        assert configuration.availability.round_to == 15
        assert configuration.availability.availability_rules["availability_method"] == "collective"
        assert configuration.availability.availability_rules["buffer"]["before"] == 60
        assert configuration.availability.availability_rules["buffer"]["after"] == 0
        assert configuration.availability.availability_rules["default_open_hours"][0]["days"] == [0, 1, 2, 5, 6]
        assert configuration.availability.availability_rules["default_open_hours"][0]["exdates"] == None
        assert configuration.availability.availability_rules["default_open_hours"][0]["timezone"] == ""
        assert configuration.availability.availability_rules["default_open_hours"][0]["start"] == "09:00"
        assert configuration.availability.availability_rules["default_open_hours"][0]["end"] == "18:00"
        assert configuration.event_booking.title == "Updated Title"
        assert configuration.event_booking.timezone == "utc"
        assert configuration.event_booking.description == ""
        assert configuration.event_booking.location == "none"
        assert configuration.event_booking.booking_type == "booking"
        assert configuration.event_booking.conferencing.provider == "Microsoft Teams"
        assert configuration.scheduler.available_days_in_future == 7
        assert configuration.scheduler.min_cancellation_notice == 60
        assert configuration.scheduler.min_booking_notice == 120
        assert configuration.appearance["submit_button_label"] == "submit"

    def test_list_configurations(self, http_client_list_response):
        configurations = Configurations(http_client_list_response)
        configurations.list(identifier="grant-123")

        http_client_list_response._execute.assert_called_once_with(
            "GET",
            "/v3/grants/grant-123/scheduling/configurations",
            None,
            None,
            None,
            overrides=None,
        )
    
    def test_find_configuration(self, http_client_response):
        configurations = Configurations(http_client_response)
        configurations.find(identifier="grant-123", config_id="config-123")

        http_client_response._execute.assert_called_once_with(
            "GET",
            "/v3/grants/grant-123/scheduling/configurations/config-123",
            None,
            None,
            None,
            overrides=None,
        )

    def test_create_configuration(self, http_client_response):
        configurations = Configurations(http_client_response)
        request_body = {
            "requires_session_auth": False,
            "participants": [
            {
                "name": "Test",
                "email": "test@nylas.com",
                "is_organizer": True,
                "availability": {
                "calendar_ids": [
                    "primary"
                ]
                },
                "booking": {
                "calendar_id": "primary"
                }
            }
            ],
            "availability": {
                "duration_minutes": 30
            },
            "event_booking": {
                "title": "My test event"
            }
        }
        configurations.create(identifier="grant-123", request_body=request_body)
        http_client_response._execute.assert_called_once_with(
            "POST",
            "/v3/grants/grant-123/scheduling/configurations",
            None,
            None,
            request_body,
            overrides=None,
        )

    def test_update_configuration(self, http_client_response):
        configurations = Configurations(http_client_response)
        request_body = { 
            "event_booking": {
                "title": "My test event"
            }
        }
        configurations.update(identifier="grant-123", config_id="config-123", request_body=request_body)

        http_client_response._execute.assert_called_once_with(
            "PUT",
            "/v3/grants/grant-123/scheduling/configurations/config-123",
            None,
            None,
            request_body,
            overrides=None,
        )

    def test_destroy_configuration(self, http_client_delete_response):
        configurations = Configurations(http_client_delete_response)
        configurations.destroy(identifier="grant-123", config_id="config-123")

        http_client_delete_response._execute.assert_called_once_with(
            "DELETE",
            "/v3/grants/grant-123/scheduling/configurations/config-123",
            None,
            None,
            None,
            overrides=None,
        )
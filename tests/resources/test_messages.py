from unittest.mock import patch, Mock

from nylas.models.messages import Message
from nylas.resources.messages import Messages
from nylas.resources.smart_compose import SmartCompose


class TestMessage:
    def test_smart_compose_property(self, http_client_response):
        messages = Messages(http_client_response)

        assert type(messages.smart_compose) is SmartCompose

    def test_message_deserialization(self):
        message_json = {
            "body": "Hello, I just sent a message using Nylas!",
            "cc": [{"name": "Arya Stark", "email": "arya.stark@example.com"}],
            "date": 1635355739,
            "attachments": [
                {
                    "content_type": "text/calendar",
                    "id": "4kj2jrcoj9ve5j9yxqz5cuv98",
                    "size": 1708,
                }
            ],
            "folders": ["8l6c4d11y1p4dm4fxj52whyr9", "d9zkcr2tljpu3m4qpj7l2hbr0"],
            "from": [{"name": "Daenerys Targaryen", "email": "daenerys.t@example.com"}],
            "grant_id": "41009df5-bf11-4c97-aa18-b285b5f2e386",
            "id": "5d3qmne77v32r8l4phyuksl2x",
            "object": "message",
            "reply_to": [
                {"name": "Daenerys Targaryen", "email": "daenerys.t@example.com"}
            ],
            "snippet": "Hello, I just sent a message using Nylas!",
            "starred": True,
            "subject": "Hello from Nylas!",
            "thread_id": "1t8tv3890q4vgmwq6pmdwm8qgsaer",
            "to": [{"name": "Jon Snow", "email": "j.snow@example.com"}],
            "unread": True,
            "metadata": {"custom_field": "value", "another_field": 123},
        }

        message = Message.from_dict(message_json)

        assert message.body == "Hello, I just sent a message using Nylas!"
        assert message.cc == [{"name": "Arya Stark", "email": "arya.stark@example.com"}]
        assert message.date == 1635355739
        assert message.attachments[0].content_type == "text/calendar"
        assert message.attachments[0].id == "4kj2jrcoj9ve5j9yxqz5cuv98"
        assert message.attachments[0].size == 1708
        assert message.folders[0] == "8l6c4d11y1p4dm4fxj52whyr9"
        assert message.folders[1] == "d9zkcr2tljpu3m4qpj7l2hbr0"
        assert message.from_ == [
            {"name": "Daenerys Targaryen", "email": "daenerys.t@example.com"}
        ]
        assert message.grant_id == "41009df5-bf11-4c97-aa18-b285b5f2e386"
        assert message.id == "5d3qmne77v32r8l4phyuksl2x"
        assert message.object == "message"
        assert message.reply_to == [
            {"name": "Daenerys Targaryen", "email": "daenerys.t@example.com"}
        ]
        assert message.snippet == "Hello, I just sent a message using Nylas!"
        assert message.starred is True
        assert message.subject == "Hello from Nylas!"
        assert message.thread_id == "1t8tv3890q4vgmwq6pmdwm8qgsaer"
        assert message.to == [{"name": "Jon Snow", "email": "j.snow@example.com"}]
        assert message.unread is True
        assert message.metadata == {"custom_field": "value", "another_field": 123}

    def test_list_messages(self, http_client_list_response):
        messages = Messages(http_client_list_response)

        messages.list(identifier="abc-123")

        http_client_list_response._execute.assert_called_once_with(
            "GET", "/v3/grants/abc-123/messages", None, None, None, overrides=None
        )

    def test_list_messages_with_query_params(self, http_client_list_response):
        messages = Messages(http_client_list_response)

        messages.list(
            identifier="abc-123",
            query_params={
                "subject": "Hello from Nylas!",
            },
        )

        http_client_list_response._execute.assert_called_once_with(
            "GET",
            "/v3/grants/abc-123/messages",
            None,
            {
                "subject": "Hello from Nylas!",
            },
            None,
            overrides=None,
        )

    def test_find_message(self, http_client_response):
        messages = Messages(http_client_response)

        messages.find(identifier="abc-123", message_id="message-123")

        http_client_response._execute.assert_called_once_with(
            "GET",
            "/v3/grants/abc-123/messages/message-123",
            None,
            None,
            None,
            overrides=None,
        )

    def test_find_message_encoded_id(self, http_client_response):
        messages = Messages(http_client_response)

        messages.find(
            identifier="abc-123",
            message_id="<!&!AAAAAAAAAAAuAAAAAAAAABQ/wHZyqaNCptfKg5rnNAoBAMO2jhD3dRHOtM0AqgC7tuYAAAAAAA4AABAAAACTn3BxdTQ/T4N/0BgqPmf+AQAAAAA=@example.com>",
        )

        http_client_response._execute.assert_called_once_with(
            "GET",
            "/v3/grants/abc-123/messages/%3C%21%26%21AAAAAAAAAAAuAAAAAAAAABQ%2FwHZyqaNCptfKg5rnNAoBAMO2jhD3dRHOtM0AqgC7tuYAAAAAAA4AABAAAACTn3BxdTQ%2FT4N%2F0BgqPmf%2BAQAAAAA%3D%40example.com%3E",
            None,
            None,
            None,
            overrides=None,
        )

    def test_find_message_with_query_params(self, http_client_response):
        messages = Messages(http_client_response)

        messages.find(
            identifier="abc-123",
            message_id="message-123",
            query_params={"fields": "standard"},
        )

        http_client_response._execute.assert_called_once_with(
            "GET",
            "/v3/grants/abc-123/messages/message-123",
            None,
            {"fields": "standard"},
            None,
            overrides=None,
        )

    def test_update_message(self, http_client_response):
        messages = Messages(http_client_response)
        request_body = {
            "starred": True,
            "unread": False,
            "folders": ["folder-123"],
            "metadata": {"foo": "bar"},
        }

        messages.update(
            identifier="abc-123",
            message_id="message-123",
            request_body=request_body,
        )

        http_client_response._execute.assert_called_once_with(
            "PUT",
            "/v3/grants/abc-123/messages/message-123",
            None,
            None,
            request_body,
            overrides=None,
        )

    def test_update_message_encoded_id(self, http_client_response):
        messages = Messages(http_client_response)
        request_body = {
            "starred": True,
            "unread": False,
            "folders": ["folder-123"],
            "metadata": {"foo": "bar"},
        }

        messages.update(
            identifier="abc-123",
            message_id="<!&!AAAAAAAAAAAuAAAAAAAAABQ/wHZyqaNCptfKg5rnNAoBAMO2jhD3dRHOtM0AqgC7tuYAAAAAAA4AABAAAACTn3BxdTQ/T4N/0BgqPmf+AQAAAAA=@example.com>",
            request_body=request_body,
        )

        http_client_response._execute.assert_called_once_with(
            "PUT",
            "/v3/grants/abc-123/messages/%3C%21%26%21AAAAAAAAAAAuAAAAAAAAABQ%2FwHZyqaNCptfKg5rnNAoBAMO2jhD3dRHOtM0AqgC7tuYAAAAAAA4AABAAAACTn3BxdTQ%2FT4N%2F0BgqPmf%2BAQAAAAA%3D%40example.com%3E",
            None,
            None,
            request_body,
            overrides=None,
        )

    def test_destroy_message(self, http_client_delete_response):
        messages = Messages(http_client_delete_response)

        messages.destroy(identifier="abc-123", message_id="message-123")

        http_client_delete_response._execute.assert_called_once_with(
            "DELETE",
            "/v3/grants/abc-123/messages/message-123",
            None,
            None,
            None,
            overrides=None,
        )

    def test_destroy_message_encoded_id(self, http_client_delete_response):
        messages = Messages(http_client_delete_response)

        messages.destroy(
            identifier="abc-123",
            message_id="<!&!AAAAAAAAAAAuAAAAAAAAABQ/wHZyqaNCptfKg5rnNAoBAMO2jhD3dRHOtM0AqgC7tuYAAAAAAA4AABAAAACTn3BxdTQ/T4N/0BgqPmf+AQAAAAA=@example.com>",
        )

        http_client_delete_response._execute.assert_called_once_with(
            "DELETE",
            "/v3/grants/abc-123/messages/%3C%21%26%21AAAAAAAAAAAuAAAAAAAAABQ%2FwHZyqaNCptfKg5rnNAoBAMO2jhD3dRHOtM0AqgC7tuYAAAAAAA4AABAAAACTn3BxdTQ%2FT4N%2F0BgqPmf%2BAQAAAAA%3D%40example.com%3E",
            None,
            None,
            None,
            overrides=None,
        )

    def test_send_message(self, http_client_response):
        messages = Messages(http_client_response)
        request_body = {
            "subject": "Hello from Nylas!",
            "to": [{"name": "Jon Snow", "email": "jsnow@gmail.com"}],
            "cc": [{"name": "Arya Stark", "email": "astark@gmail.com"}],
            "body": "This is the body of my draft message.",
            "metadata": {"custom_field": "value", "another_field": 123},
        }

        messages.send(identifier="abc-123", request_body=request_body)

        http_client_response._execute.assert_called_once_with(
            method="POST",
            path="/v3/grants/abc-123/messages/send",
            request_body=request_body,
            data=None,
            overrides=None,
        )

    def test_send_message_small_attachment(self, http_client_response):
        messages = Messages(http_client_response)
        request_body = {
            "subject": "Hello from Nylas!",
            "to": [{"name": "Jon Snow", "email": "jsnow@gmail.com"}],
            "cc": [{"name": "Arya Stark", "email": "astark@gmail.com"}],
            "body": "This is the body of my draft message.",
            "attachments": [
                {
                    "filename": "file1.txt",
                    "content_type": "text/plain",
                    "content": "this is a file",
                    "size": 3,
                },
            ],
            "metadata": {"custom_field": "value", "another_field": 123},
        }

        messages.send(identifier="abc-123", request_body=request_body)

        http_client_response._execute.assert_called_once_with(
            method="POST",
            path="/v3/grants/abc-123/messages/send",
            request_body=request_body,
            data=None,
            overrides=None,
        )

    def test_send_message_large_attachment(self, http_client_response):
        messages = Messages(http_client_response)
        mock_encoder = Mock()
        request_body = {
            "subject": "Hello from Nylas!",
            "to": [{"name": "Jon Snow", "email": "jsnow@gmail.com"}],
            "cc": [{"name": "Arya Stark", "email": "astark@gmail.com"}],
            "body": "This is the body of my draft message.",
            "attachments": [
                {
                    "filename": "file1.txt",
                    "content_type": "text/plain",
                    "content": "this is a file",
                    "size": 3 * 1024 * 1024,
                },
            ],
            "metadata": {"custom_field": "value", "another_field": 123},
        }

        with patch(
            "nylas.resources.messages._build_form_request", return_value=mock_encoder
        ):
            messages.send(identifier="abc-123", request_body=request_body)

            http_client_response._execute.assert_called_once_with(
                method="POST",
                path="/v3/grants/abc-123/messages/send",
                request_body=None,
                data=mock_encoder,
                overrides=None,
            )

    def test_list_scheduled_messages(self, http_client_list_scheduled_messages):
        messages = Messages(http_client_list_scheduled_messages)

        res = messages.list_scheduled_messages(identifier="abc-123")

        http_client_list_scheduled_messages._execute.assert_called_once_with(
            method="GET", path="/v3/grants/abc-123/messages/schedules", overrides=None
        )
        assert res.request_id == "dd3ec9a2-8f15-403d-b269-32b1f1beb9f5"
        assert len(res.data) == 2
        assert res.data[0].schedule_id == "8cd56334-6d95-432c-86d1-c5dab0ce98be"
        assert res.data[0].status.code == "pending"
        assert res.data[0].status.description == "schedule send awaiting send at time"
        assert res.data[1].schedule_id == "rb856334-6d95-432c-86d1-c5dab0ce98be"
        assert res.data[1].status.code == "success"
        assert res.data[1].status.description == "schedule send succeeded"
        assert res.data[1].close_time == 1690579819

    def test_find_scheduled_message(self, http_client_response):
        messages = Messages(http_client_response)

        messages.find_scheduled_message(
            identifier="abc-123", schedule_id="schedule-123"
        )

        http_client_response._execute.assert_called_once_with(
            method="GET",
            path="/v3/grants/abc-123/messages/schedules/schedule-123",
            overrides=None,
        )

    def test_stop_scheduled_message(self, http_client_response):
        messages = Messages(http_client_response)

        messages.stop_scheduled_message(
            identifier="abc-123", schedule_id="schedule-123"
        )

        http_client_response._execute.assert_called_once_with(
            method="DELETE",
            path="/v3/grants/abc-123/messages/schedules/schedule-123",
            overrides=None,
        )

    def test_clean_messages(self, http_client_clean_messages):
        messages = Messages(http_client_clean_messages)
        request_body = {
            "message_id": ["message-1", "message-2"],
            "ignore_images": True,
            "ignore_links": True,
            "ignore_tables": True,
            "images_as_markdown": True,
            "remove_conclusion_phrases": True,
        }

        response = messages.clean_messages(
            identifier="abc-123",
            request_body=request_body,
        )

        http_client_clean_messages._execute.assert_called_once_with(
            method="PUT",
            path="/v3/grants/abc-123/messages/clean",
            request_body=request_body,
            overrides=None,
        )

        # Assert the conversation field, and the typical message fields serialize properly
        assert len(response.data) == 2
        assert response.data[0].body == "Hello, I just sent a message using Nylas!"
        assert response.data[0].from_ == [
            {"name": "Daenerys Targaryen", "email": "daenerys.t@example.com"}
        ]
        assert response.data[0].object == "message"
        assert response.data[0].id == "message-1"
        assert response.data[0].grant_id == "41009df5-bf11-4c97-aa18-b285b5f2e386"
        assert response.data[0].conversation == "cleaned example"
        assert response.data[1].conversation == "another example"

    def test_list_messages(self, http_client_list_response):
        messages = Messages(http_client_list_response)

        messages.list(identifier="abc-123")

        http_client_list_response._execute.assert_called_once_with(
            "GET", "/v3/grants/abc-123/messages", None, None, None, overrides=None
        )

    def test_list_messages_with_query_params(self, http_client_list_response):
        messages = Messages(http_client_list_response)

        messages.list(
            identifier="abc-123",
            query_params={
                "subject": "Hello from Nylas!",
            },
        )

        http_client_list_response._execute.assert_called_once_with(
            "GET",
            "/v3/grants/abc-123/messages",
            None,
            {
                "subject": "Hello from Nylas!",
            },
            None,
            overrides=None,
        )

    def test_find_message(self, http_client_response):
        messages = Messages(http_client_response)

        messages.find(identifier="abc-123", message_id="message-123")

        http_client_response._execute.assert_called_once_with(
            "GET",
            "/v3/grants/abc-123/messages/message-123",
            None,
            None,
            None,
            overrides=None,
        )

    def test_find_message_encoded_id(self, http_client_response):
        messages = Messages(http_client_response)

        messages.find(
            identifier="abc-123",
            message_id="<!&!AAAAAAAAAAAuAAAAAAAAABQ/wHZyqaNCptfKg5rnNAoBAMO2jhD3dRHOtM0AqgC7tuYAAAAAAA4AABAAAACTn3BxdTQ/T4N/0BgqPmf+AQAAAAA=@example.com>",
        )

        http_client_response._execute.assert_called_once_with(
            "GET",
            "/v3/grants/abc-123/messages/%3C%21%26%21AAAAAAAAAAAuAAAAAAAAABQ%2FwHZyqaNCptfKg5rnNAoBAMO2jhD3dRHOtM0AqgC7tuYAAAAAAA4AABAAAACTn3BxdTQ%2FT4N%2F0BgqPmf%2BAQAAAAA%3D%40example.com%3E",
            None,
            None,
            None,
            overrides=None,
        )

    def test_find_message_with_query_params(self, http_client_response):
        messages = Messages(http_client_response)

        messages.find(
            identifier="abc-123",
            message_id="message-123",
            query_params={"fields": "standard"},
        )

        http_client_response._execute.assert_called_once_with(
            "GET",
            "/v3/grants/abc-123/messages/message-123",
            None,
            {"fields": "standard"},
            None,
            overrides=None,
        )

    def test_update_message(self, http_client_response):
        messages = Messages(http_client_response)
        request_body = {
            "starred": True,
            "unread": False,
            "folders": ["folder-123"],
            "metadata": {"foo": "bar"},
        }

        messages.update(
            identifier="abc-123",
            message_id="message-123",
            request_body=request_body,
        )

        http_client_response._execute.assert_called_once_with(
            "PUT",
            "/v3/grants/abc-123/messages/message-123",
            None,
            None,
            request_body,
            overrides=None,
        )

    def test_update_message_encoded_id(self, http_client_response):
        messages = Messages(http_client_response)
        request_body = {
            "starred": True,
            "unread": False,
            "folders": ["folder-123"],
            "metadata": {"foo": "bar"},
        }

        messages.update(
            identifier="abc-123",
            message_id="<!&!AAAAAAAAAAAuAAAAAAAAABQ/wHZyqaNCptfKg5rnNAoBAMO2jhD3dRHOtM0AqgC7tuYAAAAAAA4AABAAAACTn3BxdTQ/T4N/0BgqPmf+AQAAAAA=@example.com>",
            request_body=request_body,
        )

        http_client_response._execute.assert_called_once_with(
            "PUT",
            "/v3/grants/abc-123/messages/%3C%21%26%21AAAAAAAAAAAuAAAAAAAAABQ%2FwHZyqaNCptfKg5rnNAoBAMO2jhD3dRHOtM0AqgC7tuYAAAAAAA4AABAAAACTn3BxdTQ%2FT4N%2F0BgqPmf%2BAQAAAAA%3D%40example.com%3E",
            None,
            None,
            request_body,
            overrides=None,
        )

    def test_destroy_message(self, http_client_delete_response):
        messages = Messages(http_client_delete_response)

        messages.destroy(identifier="abc-123", message_id="message-123")

        http_client_delete_response._execute.assert_called_once_with(
            "DELETE",
            "/v3/grants/abc-123/messages/message-123",
            None,
            None,
            None,
            overrides=None,
        )

    def test_destroy_message_encoded_id(self, http_client_delete_response):
        messages = Messages(http_client_delete_response)

        messages.destroy(
            identifier="abc-123",
            message_id="<!&!AAAAAAAAAAAuAAAAAAAAABQ/wHZyqaNCptfKg5rnNAoBAMO2jhD3dRHOtM0AqgC7tuYAAAAAAA4AABAAAACTn3BxdTQ/T4N/0BgqPmf+AQAAAAA=@example.com>",
        )

        http_client_delete_response._execute.assert_called_once_with(
            "DELETE",
            "/v3/grants/abc-123/messages/%3C%21%26%21AAAAAAAAAAAuAAAAAAAAABQ%2FwHZyqaNCptfKg5rnNAoBAMO2jhD3dRHOtM0AqgC7tuYAAAAAAA4AABAAAACTn3BxdTQ%2FT4N%2F0BgqPmf%2BAQAAAAA%3D%40example.com%3E",
            None,
            None,
            None,
            overrides=None,
        )

    def test_send_message(self, http_client_response):
        messages = Messages(http_client_response)
        request_body = {
            "subject": "Hello from Nylas!",
            "to": [{"name": "Jon Snow", "email": "jsnow@gmail.com"}],
            "cc": [{"name": "Arya Stark", "email": "astark@gmail.com"}],
            "body": "This is the body of my draft message.",
        }

        messages.send(identifier="abc-123", request_body=request_body)

        http_client_response._execute.assert_called_once_with(
            method="POST",
            path="/v3/grants/abc-123/messages/send",
            request_body=request_body,
            data=None,
            overrides=None,
        )

    def test_send_message_small_attachment(self, http_client_response):
        messages = Messages(http_client_response)
        request_body = {
            "subject": "Hello from Nylas!",
            "to": [{"name": "Jon Snow", "email": "jsnow@gmail.com"}],
            "cc": [{"name": "Arya Stark", "email": "astark@gmail.com"}],
            "body": "This is the body of my draft message.",
            "attachments": [
                {
                    "filename": "file1.txt",
                    "content_type": "text/plain",
                    "content": "this is a file",
                    "size": 3,
                },
            ],
        }

        messages.send(identifier="abc-123", request_body=request_body)

        http_client_response._execute.assert_called_once_with(
            method="POST",
            path="/v3/grants/abc-123/messages/send",
            request_body=request_body,
            data=None,
            overrides=None,
        )

    def test_send_message_large_attachment(self, http_client_response):
        messages = Messages(http_client_response)
        mock_encoder = Mock()
        request_body = {
            "subject": "Hello from Nylas!",
            "to": [{"name": "Jon Snow", "email": "jsnow@gmail.com"}],
            "cc": [{"name": "Arya Stark", "email": "astark@gmail.com"}],
            "body": "This is the body of my draft message.",
            "attachments": [
                {
                    "filename": "file1.txt",
                    "content_type": "text/plain",
                    "content": "this is a file",
                    "size": 3 * 1024 * 1024,
                },
            ],
        }

        with patch(
            "nylas.resources.messages._build_form_request", return_value=mock_encoder
        ):
            messages.send(identifier="abc-123", request_body=request_body)

            http_client_response._execute.assert_called_once_with(
                method="POST",
                path="/v3/grants/abc-123/messages/send",
                request_body=None,
                data=mock_encoder,
                overrides=None,
            )

    def test_list_scheduled_messages(self, http_client_list_scheduled_messages):
        messages = Messages(http_client_list_scheduled_messages)

        res = messages.list_scheduled_messages(identifier="abc-123")

        http_client_list_scheduled_messages._execute.assert_called_once_with(
            method="GET", path="/v3/grants/abc-123/messages/schedules", overrides=None
        )
        assert res.request_id == "dd3ec9a2-8f15-403d-b269-32b1f1beb9f5"
        assert len(res.data) == 2
        assert res.data[0].schedule_id == "8cd56334-6d95-432c-86d1-c5dab0ce98be"
        assert res.data[0].status.code == "pending"
        assert res.data[0].status.description == "schedule send awaiting send at time"
        assert res.data[1].schedule_id == "rb856334-6d95-432c-86d1-c5dab0ce98be"
        assert res.data[1].status.code == "success"
        assert res.data[1].status.description == "schedule send succeeded"
        assert res.data[1].close_time == 1690579819

    def test_find_scheduled_message(self, http_client_response):
        messages = Messages(http_client_response)

        messages.find_scheduled_message(
            identifier="abc-123", schedule_id="schedule-123"
        )

        http_client_response._execute.assert_called_once_with(
            method="GET",
            path="/v3/grants/abc-123/messages/schedules/schedule-123",
            overrides=None,
        )

    def test_stop_scheduled_message(self, http_client_response):
        messages = Messages(http_client_response)

        messages.stop_scheduled_message(
            identifier="abc-123", schedule_id="schedule-123"
        )

        http_client_response._execute.assert_called_once_with(
            method="DELETE",
            path="/v3/grants/abc-123/messages/schedules/schedule-123",
            overrides=None,
        )

    def test_clean_messages(self, http_client_clean_messages):
        messages = Messages(http_client_clean_messages)
        request_body = {
            "message_id": ["message-1", "message-2"],
            "ignore_images": True,
            "ignore_links": True,
            "ignore_tables": True,
            "images_as_markdown": True,
            "remove_conclusion_phrases": True,
        }

        response = messages.clean_messages(
            identifier="abc-123",
            request_body=request_body,
        )

        http_client_clean_messages._execute.assert_called_once_with(
            method="PUT",
            path="/v3/grants/abc-123/messages/clean",
            request_body=request_body,
            overrides=None,
        )

        # Assert the conversation field, and the typical message fields serialize properly
        assert len(response.data) == 2
        assert response.data[0].body == "Hello, I just sent a message using Nylas!"
        assert response.data[0].from_ == [
            {"name": "Daenerys Targaryen", "email": "daenerys.t@example.com"}
        ]
        assert response.data[0].object == "message"
        assert response.data[0].id == "message-1"
        assert response.data[0].grant_id == "41009df5-bf11-4c97-aa18-b285b5f2e386"
        assert response.data[0].conversation == "cleaned example"
        assert response.data[1].conversation == "another example"


    def test_list_messages_select_param(self, http_client_list_response):
        messages = Messages(http_client_list_response)

        messages.list(identifier="abc-123", query_params={"select": ["id", "subject", "from", "to"]})

        http_client_list_response._execute.assert_called_once_with(
            "GET",
            "/v3/grants/abc-123/messages",
            None,
            {"select": ["id", "subject", "from", "to"]},
            None,
            overrides=None,
        )

        # Make sure query params are properly serialized
        assert http_client_list_response._execute.call_args[0][3] == {"select": ["id", "subject", "from", "to"]}

    def test_find_message_select_param(self, http_client_response):
        messages = Messages(http_client_response)

        messages.find(identifier="abc-123", message_id="message-123", query_params={"select": ["id", "subject", "from", "to"]})

        http_client_response._execute.assert_called_once_with(
            "GET",
            "/v3/grants/abc-123/messages/message-123",
            None,
            {"select": ["id", "subject", "from", "to"]},
            None,
            overrides=None,
        )

        # Make sure query params are properly serialized
        assert http_client_response._execute.call_args[0][3] == {"select": ["id", "subject", "from", "to"]}

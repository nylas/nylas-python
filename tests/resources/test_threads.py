from nylas.models.attachments import Attachment
from nylas.models.events import EmailName
from nylas.resources.threads import Threads

from nylas.models.threads import Thread


class TestThread:
    def test_thread_deserialization(self):
        thread_json = {
            "grant_id": "ca8f1733-6063-40cc-a2e3-ec7274abef11",
            "id": "7ml84jdmfnw20sq59f30hirhe",
            "object": "thread",
            "has_attachments": False,
            "has_drafts": False,
            "earliest_message_date": 1634149514,
            "latest_message_received_date": 1634832749,
            "latest_message_sent_date": 1635174399,
            "participants": [
                {"email": "daenerys.t@example.com", "name": "Daenerys Targaryen"}
            ],
            "snippet": "jnlnnn --Sent with Nylas",
            "starred": False,
            "subject": "Dinner Wednesday?",
            "unread": False,
            "message_ids": ["njeb79kFFzli09", "998abue3mGH4sk"],
            "draft_ids": ["a809kmmoW90Dx"],
            "folders": ["8l6c4d11y1p4dm4fxj52whyr9", "d9zkcr2tljpu3m4qpj7l2hbr0"],
            "latest_draft_or_message": {
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
                "from": [
                    {"name": "Daenerys Targaryen", "email": "daenerys.t@example.com"}
                ],
                "grant_id": "41009df5-bf11-4c97-aa18-b285b5f2e386",
                "id": "njeb79kFFzli09",
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
            },
        }

        thread = Thread.from_dict(thread_json)

        assert thread.grant_id == "ca8f1733-6063-40cc-a2e3-ec7274abef11"
        assert thread.id == "7ml84jdmfnw20sq59f30hirhe"
        assert thread.object == "thread"
        assert thread.has_attachments is False
        assert thread.has_drafts is False
        assert thread.earliest_message_date == 1634149514
        assert thread.latest_message_received_date == 1634832749
        assert thread.latest_message_sent_date == 1635174399
        assert thread.participants == [
            EmailName(name="Daenerys Targaryen", email="daenerys.t@example.com")
        ]
        assert thread.snippet == "jnlnnn --Sent with Nylas"
        assert thread.starred is False
        assert thread.subject == "Dinner Wednesday?"
        assert thread.unread is False
        assert thread.message_ids == ["njeb79kFFzli09", "998abue3mGH4sk"]
        assert thread.draft_ids == ["a809kmmoW90Dx"]
        assert thread.folders == [
            "8l6c4d11y1p4dm4fxj52whyr9",
            "d9zkcr2tljpu3m4qpj7l2hbr0",
        ]
        assert (
            thread.latest_draft_or_message.body
            == "Hello, I just sent a message using Nylas!"
        )
        assert thread.latest_draft_or_message.cc == [
            EmailName(name="Arya Stark", email="arya.stark@example.com")
        ]
        assert thread.latest_draft_or_message.date == 1635355739
        assert thread.latest_draft_or_message.attachments == [
            Attachment(
                content_type="text/calendar",
                id="4kj2jrcoj9ve5j9yxqz5cuv98",
                size=1708,
            ),
        ]
        assert thread.latest_draft_or_message.folders == [
            "8l6c4d11y1p4dm4fxj52whyr9",
            "d9zkcr2tljpu3m4qpj7l2hbr0",
        ]
        assert thread.latest_draft_or_message.from_ == [
            EmailName(name="Daenerys Targaryen", email="daenerys.t@example.com")
        ]
        assert (
            thread.latest_draft_or_message.grant_id
            == "41009df5-bf11-4c97-aa18-b285b5f2e386"
        )
        assert thread.latest_draft_or_message.id == "njeb79kFFzli09"
        assert thread.latest_draft_or_message.object == "message"
        assert thread.latest_draft_or_message.reply_to == [
            EmailName(name="Daenerys Targaryen", email="daenerys.t@example.com")
        ]
        assert (
            thread.latest_draft_or_message.snippet
            == "Hello, I just sent a message using Nylas!"
        )
        assert thread.latest_draft_or_message.starred is True
        assert thread.latest_draft_or_message.subject == "Hello from Nylas!"
        assert (
            thread.latest_draft_or_message.thread_id == "1t8tv3890q4vgmwq6pmdwm8qgsaer"
        )
        assert thread.latest_draft_or_message.to == [
            EmailName(name="Jon Snow", email="j.snow@example.com")
        ]
        assert thread.latest_draft_or_message.unread is True

    def test_list_threads(self, http_client_list_response):
        threads = Threads(http_client_list_response)

        threads.list(identifier="abc-123")

        http_client_list_response._execute.assert_called_once_with(
            "GET", "/v3/grants/abc-123/threads", None, None, None, overrides=None
        )

    def test_list_threads_with_query_params(self, http_client_list_response):
        threads = Threads(http_client_list_response)

        threads.list(identifier="abc-123", query_params={"to": "abc@gmail.com"})

        http_client_list_response._execute.assert_called_once_with(
            "GET", "/v3/grants/abc-123/threads", None, {"to": "abc@gmail.com"}, None, overrides=None
        )

    def test_find_thread(self, http_client_response):
        threads = Threads(http_client_response)

        threads.find(identifier="abc-123", thread_id="thread-123")

        http_client_response._execute.assert_called_once_with(
            "GET", "/v3/grants/abc-123/threads/thread-123", None, None, None, overrides=None
        )

    def test_update_thread(self, http_client_response):
        threads = Threads(http_client_response)
        request_body = {
            "starred": True,
            "unread": False,
            "folders": ["folder-123"],
        }

        threads.update(
            identifier="abc-123", thread_id="thread-123", request_body=request_body
        )

        http_client_response._execute.assert_called_once_with(
            "PUT",
            "/v3/grants/abc-123/threads/thread-123",
            None,
            None,
            request_body,
            overrides=None
        )

    def test_destroy_thread(self, http_client_delete_response):
        threads = Threads(http_client_delete_response)

        threads.destroy(identifier="abc-123", thread_id="thread-123")

        http_client_delete_response._execute.assert_called_once_with(
            "DELETE",
            "/v3/grants/abc-123/threads/thread-123",
            None,
            None,
            None,
            overrides=None
        )

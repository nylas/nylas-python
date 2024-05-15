from nylas.models.smart_compose import ComposeMessageResponse
from nylas.resources.smart_compose import SmartCompose


class TestSmartCompose:
    def test_smart_compose_deserialization(self, http_client):
        smart_compose_json = {"suggestion": "Hello world"}

        smart_compose = ComposeMessageResponse.from_dict(smart_compose_json)

        assert smart_compose.suggestion == "Hello world"

    def test_compose_message(self, http_client_response):
        smart_compose = SmartCompose(http_client_response)
        request_body = {"prompt": "Hello world"}

        smart_compose.compose_message("grant-123", request_body)

        http_client_response._execute.assert_called_once_with(
            method="POST",
            path="/v3/grants/grant-123/messages/smart-compose",
            request_body=request_body,
            overrides=None,
        )

    def test_compose_message_reply(self, http_client_response):
        smart_compose = SmartCompose(http_client_response)
        request_body = {"prompt": "Hello world"}

        smart_compose.compose_message_reply("grant-123", "message-123", request_body)

        http_client_response._execute.assert_called_once_with(
            method="POST",
            path="/v3/grants/grant-123/messages/message-123/smart-compose",
            request_body=request_body,
            overrides=None,
        )

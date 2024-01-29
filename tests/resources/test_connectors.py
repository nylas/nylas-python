from nylas.models.connectors import Connector
from nylas.resources.connectors import Connectors
from nylas.resources.credentials import Credentials


class TestConnectors:
    def test_credentials_property(self, http_client):
        connectors = Connectors(http_client)
        assert isinstance(connectors.credentials, Credentials)

    def test_connector_deserialization(self, http_client):
        connector_json = {
            "provider": "google",
            "settings": {"topic_name": "abc123"},
            "scope": [
                "https://www.googleapis.com/auth/userinfo.email",
                "https://www.googleapis.com/auth/userinfo.profile",
            ],
        }

        connector = Connector.from_dict(connector_json)

        assert connector.provider == "google"
        assert connector.settings["topic_name"] == "abc123"
        assert connector.scope == [
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
        ]

    def test_list_connectors(self, http_client_list_response):
        connectors = Connectors(http_client_list_response)

        connectors.list()

        http_client_list_response._execute.assert_called_once_with(
            "GET", "/v3/connectors", None, None, None
        )

    def test_find_connector(self, http_client_response):
        connectors = Connectors(http_client_response)

        connectors.find("google")

        http_client_response._execute.assert_called_once_with(
            "GET", "/v3/connectors/google", None, None, None
        )

    def test_create_connector(self, http_client_response):
        connectors = Connectors(http_client_response)
        request_body = {
            "provider": "google",
            "settings": {
                "client_id": "string",
                "client_secret": "string",
                "topic_name": "string",
            },
            "scope": [
                "https://www.googleapis.com/auth/userinfo.email",
                "https://www.googleapis.com/auth/userinfo.profile",
            ],
        }

        connectors.create(request_body=request_body)

        http_client_response._execute.assert_called_once_with(
            "POST",
            "/v3/connectors",
            None,
            None,
            request_body,
        )

    def test_update_connector(self, http_client_response):
        connectors = Connectors(http_client_response)
        request_body = {
            "settings": {
                "client_id": "string",
                "client_secret": "string",
                "topic_name": "string",
            },
            "scope": [
                "https://www.googleapis.com/auth/userinfo.email",
                "https://www.googleapis.com/auth/userinfo.profile",
            ],
        }

        connectors.update(
            provider="google",
            request_body=request_body,
        )

        http_client_response._execute.assert_called_once_with(
            "PATCH",
            "/v3/connectors/google",
            None,
            None,
            request_body,
        )

    def test_destroy_connector(self, http_client_delete_response):
        connectors = Connectors(http_client_delete_response)

        connectors.destroy("google")

        http_client_delete_response._execute.assert_called_once_with(
            "DELETE",
            "/v3/connectors/google",
            None,
            None,
            None,
        )

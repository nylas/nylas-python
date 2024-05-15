from nylas.models.credentials import Credential
from nylas.resources.credentials import Credentials


class TestCredentials:
    def test_credential_deserialization(self, http_client):
        credential_json = {
            "id": "e19f8e1a-eb1c-41c0-b6a6-d2e59daf7f47",
            "name": "My first Google credential",
            "created_at": 1617817109,
            "updated_at": 1617817109,
        }

        credential = Credential.from_dict(credential_json)

        assert credential.id == "e19f8e1a-eb1c-41c0-b6a6-d2e59daf7f47"
        assert credential.name == "My first Google credential"
        assert credential.created_at == 1617817109
        assert credential.updated_at == 1617817109

    def test_list_credentials(self, http_client_list_response):
        credentials = Credentials(http_client_list_response)

        credentials.list("google")

        http_client_list_response._execute.assert_called_once_with(
            "GET", "/v3/connectors/google/creds", None, None, None, overrides=None
        )

    def test_find_credential(self, http_client_response):
        credentials = Credentials(http_client_response)

        credentials.find("google", "abc-123")

        http_client_response._execute.assert_called_once_with(
            "GET",
            "/v3/connectors/google/creds/abc-123",
            None,
            None,
            None,
            overrides=None,
        )

    def test_create_credential(self, http_client_response):
        credentials = Credentials(http_client_response)
        request_body = {
            "name": "My first Google credential",
            "credential_type": "serviceaccount",
            "credential_data": {
                "private_key_id": "string",
                "private_key": "string",
                "client_email": "string",
            },
        }

        credentials.create("google", request_body=request_body)

        http_client_response._execute.assert_called_once_with(
            "POST",
            "/v3/connectors/google/creds",
            None,
            None,
            request_body,
            overrides=None,
        )

    def test_update_credential(self, http_client_response):
        credentials = Credentials(http_client_response)
        request_body = {
            "name": "My first Google credential",
            "credential_data": {
                "private_key_id": "string",
                "private_key": "string",
                "client_email": "string",
            },
        }

        credentials.update(
            provider="google",
            credential_id="abc-123",
            request_body=request_body,
        )

        http_client_response._execute.assert_called_once_with(
            "PATCH",
            "/v3/connectors/google/creds/abc-123",
            None,
            None,
            request_body,
            overrides=None,
        )

    def test_destroy_credential(self, http_client_delete_response):
        credentials = Credentials(http_client_delete_response)

        credentials.destroy("google", "abc-123")

        http_client_delete_response._execute.assert_called_once_with(
            "DELETE",
            "/v3/connectors/google/creds/abc-123",
            None,
            None,
            None,
            overrides=None,
        )

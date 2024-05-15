from nylas.models.grants import Grant
from nylas.resources.grants import Grants


class TestGrants:
    def test_grant_deserialization(self, http_client):
        grant_json = {
            "id": "e19f8e1a-eb1c-41c0-b6a6-d2e59daf7f47",
            "provider": "google",
            "grant_status": "valid",
            "email": "email@example.com",
            "scope": ["Mail.Read", "User.Read", "offline_access"],
            "user_agent": "string",
            "ip": "string",
            "state": "my-state",
            "created_at": 1617817109,
            "updated_at": 1617817109,
        }

        grant = Grant.from_dict(grant_json)

        assert grant.id == "e19f8e1a-eb1c-41c0-b6a6-d2e59daf7f47"
        assert grant.provider == "google"
        assert grant.grant_status == "valid"
        assert grant.email == "email@example.com"
        assert grant.scope == ["Mail.Read", "User.Read", "offline_access"]
        assert grant.user_agent == "string"
        assert grant.ip == "string"
        assert grant.state == "my-state"
        assert grant.created_at == 1617817109
        assert grant.updated_at == 1617817109

    def test_list_grants(self, http_client_list_response):
        grants = Grants(http_client_list_response)

        grants.list()

        http_client_list_response._execute.assert_called_once_with(
            "GET", "/v3/grants", None, None, None, overrides=None
        )

    def test_find_grant(self, http_client_response):
        grants = Grants(http_client_response)

        grants.find("grant-123")

        http_client_response._execute.assert_called_once_with(
            "GET", "/v3/grants/grant-123", None, None, None, overrides=None
        )

    def test_update_grant(self, http_client_response):
        grants = Grants(http_client_response)
        request_body = {
            "settings": {
                "client_id": "string",
                "client_secret": "string",
            },
            "scope": [
                "https://www.googleapis.com/auth/userinfo.email",
                "https://www.googleapis.com/auth/userinfo.profile",
            ],
        }

        grants.update(
            grant_id="grant-123",
            request_body=request_body,
        )

        http_client_response._execute.assert_called_once_with(
            "PUT", "/v3/grants/grant-123", None, None, request_body, overrides=None
        )

    def test_destroy_grant(self, http_client_delete_response):
        grants = Grants(http_client_delete_response)

        grants.destroy("grant-123")

        http_client_delete_response._execute.assert_called_once_with(
            "DELETE", "/v3/grants/grant-123", None, None, None, overrides=None
        )

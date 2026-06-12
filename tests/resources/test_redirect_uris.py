from nylas.resources.redirect_uris import RedirectUris

from nylas.models.redirect_uri import RedirectUri


class TestRedirectUri:
    def test_redirect_uri_deserialization(self):
        redirect_uri_json = {
            "id": "0556d035-6cb6-4262-a035-6b77e11cf8fc",
            "url": "http://localhost/abc",
            "platform": "web",
            "settings": {
                "origin": "string",
                "bundle_id": "string",
                "app_store_id": "string",
                "team_id": "string",
                "package_name": "string",
                "sha1_certificate_fingerprint": "string",
            },
            "deleted_at": 1620000000,
        }

        redirect_uri = RedirectUri.from_dict(redirect_uri_json)

        assert redirect_uri.id == "0556d035-6cb6-4262-a035-6b77e11cf8fc"
        assert redirect_uri.url == "http://localhost/abc"
        assert redirect_uri.platform == "web"
        assert redirect_uri.settings.origin == "string"
        assert redirect_uri.settings.bundle_id == "string"
        assert redirect_uri.settings.app_store_id == "string"
        assert redirect_uri.settings.team_id == "string"
        assert redirect_uri.settings.package_name == "string"
        assert redirect_uri.settings.sha1_certificate_fingerprint == "string"
        # deleted_at is an Optional soft-delete timestamp per the applications spec
        assert redirect_uri.deleted_at == 1620000000

    def test_redirect_uri_deserialization_without_deleted_at(self):
        # deleted_at is omitted when the URI is not soft-deleted; must default to None
        redirect_uri_json = {
            "id": "0556d035-6cb6-4262-a035-6b77e11cf8fc",
            "url": "http://localhost/abc",
            "platform": "web",
        }

        redirect_uri = RedirectUri.from_dict(redirect_uri_json)

        assert redirect_uri.deleted_at is None

    def test_list_redirect_uris(self, http_client_list_response):
        redirect_uris = RedirectUris(http_client_list_response)

        redirect_uris.list()

        http_client_list_response._execute.assert_called_once_with(
            "GET", "/v3/applications/redirect-uris", None, None, None, overrides=None
        )

    def test_find_redirect_uri(self, http_client_response):
        redirect_uris = RedirectUris(http_client_response)

        redirect_uris.find(redirect_uri_id="redirect_uri-123")

        http_client_response._execute.assert_called_once_with(
            "GET",
            "/v3/applications/redirect-uris/redirect_uri-123",
            None,
            None,
            None,
            overrides=None,
        )

    def test_create_redirect_uri(self, http_client_response):
        redirect_uris = RedirectUris(http_client_response)
        request_body = {
            "url": "http://localhost/abc",
            "platform": "web",
            "settings": {
                "origin": "string",
                "bundle_id": "string",
                "app_store_id": "string",
                "team_id": "string",
                "package_name": "string",
                "sha1_certificate_fingerprint": "string",
            },
        }

        redirect_uris.create(request_body=request_body)

        http_client_response._execute.assert_called_once_with(
            "POST",
            "/v3/applications/redirect-uris",
            None,
            None,
            request_body,
            overrides=None,
        )

    def test_update_redirect_uri(self, http_client_response):
        redirect_uris = RedirectUris(http_client_response)
        request_body = {
            "url": "http://localhost/abc",
            "platform": "web",
            "settings": {
                "origin": "string",
                "bundle_id": "string",
                "app_store_id": "string",
                "team_id": "string",
                "package_name": "string",
                "sha1_certificate_fingerprint": "string",
            },
        }

        redirect_uris.update(
            redirect_uri_id="redirect_uri-123",
            request_body=request_body,
        )

        # Update must use PATCH, not PUT, per the applications spec
        # (POST regenerates the id server-side; PATCH preserves the path id).
        http_client_response._execute.assert_called_once_with(
            "PATCH",
            "/v3/applications/redirect-uris/redirect_uri-123",
            None,
            None,
            request_body,
            overrides=None,
        )

    def test_destroy_redirect_uri(self, http_client_delete_response):
        redirect_uris = RedirectUris(http_client_delete_response)

        redirect_uris.destroy(redirect_uri_id="redirect_uri-123")

        http_client_delete_response._execute.assert_called_once_with(
            "DELETE",
            "/v3/applications/redirect-uris/redirect_uri-123",
            None,
            None,
            None,
            overrides=None,
        )

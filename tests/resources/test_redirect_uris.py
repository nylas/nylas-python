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

    def test_list_redirect_uris(self, http_client_list_response):
        redirect_uris = RedirectUris(http_client_list_response)

        redirect_uris.list()

        http_client_list_response._execute.assert_called_once_with(
            "GET", "/v3/redirect-uris", None, None, None
        )

    def test_find_redirect_uri(self, http_client_response):
        redirect_uris = RedirectUris(http_client_response)

        redirect_uris.find(redirect_uri_id="redirect_uri-123")

        http_client_response._execute.assert_called_once_with(
            "GET", "/v3/redirect-uris/redirect_uri-123", None, None, None
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
            "/v3/redirect-uris",
            None,
            None,
            request_body,
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

        http_client_response._execute.assert_called_once_with(
            "PUT",
            "/v3/redirect-uris/redirect_uri-123",
            None,
            None,
            request_body,
        )

    def test_destroy_redirect_uri(self, http_client_delete_response):
        redirect_uris = RedirectUris(http_client_delete_response)

        redirect_uris.destroy(redirect_uri_id="redirect_uri-123")

        http_client_delete_response._execute.assert_called_once_with(
            "DELETE",
            "/v3/redirect-uris/redirect_uri-123",
            None,
            None,
            None,
        )

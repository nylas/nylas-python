from unittest.mock import Mock

from nylas.models.application_details import ApplicationDetails

from nylas.resources.redirect_uris import RedirectUris

from nylas.resources.applications import Applications


class TestApplications:
    def test_redirect_uris_property(self, http_client):
        applications = Applications(http_client)
        assert isinstance(applications.redirect_uris, RedirectUris)

    def test_info(self):
        mock_http_client = Mock()
        mock_http_client._execute.return_value = (
            {
                "request_id": "req-123",
                "data": {
                    "application_id": "ad410018-d306-43f9-8361-fa5d7b2172e0",
                    "organization_id": "f5db4482-dbbe-4b32-b347-61c260d803ce",
                    "region": "us",
                    "environment": "production",
                    "branding": {
                        "name": "My application",
                        "icon_url": "https://my-app.com/my-icon.png",
                        "website_url": "https://my-app.com",
                        "description": "Online banking application.",
                    },
                    "hosted_authentication": {
                        "background_image_url": "https://my-app.com/bg.jpg",
                        "alignment": "left",
                        "color_primary": "#dc0000",
                        "color_secondary": "#000056",
                        "title": "string",
                        "subtitle": "string",
                        "background_color": "#003400",
                        "spacing": 5,
                    },
                    "callback_uris": [
                        {
                            "id": "0556d035-6cb6-4262-a035-6b77e11cf8fc",
                            "url": "string",
                            "platform": "web",
                            "settings": {
                                "origin": "string",
                                "bundle_id": "string",
                                "package_name": "string",
                                "sha1_certificate_fingerprint": "string",
                            },
                        }
                    ],
                },
            },
            {"X-Test-Header": "test"},
        )
        app = Applications(mock_http_client)

        res = app.info()

        mock_http_client._execute.assert_called_once_with(
            method="GET", path="/v3/applications", overrides=None
        )
        assert type(res.data) == ApplicationDetails
        assert res.data.application_id == "ad410018-d306-43f9-8361-fa5d7b2172e0"
        assert res.data.organization_id == "f5db4482-dbbe-4b32-b347-61c260d803ce"
        assert res.data.region == "us"
        assert res.data.environment == "production"
        assert res.data.branding.name == "My application"
        assert res.data.branding.icon_url == "https://my-app.com/my-icon.png"
        assert res.data.branding.website_url == "https://my-app.com"
        assert res.data.branding.description == "Online banking application."
        assert (
            res.data.hosted_authentication.background_image_url
            == "https://my-app.com/bg.jpg"
        )
        assert res.data.hosted_authentication.alignment == "left"
        assert res.data.hosted_authentication.color_primary == "#dc0000"
        assert res.data.hosted_authentication.color_secondary == "#000056"
        assert res.data.hosted_authentication.title == "string"
        assert res.data.hosted_authentication.subtitle == "string"
        assert res.data.hosted_authentication.background_color == "#003400"
        assert res.data.hosted_authentication.spacing == 5
        assert res.data.callback_uris[0].id == "0556d035-6cb6-4262-a035-6b77e11cf8fc"
        assert res.data.callback_uris[0].url == "string"
        assert res.data.callback_uris[0].platform == "web"
        assert res.data.callback_uris[0].settings.origin == "string"
        assert res.data.callback_uris[0].settings.bundle_id == "string"
        assert res.data.callback_uris[0].settings.package_name == "string"
        assert (
            res.data.callback_uris[0].settings.sha1_certificate_fingerprint == "string"
        )

    def test_info_extended_response_fields(self):
        """idp_settings, hosted_authentication URL fields, and optional top-level
        fields are public response fields and must deserialize."""
        mock_http_client = Mock()
        mock_http_client._execute.return_value = (
            {
                "request_id": "req-123",
                "data": {
                    "application_id": "ad410018-d306-43f9-8361-fa5d7b2172e0",
                    "organization_id": "f5db4482-dbbe-4b32-b347-61c260d803ce",
                    "unexpected_response_id": "unexpected-value",
                    "region": "eu",
                    "environment": "sandbox",
                    "domain": "auth.example.com",
                    "branding": {"name": "My application"},
                    "hosted_authentication": {
                        "alignment": "diagonal",
                        "terms_of_service_url": "https://my-app.com/tos",
                        "privacy_policy_url": "https://my-app.com/privacy",
                    },
                    "idp_settings": {
                        "origins": "https://a.com,https://b.com",
                        "issuers": "issuer-a,issuer-b",
                    },
                    "created_at": 1700000000,
                    "updated_at": 1700000001,
                    "blocked": True,
                },
            },
            {"X-Test-Header": "test"},
        )
        app = Applications(mock_http_client)

        res = app.info()

        assert type(res.data) == ApplicationDetails
        assert not hasattr(res.data, "unexpected_response_id")
        assert "unexpected_response_id" not in res.data.to_dict()
        # region/environment are free-form strings, not enums (discrepancies #6, #7)
        assert res.data.region == "eu"
        assert res.data.environment == "sandbox"
        assert res.data.domain == "auth.example.com"
        # alignment is free-form, not a closed enum (discrepancy #5)
        assert res.data.hosted_authentication.alignment == "diagonal"
        assert (
            res.data.hosted_authentication.terms_of_service_url
            == "https://my-app.com/tos"
        )
        assert (
            res.data.hosted_authentication.privacy_policy_url
            == "https://my-app.com/privacy"
        )
        assert res.data.idp_settings.origins == "https://a.com,https://b.com"
        assert res.data.idp_settings.issuers == "issuer-a,issuer-b"
        assert res.data.created_at == 1700000000
        assert res.data.updated_at == 1700000001
        assert res.data.blocked is True

    def test_update(self):
        """Update is PATCH /v3/applications; additional_settings is write-only
        and accepted in the body (spec: PATCH-only, discrepancy #13)."""
        mock_http_client = Mock()
        mock_http_client._execute.return_value = (
            {
                "request_id": "req-456",
                "data": {
                    "application_id": "ad410018-d306-43f9-8361-fa5d7b2172e0",
                    "organization_id": "f5db4482-dbbe-4b32-b347-61c260d803ce",
                    "region": "us",
                    "environment": "production",
                    "branding": {"name": "Updated application"},
                },
            },
            {"X-Test-Header": "test"},
        )
        app = Applications(mock_http_client)

        request_body = {
            "branding": {"name": "Updated application"},
            "hosted_authentication": {"title": "Welcome"},
            "idp_settings": {"origins": "https://a.com"},
            "callback_uris": [
                {
                    "id": "0556d035-6cb6-4262-a035-6b77e11cf8fc",
                    "url": "https://example.com/callback",
                    "platform": "web",
                }
            ],
            "domain": "auth.example.com",
            "additional_settings": {"rotate_refresh_token": True},
        }

        res = app.update(request_body=request_body)

        # Must be PATCH (no PUT) at /v3/applications with the exact body
        mock_http_client._execute.assert_called_once_with(
            "PATCH",
            "/v3/applications",
            None,
            None,
            request_body,
            overrides=None,
        )
        assert type(res.data) == ApplicationDetails
        assert res.data.branding.name == "Updated application"

from unittest.mock import patch

import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from nylas.handler.service_account import ServiceAccountSigner
from nylas.models.domains import Domain, DomainVerificationDetails
from nylas.models.response import ListResponse, Response
from nylas.resources import domains as domains_module
from nylas.resources.domains import Domains

SERVICE_ACCOUNT_HEADERS = {
    "X-Nylas-Kid": "service-account-key-id",
    "X-Nylas-Timestamp": "1742932766",
    "X-Nylas-Nonce": "nonce-1234567890123456",
    "X-Nylas-Signature": "signed-request",
}


def service_account_overrides(headers=None):
    return {"headers": headers or SERVICE_ACCOUNT_HEADERS, "skip_auth": True}


def _test_rsa_pem():
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    return key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode("ascii")


@pytest.fixture
def domain_data():
    return {
        "id": "dom_123",
        "name": "My domain",
        "branded": False,
        "domain_address": "mail.example.com",
        "organization_id": "org_1",
        "region": "us",
        "verified_ownership": False,
        "verified_dkim": False,
        "verified_spf": False,
        "verified_mx": False,
        "verified_feedback": False,
        "verified_dmarc": False,
        "verified_arc": False,
        "created_at": 1,
        "updated_at": 2,
    }


class TestMergeSignerHeaders:
    def test_returns_overrides_when_no_signer_headers(self):
        assert domains_module._merge_signer_headers({"timeout": 5}, None) == {
            "timeout": 5
        }
        assert domains_module._merge_signer_headers(None, {}) is None

    def test_merges_headers_preserving_existing(self):
        merged = domains_module._merge_signer_headers(
            {"headers": {"X-Existing": "keep"}, "timeout": 30},
            {"X-Nylas-Kid": "kid", "X-Nylas-Signature": "sig"},
        )
        assert merged["timeout"] == 30
        assert merged["headers"]["X-Existing"] == "keep"
        assert merged["headers"]["X-Nylas-Kid"] == "kid"
        assert merged["headers"]["X-Nylas-Signature"] == "sig"

    def test_creates_overrides_when_none(self):
        merged = domains_module._merge_signer_headers(None, {"X-Nylas-Kid": "kid"})
        assert merged == {"headers": {"X-Nylas-Kid": "kid"}}


class TestDomains:
    def test_domain_model_from_dict(self, domain_data):
        d = Domain.from_dict(domain_data)
        assert d.id == "dom_123"
        assert d.domain_address == "mail.example.com"

    def test_domain_verification_details_from_dict(self):
        raw = {
            "domain_id": "d1",
            "attempt": {"type": "dkim", "status": "pending"},
            "message": "add TXT",
        }
        d = DomainVerificationDetails.from_dict(raw, infer_missing=True)
        assert d.domain_id == "d1"
        assert d.attempt is not None
        assert d.attempt.verification_type == "dkim"
        assert d.message == "add TXT"

    def test_rejects_api_key_only_requests(self, http_client_list_response):
        domains = Domains(http_client_list_response)

        with pytest.raises(ValueError, match="Service Account signing headers"):
            domains.list()

        http_client_list_response._execute.assert_not_called()

    def test_list_with_signed_headers(self, http_client_list_response):
        with patch(
            "nylas.models.response.ListResponse.from_dict",
            return_value=ListResponse([], "rid", None, {}),
        ):
            domains = Domains(http_client_list_response)
            domains.list(overrides={"headers": SERVICE_ACCOUNT_HEADERS})
        http_client_list_response._execute.assert_called_once_with(
            "GET",
            "/v3/admin/domains",
            None,
            None,
            None,
            overrides=service_account_overrides(),
        )

    def test_list_with_query_and_signer(self, http_client_list_response):
        pem = _test_rsa_pem()
        signer = ServiceAccountSigner(pem, "kid-1")
        with patch(
            "nylas.models.response.ListResponse.from_dict",
            return_value=ListResponse([], "rid", None, {}),
        ):
            domains = Domains(http_client_list_response)
            domains.list(query_params={"limit": 10}, signer=signer)
        args, kwargs = http_client_list_response._execute.call_args
        assert args[0] == "GET"
        assert "/v3/admin/domains" in args[1]
        ov = kwargs.get("overrides") or {}
        assert ov.get("skip_auth") is True
        assert "X-Nylas-Signature" in (ov.get("headers") or {})

    def test_create_with_signed_headers(self, http_client_response, domain_data):
        with patch(
            "nylas.models.response.Response.from_dict",
            return_value=Response(domain_data, "rid", {}),
        ):
            domains = Domains(http_client_response)
            domains.create(
                {"name": "My domain", "domain_address": "mail.example.com"},
                overrides={"headers": SERVICE_ACCOUNT_HEADERS},
            )
        http_client_response._execute.assert_called_once_with(
            "POST",
            "/v3/admin/domains",
            None,
            None,
            None,
            overrides=service_account_overrides(),
            serialized_json_body=b'{"domain_address":"mail.example.com","name":"My domain"}',
        )

    def test_find_with_signed_headers(self, http_client_response, domain_data):
        with patch(
            "nylas.models.response.Response.from_dict",
            return_value=Response(domain_data, "rid", {}),
        ):
            domains = Domains(http_client_response)
            domains.find(
                "mail/example.com", overrides={"headers": SERVICE_ACCOUNT_HEADERS}
            )
        http_client_response._execute.assert_called_once_with(
            "GET",
            "/v3/admin/domains/mail%2Fexample.com",
            None,
            None,
            None,
            overrides=service_account_overrides(),
        )

    def test_find_with_signer(self, http_client_response, domain_data):
        pem = _test_rsa_pem()
        signer = ServiceAccountSigner(pem, "kid-x")
        with patch(
            "nylas.models.response.Response.from_dict",
            return_value=Response(domain_data, "rid", {}),
        ):
            domains = Domains(http_client_response)
            domains.find("dom_abc", signer=signer)
        ov = http_client_response._execute.call_args.kwargs.get("overrides") or {}
        assert ov.get("skip_auth") is True
        assert "X-Nylas-Signature" in (ov.get("headers") or {})

    def test_update_with_signed_headers(self, http_client_response, domain_data):
        with patch(
            "nylas.models.response.Response.from_dict",
            return_value=Response(domain_data, "rid", {}),
        ):
            domains = Domains(http_client_response)
            domains.update(
                "dom_123",
                {"name": "Renamed"},
                overrides={"headers": SERVICE_ACCOUNT_HEADERS},
            )
        http_client_response._execute.assert_called_once_with(
            "PUT",
            "/v3/admin/domains/dom_123",
            None,
            None,
            None,
            overrides=service_account_overrides(),
            serialized_json_body=b'{"name":"Renamed"}',
        )

    def test_update_with_signer(self, http_client_response, domain_data):
        pem = _test_rsa_pem()
        signer = ServiceAccountSigner(pem, "kid-1")
        with patch(
            "nylas.models.response.Response.from_dict",
            return_value=Response(domain_data, "rid", {}),
        ):
            domains = Domains(http_client_response)
            domains.update("dom_123", {"name": "Renamed"}, signer=signer)
        kwargs = http_client_response._execute.call_args.kwargs
        assert kwargs["overrides"]["skip_auth"] is True
        assert "serialized_json_body" in kwargs
        assert http_client_response._execute.call_args[0][4] is None

    def test_create_with_signer_sends_serialized_body(
        self, http_client_response, domain_data
    ):
        pem = _test_rsa_pem()
        signer = ServiceAccountSigner(pem, "kid-1")
        with patch(
            "nylas.models.response.Response.from_dict",
            return_value=Response(domain_data, "rid", {}),
        ):
            domains = Domains(http_client_response)
            domains.create(
                {"name": "My domain", "domain_address": "mail.example.com"},
                signer=signer,
            )
        kwargs = http_client_response._execute.call_args.kwargs
        assert kwargs["overrides"]["skip_auth"] is True
        assert "serialized_json_body" in kwargs
        assert kwargs["serialized_json_body"].startswith(b"{")
        pos = http_client_response._execute.call_args[0]
        assert pos[4] is None

    def test_destroy_with_signer(self, http_client_delete_response):
        from nylas.models.response import DeleteResponse

        pem = _test_rsa_pem()
        signer = ServiceAccountSigner(pem, "kid-del")
        http_client_delete_response._execute.return_value = (
            {"request_id": "del-rid"},
            {},
        )
        domains = Domains(http_client_delete_response)
        domains.destroy("dom_123", signer=signer)
        ov = http_client_delete_response._execute.call_args.kwargs["overrides"]
        assert ov["skip_auth"] is True
        assert "X-Nylas-Signature" in ov["headers"]

    def test_destroy_with_signed_headers(self, http_client_delete_response):
        from nylas.models.response import DeleteResponse

        http_client_delete_response._execute.return_value = (
            {"request_id": "del-rid"},
            {},
        )
        domains = Domains(http_client_delete_response)
        out = domains.destroy("dom_123", overrides={"headers": SERVICE_ACCOUNT_HEADERS})
        assert isinstance(out, DeleteResponse)
        http_client_delete_response._execute.assert_called_once_with(
            "DELETE",
            "/v3/admin/domains/dom_123",
            None,
            None,
            None,
            overrides=service_account_overrides(),
        )

    def test_get_info_with_signer(self, http_client_response):
        pem = _test_rsa_pem()
        signer = ServiceAccountSigner(pem, "kid-i")
        info = {"domain_id": "dom_123", "attempt": {"type": "spf"}}
        http_client_response._execute.return_value = (
            {"request_id": "r1", "data": info},
            {},
        )
        with patch(
            "nylas.models.response.Response.from_dict",
            return_value=Response(info, "r1", {}),
        ):
            domains = Domains(http_client_response)
            domains.get_info("dom_123", {"type": "spf"}, signer=signer)
        kwargs = http_client_response._execute.call_args.kwargs
        assert kwargs["overrides"]["skip_auth"] is True
        assert "serialized_json_body" in kwargs
        assert http_client_response._execute.call_args[0][4] is None

    def test_verify_with_signed_headers(self, http_client_response):
        info = {"domain_id": "dom_123", "attempt": {"type": "mx"}}
        http_client_response._execute.return_value = (
            {"request_id": "rv", "data": info},
            {},
        )
        with patch(
            "nylas.models.response.Response.from_dict",
            return_value=Response(info, "rv", {}),
        ):
            domains = Domains(http_client_response)
            domains.verify(
                "dom_123",
                {"type": "mx"},
                overrides={"headers": SERVICE_ACCOUNT_HEADERS},
            )
        http_client_response._execute.assert_called_once_with(
            "POST",
            "/v3/admin/domains/dom_123/verify",
            None,
            None,
            None,
            overrides=service_account_overrides(),
            serialized_json_body=b'{"type":"mx"}',
        )

    def test_verify_with_signer(self, http_client_response):
        pem = _test_rsa_pem()
        signer = ServiceAccountSigner(pem, "kid-v")
        info = {"domain_id": "dom_123"}
        http_client_response._execute.return_value = (
            {"request_id": "rv", "data": info},
            {},
        )
        with patch(
            "nylas.models.response.Response.from_dict",
            return_value=Response(info, "rv", {}),
        ):
            domains = Domains(http_client_response)
            domains.verify("dom_123", {"type": "dkim"}, signer=signer)
        kwargs = http_client_response._execute.call_args.kwargs
        assert kwargs["overrides"]["skip_auth"] is True
        assert "serialized_json_body" in kwargs

    def test_get_info_with_signed_headers(self, http_client_response):
        info = {
            "domain_id": "dom_123",
            "attempt": {"type": "ownership", "status": "pending"},
        }
        http_client_response._execute.return_value = (
            {"request_id": "r1", "data": info},
            {},
        )
        with patch(
            "nylas.models.response.Response.from_dict",
            return_value=Response(info, "r1", {}),
        ):
            domains = Domains(http_client_response)
            domains.get_info(
                "dom_123",
                {"type": "ownership"},
                overrides={"headers": SERVICE_ACCOUNT_HEADERS},
            )
        http_client_response._execute.assert_called_once_with(
            "POST",
            "/v3/admin/domains/dom_123/info",
            None,
            None,
            None,
            overrides=service_account_overrides(),
            serialized_json_body=b'{"type":"ownership"}',
        )

    def test_get_info_accepts_extended_verification_options(self, http_client_response):
        info = {
            "domain_id": "dom_123",
            "attempt": {"type": "dkim", "options": {"key_length": 2048}},
        }
        http_client_response._execute.return_value = (
            {"request_id": "r1", "data": info},
            {},
        )
        with patch(
            "nylas.models.response.Response.from_dict",
            return_value=Response(info, "r1", {}),
        ):
            domains = Domains(http_client_response)
            domains.get_info(
                "dom_123",
                {"type": "dkim", "options": {"key_length": 2048}},
                overrides={"headers": SERVICE_ACCOUNT_HEADERS},
            )
        http_client_response._execute.assert_called_once_with(
            "POST",
            "/v3/admin/domains/dom_123/info",
            None,
            None,
            None,
            overrides=service_account_overrides(),
            serialized_json_body=b'{"options":{"key_length":2048},"type":"dkim"}',
        )

    def test_merge_signer_with_existing_headers(self, http_client_list_response):
        pem = _test_rsa_pem()
        signer = ServiceAccountSigner(pem, "kid-1")
        with patch(
            "nylas.models.response.ListResponse.from_dict",
            return_value=ListResponse([], "rid", None, {}),
        ):
            domains = Domains(http_client_list_response)
            domains.list(
                signer=signer,
                overrides={"headers": {"X-Custom": "precedence"}},
            )
        headers = http_client_list_response._execute.call_args.kwargs["overrides"][
            "headers"
        ]
        assert (
            http_client_list_response._execute.call_args.kwargs["overrides"][
                "skip_auth"
            ]
            is True
        )
        assert headers["X-Custom"] == "precedence"
        assert "X-Nylas-Kid" in headers

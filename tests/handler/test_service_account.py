import base64
import string

import pytest
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, padding, rsa

from nylas.handler.service_account import (
    ServiceAccountSigner,
    _signing_envelope_bytes,
    canonical_json,
    generate_nonce,
    load_rsa_private_key_from_pem,
    sign_bytes,
)


class TestCanonicalJson:
    def test_sorted_keys_flat(self):
        assert canonical_json({"b": 1, "a": 2}) == '{"a":2,"b":1}'

    def test_nested_dict_sorted(self):
        assert (
            canonical_json({"z": {"b": 1, "a": 2}, "y": 0})
            == '{"y":0,"z":{"a":2,"b":1}}'
        )

    def test_string_escaping(self):
        s = canonical_json({"msg": 'quote"here'})
        assert s.startswith("{")
        assert '"msg":' in s
        assert "quote" in s

    def test_list_and_bool_values_use_json_dumps(self):
        s = canonical_json({"ok": True, "items": [3, 1, 2]})
        assert '"items":[3,1,2]' in s
        assert '"ok":true' in s


class TestServiceAccountSigning:
    @pytest.fixture
    def rsa_pem(self):
        key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        return (
            key,
            key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            ).decode("ascii"),
        )

    def test_load_pkcs8_pem(self, rsa_pem):
        _, pem = rsa_pem
        loaded = load_rsa_private_key_from_pem(pem)
        assert isinstance(loaded, rsa.RSAPrivateKey)

    def test_load_pkcs1_traditional_pem(self, rsa_pem):
        private_key, _ = rsa_pem
        pem_pkcs1 = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )
        loaded = load_rsa_private_key_from_pem(pem_pkcs1)
        assert isinstance(loaded, rsa.RSAPrivateKey)

    def test_load_pem_accepts_bytes(self, rsa_pem):
        _, pem = rsa_pem
        loaded = load_rsa_private_key_from_pem(pem.encode("ascii"))
        assert isinstance(loaded, rsa.RSAPrivateKey)

    def test_load_non_rsa_raises(self):
        ec_key = ec.generate_private_key(ec.SECP256R1())
        pem = ec_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        ).decode("ascii")
        with pytest.raises(ValueError, match="Private key must be RSA"):
            load_rsa_private_key_from_pem(pem)

    def test_sign_bytes_verifies_with_public_key(self, rsa_pem):
        private_key, pem = rsa_pem
        message = b"hello nylas canonical envelope"
        sig_b64 = sign_bytes(private_key, message)
        sig = base64.b64decode(sig_b64)
        public_key = private_key.public_key()
        public_key.verify(sig, message, padding.PKCS1v15(), hashes.SHA256())

    def test_golden_envelope_signature_round_trip(self, rsa_pem):
        """Fixed inputs: signature must verify (independent of ServiceAccountSigner time)."""
        private_key, pem = rsa_pem
        path = "/v3/admin/domains"
        ts = 1742932766
        nonce = "abcdefabcdefabcdefab"
        body = {"type": "ownership"}
        envelope = _signing_envelope_bytes(path, "POST", ts, nonce, body)
        sig_b64 = sign_bytes(private_key, envelope)
        sig = base64.b64decode(sig_b64)
        private_key.public_key().verify(sig, envelope, padding.PKCS1v15(), hashes.SHA256())

    def test_service_account_signer_build_headers_post(self, rsa_pem):
        private_key, pem = rsa_pem
        signer = ServiceAccountSigner(pem, "test-kid-uuid")
        headers, body_bytes = signer.build_headers(
            "POST",
            "/v3/admin/domains",
            {"name": "My domain", "domain_address": "mail.example.com"},
            timestamp=1700000000,
            nonce="nonce123456789012345",
        )
        assert headers["X-Nylas-Kid"] == "test-kid-uuid"
        assert headers["X-Nylas-Nonce"] == "nonce123456789012345"
        assert headers["X-Nylas-Timestamp"] == "1700000000"
        assert len(headers["X-Nylas-Signature"]) > 0
        assert body_bytes == canonical_json(
            {"name": "My domain", "domain_address": "mail.example.com"}
        ).encode("utf-8")

        envelope = _signing_envelope_bytes(
            "/v3/admin/domains",
            "POST",
            1700000000,
            "nonce123456789012345",
            {"name": "My domain", "domain_address": "mail.example.com"},
        )
        sig = base64.b64decode(headers["X-Nylas-Signature"])
        private_key.public_key().verify(sig, envelope, padding.PKCS1v15(), hashes.SHA256())

    def test_service_account_signer_get_no_body_bytes(self, rsa_pem):
        _, pem = rsa_pem
        signer = ServiceAccountSigner(pem, "kid")
        headers, body_bytes = signer.build_headers(
            "GET", "/v3/admin/domains", None, timestamp=1, nonce="n" * 20
        )
        assert body_bytes is None
        assert "X-Nylas-Signature" in headers

    def test_signing_envelope_get_omits_payload(self, rsa_pem):
        private_key, _ = rsa_pem
        env = _signing_envelope_bytes("/v3/admin/domains", "GET", 1, "n" * 20, None)
        assert b"payload" not in env
        sig_b64 = sign_bytes(private_key, env)
        private_key.public_key().verify(
            base64.b64decode(sig_b64), env, padding.PKCS1v15(), hashes.SHA256()
        )

    def test_signing_envelope_put_and_patch_include_payload(self, rsa_pem):
        private_key, _ = rsa_pem
        for method in ("PUT", "patch"):
            env = _signing_envelope_bytes(
                "/v3/admin/domains/x", method, 2, "m" * 20, {"name": "n"}
            )
            assert b"payload" in env
            sig_b64 = sign_bytes(private_key, env)
            private_key.public_key().verify(
                base64.b64decode(sig_b64), env, padding.PKCS1v15(), hashes.SHA256()
            )

    def test_generate_nonce_custom_length(self):
        n = generate_nonce(12)
        assert len(n) == 12
        assert all(c in (string.ascii_letters + string.digits) for c in n)

    def test_build_headers_patch(self, rsa_pem):
        _, pem = rsa_pem
        signer = ServiceAccountSigner(pem, "kid")
        headers, body_bytes = signer.build_headers(
            "PATCH",
            "/v3/admin/example",
            {"op": "replace"},
            timestamp=9,
            nonce="z" * 20,
        )
        assert body_bytes == canonical_json({"op": "replace"}).encode("utf-8")
        assert headers["X-Nylas-Timestamp"] == "9"

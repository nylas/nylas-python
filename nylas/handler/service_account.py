"""
Nylas Service Account request signing for organization admin APIs.

See https://developer.nylas.com/docs/v3/auth/nylas-service-account/

If you set X-Nylas-* headers manually via RequestOverrides, the HTTP request body must be
byte-identical to the canonical JSON string used when computing the signature.
"""

from __future__ import annotations

import base64
import json
import secrets
import string
import time
from typing import Any, Dict, Optional, Tuple

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa

_NONCE_ALPHABET = string.ascii_letters + string.digits
_NONCE_LENGTH = 20


def canonical_json(data: Dict[str, Any]) -> str:
    """
    Deterministic JSON with sorted keys at each object level, matching Nylas's reference
    implementation for service account signing.
    """
    keys = sorted(data.keys())
    parts = []
    for k in keys:
        key_json = json.dumps(k, ensure_ascii=False, allow_nan=False)
        v = data[k]
        if isinstance(v, dict):
            val_json = canonical_json(v)
        else:
            val_json = json.dumps(
                v, ensure_ascii=False, allow_nan=False, separators=(",", ":")
            )
        parts.append(f"{key_json}:{val_json}")
    return "{" + ",".join(parts) + "}"


def load_rsa_private_key_from_pem(pem: str) -> rsa.RSAPrivateKey:
    """Load an RSA private key from a PEM string (PKCS#1 or PKCS#8)."""
    key_bytes = pem.encode("utf-8") if isinstance(pem, str) else pem
    loaded = serialization.load_pem_private_key(key_bytes, password=None)
    if not isinstance(loaded, rsa.RSAPrivateKey):
        raise ValueError("Private key must be RSA")
    return loaded


def _signing_envelope_bytes(
    path: str,
    method: str,
    timestamp: int,
    nonce: str,
    body: Optional[Dict[str, Any]],
) -> bytes:
    method_l = method.lower()
    envelope: Dict[str, Any] = {
        "method": method_l,
        "nonce": nonce,
        "path": path,
        "timestamp": timestamp,
    }
    if method_l in ("post", "put", "patch") and body is not None:
        envelope["payload"] = canonical_json(body)
    canonical = canonical_json(envelope)
    return canonical.encode("utf-8")


def sign_bytes(private_key: rsa.RSAPrivateKey, message: bytes) -> str:
    """RSA PKCS#1 v1.5 signature over SHA-256(message), Base64-encoded."""
    signature = private_key.sign(message, padding.PKCS1v15(), hashes.SHA256())
    return base64.b64encode(signature).decode("ascii")


def generate_nonce(length: int = _NONCE_LENGTH) -> str:
    """Cryptographically secure nonce (alphanumeric), default length 20."""
    return "".join(secrets.choice(_NONCE_ALPHABET) for _ in range(length))


class ServiceAccountSigner:
    """
    Builds the four required Nylas service account headers for a single request.

    Args:
        private_key_pem: RSA private key in PEM text form (from the service account JSON).
        private_key_id: Value for X-Nylas-Kid (``private_key_id`` in the JSON credentials).
    """

    def __init__(self, private_key_pem: str, private_key_id: str):
        self._private_key = load_rsa_private_key_from_pem(private_key_pem)
        self._private_key_id = private_key_id

    def build_headers(
        self,
        method: str,
        path: str,
        body: Optional[Dict[str, Any]] = None,
        *,
        timestamp: Optional[int] = None,
        nonce: Optional[str] = None,
    ) -> Tuple[Dict[str, str], Optional[bytes]]:
        """
        Produce signing headers and optional canonical JSON body bytes.

        For POST/PUT/PATCH, ``body`` must be the same dict that will be sent; returned bytes
        should be passed to HttpClient as ``serialized_json_body`` so the wire body matches
        the signed payload.

        Returns:
            (headers, serialized_json_body) where serialized_json_body is set for
            POST/PUT/PATCH when body is not None, else None.
        """
        ts = int(time.time()) if timestamp is None else int(timestamp)
        n = generate_nonce() if nonce is None else nonce

        serialized: Optional[bytes] = None
        body_for_sign: Optional[Dict[str, Any]] = body
        if method.lower() in ("post", "put", "patch") and body is not None:
            serialized = canonical_json(body).encode("utf-8")

        envelope = _signing_envelope_bytes(path, method, ts, n, body_for_sign)
        signature_b64 = sign_bytes(self._private_key, envelope)

        headers = {
            "X-Nylas-Kid": self._private_key_id,
            "X-Nylas-Nonce": n,
            "X-Nylas-Timestamp": str(ts),
            "X-Nylas-Signature": signature_b64,
        }
        return headers, serialized

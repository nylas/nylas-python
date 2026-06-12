import urllib.parse
from typing import Optional

from nylas.config import RequestOverrides
from nylas.handler.api_resources import (
    CreatableApiResource,
    DestroyableApiResource,
    FindableApiResource,
    ListableApiResource,
    UpdatableApiResource,
)
from nylas.handler.service_account import ServiceAccountSigner, canonical_json
from nylas.models.domains import (
    CreateDomainRequest,
    Domain,
    DomainVerificationDetails,
    GetDomainInfoRequest,
    ListDomainsQueryParams,
    UpdateDomainRequest,
    VerifyDomainRequest,
)
from nylas.models.response import DeleteResponse, ListResponse, Response

_REQUIRED_SERVICE_ACCOUNT_HEADERS = (
    "x-nylas-kid",
    "x-nylas-timestamp",
    "x-nylas-nonce",
    "x-nylas-signature",
)


def _merge_signer_headers(
    overrides: Optional[RequestOverrides], signer_headers: Optional[dict]
) -> Optional[RequestOverrides]:
    if not signer_headers:
        return overrides
    merged: RequestOverrides = dict(overrides) if overrides else {}
    headers = dict(merged.get("headers") or {})
    headers.update(signer_headers)
    merged["headers"] = headers
    return merged


def _service_account_overrides(
    overrides: Optional[RequestOverrides],
) -> RequestOverrides:
    merged: RequestOverrides = dict(overrides) if overrides else {}
    merged["skip_auth"] = True
    return merged


def _require_service_account_headers(overrides: Optional[RequestOverrides]) -> None:
    headers = (overrides or {}).get("headers") or {}
    normalized = {key.lower(): value for key, value in headers.items()}
    missing = [
        header
        for header in _REQUIRED_SERVICE_ACCOUNT_HEADERS
        if not str(normalized.get(header, "")).strip()
    ]
    if missing:
        raise ValueError(
            "Manage Domains API requests require Nylas Service Account signing headers."
        )


def _encode_domain_id(domain_id: str) -> str:
    return urllib.parse.quote(domain_id, safe="")


def _canonical_body_bytes(request_body: dict) -> bytes:
    return canonical_json(dict(request_body)).encode("utf-8")


class Domains(
    ListableApiResource,
    FindableApiResource,
    CreatableApiResource,
    UpdatableApiResource,
    DestroyableApiResource,
):
    """
    Nylas Manage Domains API (``/v3/admin/domains``).

    Organization admin endpoints for registering and verifying email domains used with
    Transactional Send and Nylas Inbound. Optional :class:`ServiceAccountSigner` adds the
    required ``X-Nylas-*`` headers; you can also supply those headers via ``RequestOverrides``.
    """

    def list(
        self,
        query_params: Optional[ListDomainsQueryParams] = None,
        signer: Optional[ServiceAccountSigner] = None,
        overrides: RequestOverrides = None,
    ) -> ListResponse[Domain]:
        path = "/v3/admin/domains"
        merged = overrides
        if signer:
            hdrs, _ = signer.build_headers("GET", path, None)
            merged = _merge_signer_headers(overrides, hdrs)
        merged = _service_account_overrides(merged)
        _require_service_account_headers(merged)
        return super().list(
            path=path,
            response_type=Domain,
            query_params=query_params,
            overrides=merged,
        )

    def create(
        self,
        request_body: CreateDomainRequest,
        signer: Optional[ServiceAccountSigner] = None,
        overrides: RequestOverrides = None,
    ) -> Response[Domain]:
        path = "/v3/admin/domains"
        merged = overrides
        serialized = _canonical_body_bytes(request_body)
        body_arg = request_body
        if signer:
            hdrs, serialized = signer.build_headers("POST", path, dict(request_body))
            merged = _merge_signer_headers(overrides, hdrs)
        if serialized is not None:
            body_arg = None
        merged = _service_account_overrides(merged)
        _require_service_account_headers(merged)
        return super().create(
            path=path,
            request_body=body_arg,
            response_type=Domain,
            overrides=merged,
            serialized_json_body=serialized,
        )

    def find(
        self,
        domain_id: str,
        signer: Optional[ServiceAccountSigner] = None,
        overrides: RequestOverrides = None,
    ) -> Response[Domain]:
        path = f"/v3/admin/domains/{_encode_domain_id(domain_id)}"
        merged = overrides
        if signer:
            hdrs, _ = signer.build_headers("GET", path, None)
            merged = _merge_signer_headers(overrides, hdrs)
        merged = _service_account_overrides(merged)
        _require_service_account_headers(merged)
        return super().find(
            path=path,
            response_type=Domain,
            overrides=merged,
        )

    def update(
        self,
        domain_id: str,
        request_body: UpdateDomainRequest,
        signer: Optional[ServiceAccountSigner] = None,
        overrides: RequestOverrides = None,
    ) -> Response[Domain]:
        path = f"/v3/admin/domains/{_encode_domain_id(domain_id)}"
        merged = overrides
        serialized = _canonical_body_bytes(request_body)
        body_arg = request_body
        if signer:
            hdrs, serialized = signer.build_headers("PUT", path, dict(request_body))
            merged = _merge_signer_headers(overrides, hdrs)
        if serialized is not None:
            body_arg = None
        merged = _service_account_overrides(merged)
        _require_service_account_headers(merged)
        return super().update(
            path=path,
            request_body=body_arg,
            response_type=Domain,
            overrides=merged,
            serialized_json_body=serialized,
        )

    def destroy(
        self,
        domain_id: str,
        signer: Optional[ServiceAccountSigner] = None,
        overrides: RequestOverrides = None,
    ) -> DeleteResponse:
        path = f"/v3/admin/domains/{_encode_domain_id(domain_id)}"
        merged = overrides
        if signer:
            hdrs, _ = signer.build_headers("DELETE", path, None)
            merged = _merge_signer_headers(overrides, hdrs)
        merged = _service_account_overrides(merged)
        _require_service_account_headers(merged)
        return super().destroy(path=path, overrides=merged)

    def get_info(
        self,
        domain_id: str,
        request_body: GetDomainInfoRequest,
        signer: Optional[ServiceAccountSigner] = None,
        overrides: RequestOverrides = None,
    ) -> Response[DomainVerificationDetails]:
        """
        Return DNS record information and verification status for the given verification type.

        Args:
            domain_id: The domain ID.
            request_body: Body with ``type`` (for example ``ownership`` or ``dkim``).
            signer: Optional service account signer for ``X-Nylas-*`` headers.
            overrides: Request overrides (for example extra headers).

        Returns:
            Verification details including required DNS records.
        """
        path = f"/v3/admin/domains/{_encode_domain_id(domain_id)}/info"
        body = dict(request_body)
        merged = overrides
        serialized = _canonical_body_bytes(body)
        if signer:
            hdrs, serialized = signer.build_headers("POST", path, body)
            merged = _merge_signer_headers(overrides, hdrs)
        merged = _service_account_overrides(merged)
        _require_service_account_headers(merged)
        exec_kwargs = {"overrides": merged}
        if serialized is not None:
            exec_kwargs["serialized_json_body"] = serialized
        res, headers = self._http_client._execute(
            "POST",
            path,
            None,
            None,
            None if serialized is not None else body,
            **exec_kwargs,
        )
        return Response.from_dict(res, DomainVerificationDetails, headers)

    def verify(
        self,
        domain_id: str,
        request_body: VerifyDomainRequest,
        signer: Optional[ServiceAccountSigner] = None,
        overrides: RequestOverrides = None,
    ) -> Response[DomainVerificationDetails]:
        """
        Trigger a verification check for the specified DNS record type.

        Args:
            domain_id: The domain ID.
            request_body: Body with ``type`` of verification to run.
            signer: Optional service account signer for ``X-Nylas-*`` headers.
            overrides: Request overrides (for example extra headers).

        Returns:
            Verification attempt details and status.
        """
        path = f"/v3/admin/domains/{_encode_domain_id(domain_id)}/verify"
        body = dict(request_body)
        merged = overrides
        serialized = _canonical_body_bytes(body)
        if signer:
            hdrs, serialized = signer.build_headers("POST", path, body)
            merged = _merge_signer_headers(overrides, hdrs)
        merged = _service_account_overrides(merged)
        _require_service_account_headers(merged)
        exec_kwargs = {"overrides": merged}
        if serialized is not None:
            exec_kwargs["serialized_json_body"] = serialized
        res, headers = self._http_client._execute(
            "POST",
            path,
            None,
            None,
            None if serialized is not None else body,
            **exec_kwargs,
        )
        return Response.from_dict(res, DomainVerificationDetails, headers)

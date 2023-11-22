import sys
from typing import Union
from urllib.parse import urlparse, urlencode

import requests
from requests import Response

from nylas._client_sdk_version import __VERSION__
from nylas.models.errors import (
    NylasApiError,
    NylasApiErrorResponse,
    NylasSdkTimeoutError,
    NylasOAuthError,
    NylasOAuthErrorResponse,
    NylasApiErrorResponseData,
)


def _validate_response(response: Response) -> dict:
    json = response.json()
    if response.status_code >= 400:
        parsed_url = urlparse(response.url)
        try:
            if (
                "connect/token" in parsed_url.path
                or "connect/revoke" in parsed_url.path
            ):
                parsed_error = NylasOAuthErrorResponse.from_dict(json)
                raise NylasOAuthError(parsed_error, response.status_code)
            else:
                parsed_error = NylasApiErrorResponse.from_dict(json)
                raise NylasApiError(parsed_error, response.status_code)
        except (KeyError, TypeError):
            request_id = json.get("request_id", None)
            raise NylasApiError(
                NylasApiErrorResponse(
                    request_id,
                    NylasApiErrorResponseData(
                        type="unknown",
                        message=json,
                    ),
                ),
                status_code=response.status_code,
            )

    return json


class HttpClient(object):
    """HTTP client for the Nylas API."""

    def __init__(self, api_server, api_key, timeout):
        self.api_server = api_server
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()

    def _execute(
        self,
        method,
        path,
        headers=None,
        query_params=None,
        request_body=None,
        data=None,
    ) -> dict:
        request = self._build_request(
            method, path, headers, query_params, request_body, data
        )
        try:
            response = self.session.request(
                request["method"],
                request["url"],
                headers=request["headers"],
                json=request_body,
                timeout=self.timeout,
                data=data,
            )
        except requests.exceptions.Timeout:
            raise NylasSdkTimeoutError(url=request["url"], timeout=self.timeout)

        return _validate_response(response)

    def _execute_download_request(
        self,
        path,
        headers=None,
        query_params=None,
        stream=False,
    ) -> Union[bytes, Response]:
        request = self._build_request("GET", path, headers, query_params)
        try:
            response = self.session.request(
                request["method"],
                request["url"],
                headers=request["headers"],
                timeout=self.timeout,
                stream=stream,
            )

            # If we stream an iterator for streaming the content, otherwise return the entire byte array
            if stream:
                return response
            else:
                return response.content if response.content else None
        except requests.exceptions.Timeout:
            raise NylasSdkTimeoutError(url=request["url"], timeout=self.timeout)

    def _build_request(
        self,
        method: str,
        path: str,
        headers: dict = None,
        query_params: dict = None,
        request_body=None,
        data=None,
    ) -> dict:
        url = "{}{}".format(self.api_server, path)
        if query_params:
            # Convert list of values to comma separated string first
            process_query_params = {
                k: ",".join(v) if isinstance(v, list) else v
                for k, v in query_params.items()
            }
            url = "{}?{}".format(url, urlencode(process_query_params))
        headers = self._build_headers(headers, request_body, data)

        return {
            "method": method,
            "url": url,
            "headers": headers,
        }

    def _build_headers(
        self, extra_headers: dict = None, response_body=None, data=None
    ) -> dict:
        if extra_headers is None:
            extra_headers = {}

        major, minor, revision, _, __ = sys.version_info
        user_agent_header = "Nylas Python SDK {} - {}.{}.{}".format(
            __VERSION__, major, minor, revision
        )
        headers = {
            "X-Nylas-API-Wrapper": "python",
            "User-Agent": user_agent_header,
            "Authorization": "Bearer {}".format(self.api_key),
        }
        if data is not None and data.content_type is not None:
            headers["Content-type"] = data.content_type
        elif response_body is not None:
            headers["Content-type"] = "application/json"

        return {**headers, **extra_headers}

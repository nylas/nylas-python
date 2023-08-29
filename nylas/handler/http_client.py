import sys
import urllib.parse

import requests
from requests import Response

from nylas._client_sdk_version import __VERSION__
from nylas.models.nylas_api_error_response import NylasApiErrorResponse


def _validate_response(response: Response) -> dict:
    json = response.json()
    if response.status_code >= 400:
        raise NylasApiErrorResponse(json["request_id"], json["error"])

    return json


class HttpClient(object):
    """HTTP client for the Nylas API."""

    def __init__(self, api_server, api_key, timeout):
        self.api_server = api_server
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()

    def _execute(
        self, method, path, headers=None, query_params=None, request_body=None
    ) -> dict:
        request = self._build_request(method, path, headers, query_params)
        response = self.session.request(
            request["method"],
            request["url"],
            headers=request["headers"],
            json=request_body,
        )
        # TODO::Also validate and parse response
        return _validate_response(response)

    def _build_request(
        self, method: str, path: str, headers: dict = None, query_params: dict = None
    ) -> dict:
        url = "{}{}".format(self.api_server, path)
        if query_params:
            url = "{}?{}".format(url, urllib.parse.urlencode(query_params))
        headers = self._build_headers(headers)

        return {
            "method": method,
            "url": url,
            "headers": headers,
        }

    def _build_headers(self, extra_headers: dict = None) -> dict:
        if extra_headers is None:
            extra_headers = {}

        major, minor, revision, _, __ = sys.version_info
        user_agent_header = "Nylas Python SDK {} - {}.{}.{}".format(
            __VERSION__, major, minor, revision
        )
        headers = {
            "X-Nylas-API-Wrapper": "python",
            "User-Agent": user_agent_header,
            "Content-type": "application/json",
            "Authorization": "Bearer {}".format(self.api_key),
        }

        return {**headers, **extra_headers}

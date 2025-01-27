from dataclasses import dataclass
from typing import Optional

from requests.structures import CaseInsensitiveDict
from dataclasses_json import dataclass_json


class AbstractNylasApiError(Exception):
    """
    Base class for all Nylas API errors.

    Attributes:
        request_id: The unique identifier of the request.
        status_code: The HTTP status code of the error response.
        headers: The headers returned from the API.
    """

    def __init__(
        self,
        message: str,
        request_id: Optional[str] = None,
        status_code: Optional[int] = None,
        headers: Optional[CaseInsensitiveDict] = None,
    ):
        """
        Args:
            request_id: The unique identifier of the request.
            status_code: The HTTP status code of the error response.
            message: The error message.
        """
        self.request_id: str = request_id
        self.status_code: int = status_code
        self.headers: CaseInsensitiveDict = headers
        super().__init__(message)


class AbstractNylasSdkError(Exception):
    """
    Base class for all Nylas SDK errors.
    """

    pass


@dataclass_json
@dataclass
class NylasApiErrorResponseData:
    """
    Interface representing the error data within the response object.

    Attributes:
        type: The type of error.
        message: The error message.
        provider_error: The provider error if there is one.
    """

    type: str
    message: str
    provider_error: Optional[dict] = None


@dataclass_json
@dataclass
class NylasApiErrorResponse:
    """
    Interface representing the error response from the Nylas API.

    Attributes:
        request_id: The unique identifier of the request.
        error: The error data.
    """

    request_id: str
    error: NylasApiErrorResponseData


@dataclass_json
@dataclass
class NylasOAuthErrorResponse:
    """
    Interface representing an OAuth error returned by the Nylas API.

    Attributes:
        error: Error type.
        error_code: Error code used for referencing the docs, logs, and data stream.
        error_description: Human readable error description.
        error_uri: URL to the related documentation and troubleshooting regarding this error.
    """

    error: str
    error_code: int
    error_description: str
    error_uri: str


class NylasApiError(AbstractNylasApiError):
    """
    Class representation of a general Nylas API error.

    Attributes:
        type: Error type.
        provider_error: Provider Error.
        headers: The headers returned from the API.
    """

    def __init__(
        self,
        api_error: NylasApiErrorResponse,
        status_code: Optional[int] = None,
        headers: Optional[CaseInsensitiveDict] = None,
    ):
        """
        Args:
            api_error: The error details from the API.
            status_code: The HTTP status code of the error response.
        """
        super().__init__(api_error.error.message, api_error.request_id, status_code, headers)
        self.type: str = api_error.error.type
        self.provider_error: Optional[dict] = api_error.error.provider_error
        self.headers: CaseInsensitiveDict = headers

class NylasOAuthError(AbstractNylasApiError):
    """
    Class representation of an OAuth error returned by the Nylas API.

    Attributes:
        error: Error type.
        error_code: Error code used for referencing the docs, logs, and data stream.
        error_description: Human readable error description.
        error_uri: URL to the related documentation and troubleshooting regarding this error.
    """

    def __init__(
        self,
        oauth_error: NylasOAuthErrorResponse,
        status_code: Optional[int] = None,
        headers: Optional[CaseInsensitiveDict] = None,
    ):
        """
        Args:
            oauth_error: The error details from the API.
            status_code: The HTTP status code of the error response.
        """
        super().__init__(oauth_error.error_description, None, status_code, headers)
        self.error: str = oauth_error.error
        self.error_code: int = oauth_error.error_code
        self.error_description: str = oauth_error.error_description
        self.error_uri: str = oauth_error.error_uri
        self.headers: CaseInsensitiveDict = headers

class NylasSdkTimeoutError(AbstractNylasSdkError):
    """
    Error thrown when the Nylas SDK times out before receiving a response from the server.

    Attributes:
        url: The URL that timed out.
        timeout: The timeout value set in the Nylas SDK, in seconds.
    """

    def __init__(self, url: str, timeout: int, headers: Optional[CaseInsensitiveDict] = None):
        """
        Args:
            url: The URL that timed out.
            timeout: The timeout value set in the Nylas SDK, in seconds.
        """
        super().__init__(
            "Nylas SDK timed out before receiving a response from the server."
        )
        self.url: str = url
        self.timeout: int = timeout
        self.headers: CaseInsensitiveDict = headers

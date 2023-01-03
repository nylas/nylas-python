import json

from requests import HTTPError


class NylasError(Exception):
    pass


class MessageRejectedError(NylasError):
    pass


class FileUploadError(NylasError):
    pass


class UnSyncedError(NylasError):
    """
    HTTP Code 202
    The request was valid but the resource wasn't ready. Retry the request with exponential backoff.
    """

    pass


class NylasApiError(HTTPError):
    """
    Error class for Nylas API Errors
    This class provides more information to the user sent from the server, if present
    """

    def __init__(self, response):
        try:
            response_json = json.loads(response.text)
            error_message = "%s %s. Reason: %s. Nylas Error Type: %s" % (
                response.status_code,
                response.reason,
                response_json["message"],
                response_json["type"],
            )
            super(NylasApiError, self).__init__(error_message, response=response)
        except (ValueError, KeyError):
            super(NylasApiError, self).__init__(response.text, response=response)


class RateLimitError(NylasApiError):
    """
    Error class for 429 rate limit errors
    This class provides details about the rate limit returned from the server
    """

    RATE_LIMIT_LIMIT_HEADER = "X-RateLimit-Limit"
    RATE_LIMIT_RESET_HEADER = "X-RateLimit-Reset"

    def __init__(self, response):
        try:
            self.rate_limit = int(response.headers[self.RATE_LIMIT_LIMIT_HEADER])
            self.rate_limit_reset = int(response.headers[self.RATE_LIMIT_RESET_HEADER])
            super(RateLimitError, self).__init__(response)
        except (ValueError, KeyError):
            super(RateLimitError, self).__init__(response)

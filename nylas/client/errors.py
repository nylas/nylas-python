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

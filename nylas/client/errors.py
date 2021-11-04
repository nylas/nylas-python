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
        response_json = json.loads(response.text)
        if response_json and "message" in response_json and "type" in response_json:
            error_message = u"%s %s. Reason: %s. Nylas Error Type: %s" % (
                response.status_code,
                response.reason,
                response_json["message"],
                response_json["type"],
            )
            super(NylasApiError, self).__init__(error_message, response=response)
        else:
            super(NylasApiError, self).__init__(response.text, response=response)

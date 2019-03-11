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

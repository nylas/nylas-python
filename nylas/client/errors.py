class NylasError(Exception):
    pass

class MessageRejectedError(NylasError):
    pass

class FileUploadError(NylasError):
    pass

class UnSyncedError(NylasError):
    pass

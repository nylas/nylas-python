class NylasError(Exception):
    pass

class MessageRejectedError(NylasError):
    pass

class FileUploadError(NylasError):
    pass

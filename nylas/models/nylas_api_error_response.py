from typing import NamedTuple

from nylas.models.nylas_api_error import NylasApiError


class NylasApiErrorResponse(Exception):
    """Error response object returned from the Nylas API."""

    def __int__(self, request_id: str, error_dict: dict):
        self.request_id: str = request_id
        self.error: NylasApiError = NylasApiError.from_dict(error_dict)
        super().__init__(self.error.message)

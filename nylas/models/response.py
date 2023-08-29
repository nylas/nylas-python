from dataclasses import dataclass
from typing import TypeVar, Generic

from dataclasses_json import DataClassJsonMixin, dataclass_json

T = TypeVar("T", bound=DataClassJsonMixin)


class Response(tuple, Generic[T]):
    """Response object returned from the Nylas API."""

    data: T
    request_id: str

    def __new__(cls, data: T, request_id: str):
        cls = tuple.__new__(cls, (data, request_id))
        cls.data = data
        cls.request_id = request_id
        return cls

    @classmethod
    def from_dict(cls, resp: dict, generic_type):
        return cls(
            data=generic_type.from_dict(resp["data"]),
            request_id=resp["request_id"],
        )


@dataclass_json
@dataclass
class RequestIdOnlyResponse:
    """
    Response object returned from the Nylas API that only contains a request ID.

    Attributes:
        request_id: The request ID returned from the API.
    """

    request_id: str

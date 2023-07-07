from typing import TypeVar, Generic, Type

from dataclasses_json import DataClassJsonMixin

T = TypeVar("T", bound=DataClassJsonMixin)


class Response(Generic[T]):
    """Response object returned from the Nylas API."""

    # request_id: str
    # data: T

    def __init__(self, request_id: str, data: T):
        self.request_id = request_id
        self.data = data

    @classmethod
    def from_dict(cls, resp: dict, generic_type: Type[T]):
        return cls(
            request_id=resp["request_id"],
            data=generic_type.from_dict(resp["data"]),
        )

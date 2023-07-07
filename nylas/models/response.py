from typing import NamedTuple, Dict, Any, TypeVar, Generic

T = TypeVar("T")


class Response(Generic[T]):
    """Response object returned from the Nylas API."""

    # request_id: str
    # data: T

    def __init__(self, request_id: str, data: T):
        self.request_id = request_id
        self.data = data

    @classmethod
    def from_dict(cls, resp: dict):
        return cls(
            request_id=resp["request_id"],
            data=resp["data"],
        )

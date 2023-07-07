from typing import List, Optional, TypeVar, Generic, Type

T = TypeVar("T")


class ListResponse(Generic[T]):
    """List response object returned from the Nylas API."""

    # request_id: str
    # data: List[Dict[str, Any]]
    # next_cursor: Optional[str]

    def __init__(self, request_id: str, data: List[T], next_cursor: Optional[str]):
        self.request_id = request_id
        self.data = data
        self.next_cursor = next_cursor

    @classmethod
    def from_dict(cls, resp: dict, generic_type: Type[T]):
        converted_data = []
        for item in resp["data"]:
            converted_data.append(generic_type.from_dict(item))
        return cls(
            request_id=resp["request_id"],
            data=converted_data,
            next_cursor=resp.get("next_cursor", None),
        )

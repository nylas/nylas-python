from typing import NamedTuple, Dict, Any


class Response(NamedTuple):
    """Response object returned from the Nylas API."""

    request_id: str
    data: Dict[str, Any]

    @classmethod
    def from_dict(cls, resp: dict):
        return cls(
            request_id=resp["request_id"],
            data=resp["data"],
        )

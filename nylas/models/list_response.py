from typing import NamedTuple, List, Dict, Any, Optional


class ListResponse(NamedTuple):
    """List response object returned from the Nylas API."""

    request_id: str
    data: List[Dict[str, Any]]
    next_cursor: Optional[str]

    @classmethod
    def from_dict(cls, resp: dict):
        return cls(
            request_id=resp["request_id"],
            data=resp["data"],
            next_cursor=resp.get("next_cursor", None),
        )

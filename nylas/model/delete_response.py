from typing import NamedTuple, List, Dict, Any, Optional


class DeleteResponse(NamedTuple):
    """Delete response object returned from the Nylas API."""

    request_id: str

    @classmethod
    def from_dict(cls, resp: dict):
        return cls(
            request_id=resp["request_id"],
        )

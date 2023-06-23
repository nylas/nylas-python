from typing import NamedTuple, Dict, Any, Optional


class NylasApiError(NamedTuple):
    """Error object returned from the Nylas API."""

    type: str
    message: str
    provider_error: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, resp: dict):
        return cls(
            type=resp["type"],
            message=resp["message"],
            provider_error=resp.get("provider_error", None),
        )

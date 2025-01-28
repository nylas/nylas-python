from dataclasses import dataclass
from typing import TypeVar, Generic, Optional, List

from dataclasses_json import DataClassJsonMixin

from requests.structures import CaseInsensitiveDict

T = TypeVar("T", bound=DataClassJsonMixin)


class Response(tuple, Generic[T]):
    """
    Response object returned from the Nylas API.

    Attributes:
        data: The requested data object.
        request_id: The request ID.
    """

    data: T
    request_id: str
    headers: Optional[CaseInsensitiveDict] = None

    def __new__(cls, data: T, request_id: str, headers: Optional[CaseInsensitiveDict] = None):
        """
        Initialize the response object.

        Args:
            data: The requested data object.
            request_id: The request ID.
            headers: The headers returned from the API.
        """
        # Initialize the tuple for destructuring support
        instance = super().__new__(cls, (data, request_id, headers))

        instance.data = data
        instance.request_id = request_id
        instance.headers = headers

        return instance

    @classmethod
    def from_dict(cls, resp: dict, generic_type, headers: Optional[CaseInsensitiveDict] = None):
        """
        Convert a dictionary to a response object.

        Args:
            resp: The dictionary to convert.
            generic_type: The type to deserialize the data object into.
            headers: The headers returned from the API.
        """

        return cls(
            data=generic_type.from_dict(resp["data"]),
            request_id=resp["request_id"],
            headers=headers,
        )


class ListResponse(tuple, Generic[T]):
    """
    List response object returned from the Nylas API.

    Attributes:
        data: The list of requested data objects.
        request_id: The request ID.
        next_cursor: The cursor to use to get the next page of data.
        headers: The headers returned from the API.
    """

    data: List[T]
    request_id: str
    next_cursor: Optional[str] = None
    headers: Optional[CaseInsensitiveDict] = None

    def __new__(
        cls,
        data: List[T],
        request_id: str,
        next_cursor: Optional[str] = None,
        headers: Optional[CaseInsensitiveDict] = None
    ):
        """
        Initialize the response object.

        Args:
            data: The list of requested data objects.
            request_id: The request ID.
            next_cursor: The cursor to use to get the next page of data.
            headers: The headers returned from the API.
        """
        # Initialize the tuple for destructuring support
        instance = super().__new__(cls, (data, request_id, next_cursor, headers))

        instance.data = data
        instance.request_id = request_id
        instance.next_cursor = next_cursor
        instance.headers = headers

        return instance

    @classmethod
    def from_dict(cls, resp: dict, generic_type, headers: Optional[CaseInsensitiveDict] = None):
        """
        Convert a dictionary to a response object.

        Args:
            resp: The dictionary to convert.
            generic_type: The type to deserialize the data objects into.
            headers: The headers returned from the API.
        """

        converted_data = []
        for item in resp["data"]:
            converted_data.append(generic_type.from_dict(item, infer_missing=True))

        return cls(
            data=converted_data,
            request_id=resp["request_id"],
            next_cursor=resp.get("next_cursor", None),
            headers=headers,
        )


@dataclass
class DeleteResponse:
    """
    Delete response object returned from the Nylas API.

    Attributes:
        request_id: The request ID returned from the API.
        headers: The headers returned from the API.
    """

    request_id: str
    headers: Optional[CaseInsensitiveDict] = None

    @classmethod
    def from_dict(cls, resp: dict, headers: Optional[CaseInsensitiveDict] = None):
        """
        Convert a dictionary to a response object.

        Args:
            resp: The dictionary to convert.
            headers: The headers returned from the API.
        """
        return cls(request_id=resp["request_id"], headers=headers)


@dataclass
class RequestIdOnlyResponse:
    """
    Response object returned from the Nylas API that only contains a request ID.

    Attributes:
        request_id: The request ID returned from the API.
        headers: The headers returned from the API.
    """

    request_id: str
    headers: Optional[CaseInsensitiveDict] = None

    @classmethod
    def from_dict(cls, resp: dict, headers: Optional[CaseInsensitiveDict] = None):
        """
        Convert a dictionary to a response object.

        Args:
            resp: The dictionary to convert.
            headers: The headers returned from the API.
        """
        return cls(request_id=resp["request_id"], headers=headers)

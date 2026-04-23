from dataclasses import dataclass
from typing import List as TypingList, Literal, Optional

from dataclasses_json import dataclass_json
from typing_extensions import NotRequired, TypedDict

from nylas.models.list_query_params import ListQueryParams

ListType = Literal["domain", "tld", "address"]


class ListListsQueryParams(ListQueryParams):
    """Query parameters for listing lists."""

    pass


class ListListItemsQueryParams(ListQueryParams):
    """Query parameters for listing items in a list."""

    pass


class CreateListRequest(TypedDict):
    """Request body for creating a list."""

    name: str
    type: ListType
    description: NotRequired[str]


class UpdateListRequest(TypedDict, total=False):
    """Request body for updating a list."""

    name: NotRequired[str]
    description: NotRequired[str]


class UpdateListItemsRequest(TypedDict):
    """Request body for adding/removing list items."""

    items: TypingList[str]


@dataclass_json
@dataclass
class NylasList:
    """A typed collection used in `in_list` rule conditions."""

    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    items_count: Optional[int] = None
    application_id: Optional[str] = None
    organization_id: Optional[str] = None
    created_at: Optional[int] = None
    updated_at: Optional[int] = None


@dataclass_json
@dataclass
class ListItem:
    """A single value belonging to a Nylas list."""

    id: Optional[str] = None
    list_id: Optional[str] = None
    value: Optional[str] = None
    created_at: Optional[int] = None

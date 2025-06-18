from dataclasses import dataclass
from typing import Optional

from dataclasses_json import dataclass_json
from typing_extensions import TypedDict, NotRequired

from nylas.models.list_query_params import ListQueryParams


@dataclass_json
@dataclass
class Folder:
    """
    Class representing a Nylas folder.

    Attributes:
        id: A globally unique object identifier.
        grant_id: A Grant ID of the Nylas account.
        name: Folder name
        object: The type of object.
        parent_id: ID of the parent folder. (Microsoft only)
        background_color: Folder background color. (Google only)
        text_color: Folder text color. (Google only)
        system_folder: Indicates if the folder is user created or system created. (Google Only)
        child_count: The number of immediate child folders in the current folder. (Microsoft only)
        unread_count: The number of unread items inside of a folder.
        total_count: The number of items inside of a folder.
        attributes: Common attribute descriptors shared by system folders across providers.
            For example, Sent email folders have the `["\\Sent"]` attribute.
            For IMAP grants, IMAP providers provide the attributes.
            For Google and Microsoft Graph, Nylas matches system folders to a set of common attributes.
    """

    id: str
    grant_id: str
    name: str
    object: str = "folder"
    parent_id: Optional[str] = None
    background_color: Optional[str] = None
    text_color: Optional[str] = None
    system_folder: Optional[bool] = None
    child_count: Optional[int] = None
    unread_count: Optional[int] = None
    total_count: Optional[int] = None
    attributes: Optional[str] = None


class CreateFolderRequest(TypedDict):
    """
    Class representation of the Nylas folder creation request.

    Attributes:
        name: The name of the folder.
        parent_id: The parent ID of the folder. (Microsoft only)
        background_color: The background color of the folder. (Google only)
        text_color: The text color of the folder. (Google only)
    """

    name: str
    parent_id: NotRequired[str]
    background_color: NotRequired[str]
    text_color: NotRequired[str]


class UpdateFolderRequest(TypedDict):
    """
    Class representation of the Nylas folder update request.

    Attributes:
        name: The name of the folder.
        parent_id: The parent ID of the folder. (Microsoft only)
        background_color: The background color of the folder. (Google only)
        text_color: The text color of the folder. (Google only)
    """

    name: NotRequired[str]
    parent_id: NotRequired[str]
    background_color: NotRequired[str]
    text_color: NotRequired[str]


class ListFolderQueryParams(ListQueryParams):
    """
    Interface representing the query parameters for listing folders.

    Attributes:
        parent_id: (Microsoft and EWS only.) Use the ID of a folder to find all child folders it contains.
        include_hidden_folders: (Microsoft only) When true, Nylas includes hidden folders in its response.
        single_level: (Microsoft only) If true, retrieves folders from a single-level hierarchy only.
            If false, retrieves folders across a multi-level hierarchy. Defaults to false.
        select (NotRequired[str]): Comma-separated list of fields to return in the response.
            This allows you to receive only the portion of object data that you're interested in.
        limit (NotRequired[int]): The maximum number of objects to return.
            This field defaults to 50. The maximum allowed value is 200.
        page_token (NotRequired[str]): An identifier that specifies which page of data to return.
            This value should be taken from a ListResponse object's next_cursor parameter.
    """

    parent_id: NotRequired[str]
    include_hidden_folders: NotRequired[bool]
    single_level: NotRequired[bool]


class FindFolderQueryParams(TypedDict):
    """
    Interface representing the query parameters for finding a folder.

    Attributes:
        select: Comma-separated list of fields to return in the response.
            This allows you to receive only the portion of object data that you're interested in.
    """

    select: NotRequired[str]

from dataclasses import dataclass
from typing import Optional

from dataclasses_json import dataclass_json
from typing_extensions import TypedDict, NotRequired


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


class CreateFolderRequest(TypedDict):
    """
    Class representation of the Nylas folder creation request.

    Attributes:
        name: The name of the folder.
        parent_id: The parent ID of the folder. (Microsoft only)
        background_color: The background color of the folder. (Google only)
        tex_color: The text color of the folder. (Google only)
    """

    name: str
    parent_id: NotRequired[str]
    background_color: NotRequired[str]
    tex_color: NotRequired[str]


class UpdateFolderRequest(TypedDict):
    """
    Class representation of the Nylas folder update request.

    Attributes:
        name: The name of the folder.
        parent_id: The parent ID of the folder. (Microsoft only)
        background_color: The background color of the folder. (Google only)
        tex_color: The text color of the folder. (Google only)
    """

    name: NotRequired[str]
    parent_id: NotRequired[str]
    background_color: NotRequired[str]
    tex_color: NotRequired[str]

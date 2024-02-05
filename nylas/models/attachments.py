from dataclasses import dataclass
from typing import Optional, Union, BinaryIO

from dataclasses_json import dataclass_json
from typing_extensions import TypedDict, NotRequired


@dataclass_json
@dataclass
class Attachment:
    """
    An attachment on a message.

    Attributes:
        id: Globally unique object identifier.
        grant_id: The grant ID of the attachment.
        size: Size of the attachment in bytes.
        filename: Name of the attachment.
        content_type: MIME type of the attachment.
        content_id: The content ID of the attachment.
        content_disposition: The content disposition of the attachment.
        is_inline: Whether the attachment is inline.
    """

    id: str
    grant_id: Optional[str] = None
    filename: Optional[str] = None
    content_type: Optional[str] = None
    size: Optional[int] = None
    content_id: Optional[str] = None
    content_disposition: Optional[str] = None
    is_inline: Optional[bool] = None


class CreateAttachmentRequest(TypedDict):
    """
    A request to create an attachment.

    You can use `attach_file_request_builder()` to build this request.

    Attributes:
        filename: Name of the attachment.
        content_type: MIME type of the attachment.
        content: Either a Base64 encoded content of the attachment or a pointer to a file.
        size: Size of the attachment in bytes.
        content_id: The content ID of the attachment.
        content_disposition: The content disposition of the attachment.
        is_inline: Whether the attachment is inline.
    """

    filename: str
    content_type: str
    content: Union[str, BinaryIO]
    size: int
    content_id: NotRequired[str]
    content_disposition: NotRequired[str]
    is_inline: NotRequired[bool]


class FindAttachmentQueryParams(TypedDict):
    """
    Interface of the query parameters for finding an attachment.

    Attributes:
        message_id: Message ID to find the attachment in.
    """

    message_id: str

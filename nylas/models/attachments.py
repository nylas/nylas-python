from dataclasses import dataclass
from typing import Optional

from dataclasses_json import dataclass_json
from typing_extensions import TypedDict, NotRequired


@dataclass_json
@dataclass
class Attachment:
    """
    An attachment on a message.

    Attributes:
        id: Globally unique object identifier.
        size: Size of the attachment in bytes.
        filename: Name of the attachment.
        content_type: MIME type of the attachment.
    """

    id: str
    size: int
    filename: Optional[str] = None
    content_type: Optional[str] = None


class CreateAttachmentRequest(TypedDict):
    """
    A request to create an attachment.

    Attributes:
        filename: Name of the attachment.
        content_type: MIME type of the attachment.
        content: Base64 encoded content of the attachment.
        size: Size of the attachment in bytes.
        content_id: The content ID of the attachment.
        content_disposition: The content disposition of the attachment.
        is_inline: Whether the attachment is inline.
    """

    filename: str
    content_type: str
    content: str
    size: int
    content_id: NotRequired[str]
    content_disposition: NotRequired[str]
    is_inline: NotRequired[bool]

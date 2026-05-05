from dataclasses import dataclass
from typing import Optional, Union, BinaryIO, Dict

from dataclasses_json import dataclass_json
from typing_extensions import TypedDict, NotRequired, Literal


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

    id: Optional[str] = None
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


AttachmentUploadSessionStatusType = Literal["uploading", "ready", "failed", "expired"]


class CreateAttachmentUploadSessionRequest(TypedDict):
    """
    Request body for creating a large-attachment upload session (Graph only).

    Attributes:
        filename: The name of the file as it will appear in the email.
        content_type: MIME type of the file (e.g. 'application/pdf').
        size: Expected file size in bytes (max 157286400 / 150 MB). Recommended —
              Nylas validates the upload matches this size at completion.
    """

    filename: str
    content_type: str
    size: NotRequired[int]


@dataclass_json
@dataclass
class AttachmentUploadSession:
    """
    Upload session returned when creating a large-attachment upload session.

    Attributes:
        attachment_id: Unique session ID — use when completing the session and when
                       referencing the attachment in send/draft.
        method: HTTP method to use when uploading to `url`. Always 'PUT'.
        url: Pre-signed URL to upload file bytes (no Nylas auth header needed).
        headers: Headers to include when uploading to `url`.
        expires_at: When the session expires (RFC 3339).
        max_size: Maximum allowed file size in bytes (157286400).
        size: Expected file size echoing the request; 0 if `size` was omitted.
        content_type: MIME type of the file.
        filename: Name of the file.
        grant_id: Grant ID the session belongs to.
    """

    attachment_id: Optional[str] = None
    method: Optional[str] = None
    url: Optional[str] = None
    headers: Optional[Dict[str, str]] = None
    expires_at: Optional[str] = None
    max_size: Optional[int] = None
    size: Optional[int] = None
    content_type: Optional[str] = None
    filename: Optional[str] = None
    grant_id: Optional[str] = None


@dataclass_json
@dataclass
class AttachmentUploadSessionComplete:
    """
    Result of completing a large-attachment upload session.

    Attributes:
        attachment_id: The session ID.
        grant_id: Grant ID the session belongs to.
        status: Upload status; typically 'ready' after successful completion.
    """

    attachment_id: Optional[str] = None
    grant_id: Optional[str] = None
    status: Optional[str] = None

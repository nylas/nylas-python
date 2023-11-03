from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from typing import List, Literal, Optional, Dict, Any
from typing_extensions import TypedDict, NotRequired, get_type_hints
from datetime import datetime

from nylas.models.attachments import Attachment
from nylas.models.list_query_params import ListQueryParams
from nylas.models.events import EmailName


Fields = Literal["standard", "include_headers"]
""" Literal representing which headers to include with a message. """


@dataclass_json
@dataclass
class MessageHeader:
    """
    A message header.

    Attributes:
        name: The header name.
        value: The header value.
    """

    name: str
    value: str


@dataclass_json
@dataclass
class Message:
    """
    A Message object.

    Attributes:
        id: Globally unique object identifier.
        grant_id: The grant that this message belongs to.
        thread_id: The thread that this message belongs to.
        subject: The subject of the message.
        from_: The sender of the message.
        object: The type of object.
        to: The recipients of the message.
        cc: The CC recipients of the message.
        bcc: The BCC recipients of the message.
        reply_to: The reply-to recipients of the message.
        date: The date the message was received.
        unread: Whether the message is unread.
        starred: Whether the message is starred.
        snippet: A snippet of the message body.
        body: The body of the message.
        attachments: The attachments on the message.
        folders: The folders that the message is in.
        headers: The headers of the message.
        created_at: Unix timestamp of when the message was created.
    """

    id: str
    grant_id: str
    from_: List[EmailName] = field(metadata=config(field_name="from"))
    date: datetime
    object: str = "messages"
    body: Optional[str] = None
    thread_id: Optional[str] = None
    subject: Optional[str] = None
    snippet: Optional[str] = None
    to: Optional[List[EmailName]] = None
    bcc: Optional[List[EmailName]] = None
    cc: Optional[List[EmailName]] = None
    reply_to: Optional[List[EmailName]] = None
    attachments: Optional[List[Attachment]] = None
    folders: Optional[List[str]] = None
    headers: Optional[List[MessageHeader]] = None
    unread: Optional[bool] = None
    starred: Optional[bool] = None
    created_at: Optional[int] = None


# Need to use Functional typed dicts because "from" and "in" are Python
# keywords, and can't be declared using the declarative syntax
ListMessagesQueryParams = TypedDict(
    "ListMessagesQueryParams",
    {
        **get_type_hints(ListQueryParams),  # Inherit fields from ListQueryParams
        "subject": NotRequired[str],
        "any_email": NotRequired[List[str]],
        "from": NotRequired[List[str]],
        "to": NotRequired[List[str]],
        "cc": NotRequired[List[str]],
        "bcc": NotRequired[List[str]],
        "in": NotRequired[List[str]],
        "unread": NotRequired[bool],
        "starred": NotRequired[bool],
        "thread_id": NotRequired[str],
        "received_before": NotRequired[int],
        "received_after": NotRequired[int],
        "has_attachment": NotRequired[bool],
        "fields": NotRequired[Fields],
        "search_query_native": NotRequired[str],
    },
)
"""
Query parameters for listing messages.

Attributes:
    subject: Return messages with matching subject.
    any_email: Return messages that have been sent or received by this comma-separated list of email addresses.
    from: Return messages sent from this email address.
    to: Return messages sent to this email address.
    cc: Return messages cc'd to this email address.
    bcc: Return messages bcc'd to this email address.
    in: Return messages in this specific folder or label, specified by ID.
    unread: Filter messages by unread status.
    starred: Filter messages by starred status.
    thread_id: Filter messages by thread_id.
    received_before: Return messages with received dates before received_before.
    received_after: Return messages with received dates after received_after.
    has_attachment: Filter messages by whether they have an attachment.
    fields: Specify "include_headers" to include headers in the response. "standard" is the default.
    search_query_native: A native provider search query for Google or Microsoft.
    limit (NotRequired[int]): The maximum number of objects to return.
        This field defaults to 50. The maximum allowed value is 200.
    page_token (NotRequired[str]): An identifier that specifies which page of data to return.
        This value should be taken from a ListResponse object's next_cursor parameter.
"""


class FindMessageQueryParams(TypedDict):

    """
    Query parameters for finding a message.

    Attributes:
        fields: Specify "include_headers" to include headers in the response. "standard" is the default.
    """

    fields: NotRequired[Fields]


class UpdateMessageRequest(TypedDict):

    """
    Request payload for updating a message.

    Attributes:
        starred: The message's starred status
        unread: The message's unread status
        folder: The message's folders
        metadata: A list of key-value pairs storing additional data
    """

    unread: NotRequired[bool]
    starred: NotRequired[bool]
    folder: NotRequired[List[str]]
    metadata: NotRequired[Dict[str, Any]]


@dataclass_json
@dataclass
class ScheduledMessageStatus:
    """
    The status of a scheduled message.

    Attributes:
        code: The status code the describes the state of the scheduled message.
        description: A description of the status of the scheduled message.
    """

    code: str
    description: str


@dataclass_json
@dataclass
class ScheduledMessage:
    """
    A scheduled message.

    Attributes:
        schedule_id: The unique identifier for the scheduled message.
        status: The status of the scheduled message.
        close_time: The time the message was sent or failed to send, in epoch time.
    """

    schedule_id: int
    status: ScheduledMessageStatus
    close_time: Optional[int] = None


@dataclass_json
@dataclass
class ScheduledMessagesList:
    """
    A list of scheduled messages.

    Attributes:
        schedules: The list of scheduled messages.
    """

    schedules: List[ScheduledMessage]


@dataclass_json
@dataclass
class StopScheduledMessageResponse:
    """
    The response from stopping a scheduled message.

    Attributes:
        message: A message describing the result of the request.
    """

    message: str

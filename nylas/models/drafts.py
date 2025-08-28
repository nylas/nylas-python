from dataclasses import dataclass
from typing import List, Dict, Any, get_type_hints

from dataclasses_json import dataclass_json
from typing_extensions import TypedDict, NotRequired

from nylas.models.attachments import CreateAttachmentRequest
from nylas.models.events import EmailName
from nylas.models.list_query_params import ListQueryParams
from nylas.models.messages import Message


@dataclass_json
@dataclass
class Draft(Message):
    """
    A Draft object.

    Attributes:
        id (str): Globally unique object identifier.
        grant_id (str): The grant that this message belongs to.
        from_ (List[EmailName]): The sender of the message.
        date (int): The date the message was received.
        object: The type of object.
        thread_id (Optional[str]): The thread that this message belongs to.
        subject (Optional[str]): The subject of the message.
        to (Optional[List[EmailName]]): The recipients of the message.
        cc (Optional[List[EmailName]]): The CC recipients of the message.
        bcc (Optional[List[EmailName]]): The BCC recipients of the message.
        reply_to (Optional[List[EmailName]]): The reply-to recipients of the message.
        unread (Optional[bool]): Whether the message is unread.
        starred (Optional[bool]): Whether the message is starred.
        snippet (Optional[str]): A snippet of the message body.
        body (Optional[str]): The body of the message.
        attachments (Optional[List[Attachment]]): The attachments on the message.
        folders (Optional[List[str]]): The folders that the message is in.
        created_at (Optional[int]): Unix timestamp of when the message was created.
    """

    object: str = "draft"


class TrackingOptions(TypedDict):
    """
    The different tracking options for when a message is sent.

    Attributes:
        label: The label to apply to tracked messages.
        links: Whether to track links.
        opens: Whether to track opens.
        thread_replies: Whether to track thread replies.
    """

    label: NotRequired[str]
    links: NotRequired[bool]
    opens: NotRequired[bool]
    thread_replies: NotRequired[bool]


class CustomHeader(TypedDict):
    """
    A key-value pair representing a header that can be added to drafts and outgoing messages.

    Attributes:
        name: The name of the custom header.
        value: The value of the custom header.
    """

    name: str
    value: str


class CreateDraftRequest(TypedDict):
    """
    A request to create a draft.

    Attributes:
        subject: The subject of the message.
        to: The recipients of the message.
        cc: The CC recipients of the message.
        bcc: The BCC recipients of the message.
        reply_to: The reply-to recipients of the message.
        starred: Whether the message is starred.
        body: The body of the message.
        attachments: The attachments on the message.
        send_at: Unix timestamp to send the message at.
        reply_to_message_id: The ID of the message that you are replying to.
        tracking_options: Options for tracking opens, links, and thread replies.
        custom_headers: Custom headers to add to the message.
        metadata: A dictionary of key-value pairs storing additional data.
        is_plaintext: When true, the message body is sent as plain text and the MIME data doesn't include 
            the HTML version of the message. When false, the message body is sent as HTML.
    """

    body: NotRequired[str]
    subject: NotRequired[str]
    to: NotRequired[List[EmailName]]
    bcc: NotRequired[List[EmailName]]
    cc: NotRequired[List[EmailName]]
    reply_to: NotRequired[List[EmailName]]
    attachments: NotRequired[List[CreateAttachmentRequest]]
    starred: NotRequired[bool]
    send_at: NotRequired[int]
    reply_to_message_id: NotRequired[str]
    tracking_options: NotRequired[TrackingOptions]
    custom_headers: NotRequired[List[CustomHeader]]
    metadata: NotRequired[Dict[str, Any]]
    is_plaintext: NotRequired[bool]


UpdateDraftRequest = CreateDraftRequest
""" A request to update a draft. """


# Need to use Functional typed dicts because "from" and "in" are Python
# keywords, and can't be declared using the declarative syntax
ListDraftsQueryParams = TypedDict(
    "ListDraftsQueryParams",
    {
        **get_type_hints(ListQueryParams),
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
        "has_attachment": NotRequired[bool],
    },
)
"""
Query parameters for listing drafts.

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
    has_attachment: Filter messages by whether they have an attachment.
    limit (NotRequired[int]): The maximum number of objects to return.
        This field defaults to 50. The maximum allowed value is 200.
    page_token (NotRequired[str]): An identifier that specifies which page of data to return.
        This value should be taken from a ListResponse object's next_cursor parameter.
"""


class FindDraftQueryParams(TypedDict):
    """
    Query parameters for finding a draft.

    Attributes:
        select: Comma-separated list of fields to return in the response.
            This allows you to receive only the portion of object data that you're interested in.
    """

    select: NotRequired[str]


class SendMessageRequest(CreateDraftRequest):
    """
    A request to send a message.

    Attributes:
        subject (NotRequired[str]): The subject of the message.
        to (NotRequired[List[EmailName]]): The recipients of the message.
        cc (NotRequired[List[EmailName]]): The CC recipients of the message.
        bcc (NotRequired[List[EmailName]]): The BCC recipients of the message.
        reply_to (NotRequired[List[EmailName]]): The reply-to recipients of the message.
        starred (NotRequired[bool]): Whether the message is starred.
        body (NotRequired[str]): The body of the message.
        attachments (NotRequired[List[CreateAttachmentRequest]]): The attachments on the message.
        send_at (NotRequired[int]): Unix timestamp to send the message at.
        reply_to_message_id (NotRequired[str]): The ID of the message that you are replying to.
        tracking_options (NotRequired[TrackingOptions]): Options for tracking opens, links, and thread replies.
        custom_headers(NotRequired[List[CustomHeader]]): Custom headers to add to the message.
        is_plaintext (NotRequired[bool]): When true, the message body is sent as plain text and the MIME data 
            doesn't include the HTML version of the message. When false, the message body is sent as HTML.
        from_: The sender of the message.
        use_draft: Whether or not to use draft support. This is primarily used when dealing with large attachments.
    """

    from_: NotRequired[List[EmailName]]
    use_draft: NotRequired[bool]

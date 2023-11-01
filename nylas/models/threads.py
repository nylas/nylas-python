from dataclasses import dataclass
from typing import List, Optional, TypedDict, NotRequired, get_type_hints

from dataclasses_json import dataclass_json
from nylas.models.events import EmailName
from nylas.models.list_query_params import ListQueryParams

from nylas.models.messages import Message


@dataclass_json
@dataclass
class Thread:
    """
    A Thread object.

    Attributes:
        id: Globally unique object identifier.
        grant_id: The grant that this thread belongs to.
        latest_draft_or_message: The latest draft or message in the thread.
        has_attachment: Whether the thread has an attachment.
        has_drafts: Whether the thread has drafts.
        starred: A boolean indicating whether the thread is starred or not
        unread: A boolean indicating whether the thread is read or not.
        earliest_message_date: Unix timestamp of the earliest or first message in the thread.
        latest_message_received_date: Unix timestamp of the most recent message received in the thread.
        latest_message_sent_date: Unix timestamp of the most recent message sent in the thread.
        participant: An array of participants in the thread.
        message_ids: An array of message IDs in the thread.
        draft_ids: An array of draft IDs in the thread.
        folders: An array of folder IDs the thread appears in.
        object: The type of object.
        snippet: A short snippet of the last received message/draft body.
                This is the first 100 characters of the message body, with any HTML tags removed.
        subject: The subject of the thread.
    """

    id: str
    grant_id: str
    latest_draft_or_message: Message
    has_attachment: bool
    has_drafts: bool
    starred: bool
    unread: bool
    earliest_message_date: int
    latest_message_received_date: int
    latest_message_sent_date: int
    participant: List[EmailName]
    message_ids: List[str]
    draft_ids: List[str]
    folders: List[str]
    object: str = "thread"
    snippet: Optional[str] = None
    subject: Optional[str] = None


class UpdateThreadRequest(TypedDict):
    """
    A request to update a thread.

    Attributes:
        starred: Sets all messages in the thread as starred or unstarred.
        unread: Sets all messages in the thread as read or unread.
        folder: The IDs of the folders to apply, overwriting all previous folders for all messages in the thread.
    """

    starred: NotRequired[bool]
    unread: NotRequired[bool]
    folder: NotRequired[str]


# Need to use Functional typed dicts because "from" and "in" are Python
# keywords, and can't be declared using the declarative syntax
ListThreadsQueryParams = TypedDict(
    "ListThreadsQueryParams",
    {
        **get_type_hints(ListQueryParams),  # Inherit fields from ListQueryParams
        "subject": NotRequired[str],
        "any_email": NotRequired[str],
        "from": NotRequired[str],
        "to": NotRequired[str],
        "cc": NotRequired[str],
        "bcc": NotRequired[str],
        "in": NotRequired[str],
        "unread": NotRequired[bool],
        "starred": NotRequired[bool],
        "thread_id": NotRequired[str],
        "latest_message_before": NotRequired[int],
        "latest_message_after": NotRequired[int],
        "has_attachment": NotRequired[bool],
        "search_query_native": NotRequired[str],
    },
)
"""
Query parameters for listing threads.

Attributes:
    subject: Return threads with matching subject.
    any_email: Return threads that have been sent or received by this comma-separated list of email addresses.
    from: Return threads sent from this email address.
    to: Return threads sent to this email address.
    cc: Return threads cc'd to this email address.
    bcc: Return threads bcc'd to this email address.
    in: Return threads in this specific folder or label, specified by ID.
    unread: Filter threads by unread status.
    starred: Filter threads by starred status.
    thread_id: Filter threads by thread_id.
    latest_message_before: Return threads whose most recent message was received before this Unix timestamp.
    latest_message_after: Return threads whose most recent message was received after this Unix timestamp.
    has_attachment: Filter threads by whether they have an attachment.
    search_query_native: A native provider search query for Google or Microsoft.
    limit (NotRequired[int]): The maximum number of objects to return.
        This field defaults to 50. The maximum allowed value is 200.
    page_token (NotRequired[str]): An identifier that specifies which page of data to return.
        This value should be taken from a ListResponse object's next_cursor parameter.
"""

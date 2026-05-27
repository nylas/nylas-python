from typing import Any, Dict, List

from typing_extensions import NotRequired, Required, TypedDict

from nylas.models.attachments import CreateAttachmentRequest
from nylas.models.drafts import CustomHeader, TrackingOptions
from nylas.models.events import EmailName


class TransactionalTemplate(TypedDict, total=False):
    """
    Template selection for a transactional send request.

    Attributes:
        id: The template ID.
        strict: When true, Nylas returns an error if the template contains undefined variables.
        variables: Key/value pairs substituted into the template.
    """

    id: Required[str]
    strict: NotRequired[bool]
    variables: NotRequired[Dict[str, Any]]


class TransactionalSendMessageRequest(TypedDict, total=False):
    """
    Request body for POST /v3/domains/{domain_name}/messages/send.

    Use ``from_`` for the sender; it is serialized as JSON ``from`` (``from`` is a Python keyword).

    Attributes:
        to: Recipients (required by the API).
        from_: Sender ``email`` / optional ``name`` (required by the API).
        subject: Subject line.
        body: HTML or plain body depending on ``is_plaintext``.
        cc: CC recipients.
        bcc: BCC recipients.
        reply_to: Reply-To recipients.
        attachments: File attachments.
        send_at: Unix timestamp to send the message later.
        reply_to_message_id: Message being replied to.
        tracking_options: Open/link tracking settings.
        custom_headers: Custom MIME headers.
        metadata: String-keyed metadata.
        is_plaintext: Send body as plain text when true.
        template: Application template to render (optional vs. body/subject).
    """

    to: Required[List[EmailName]]
    from_: Required[EmailName]
    subject: NotRequired[str]
    body: NotRequired[str]
    cc: NotRequired[List[EmailName]]
    bcc: NotRequired[List[EmailName]]
    reply_to: NotRequired[List[EmailName]]
    attachments: NotRequired[List[CreateAttachmentRequest]]
    send_at: NotRequired[int]
    reply_to_message_id: NotRequired[str]
    tracking_options: NotRequired[TrackingOptions]
    custom_headers: NotRequired[List[CustomHeader]]
    metadata: NotRequired[Dict[str, Any]]
    is_plaintext: NotRequired[bool]
    template: NotRequired[TransactionalTemplate]

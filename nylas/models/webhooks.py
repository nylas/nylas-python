from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Literal

from dataclasses_json import dataclass_json
from typing_extensions import TypedDict, NotRequired

WebhookStatus = Literal["active", "failing", "failed", "pause"]


class WebhookTriggers(str, Enum):
    CALENDAR_CREATED = "calendar.created"
    CALENDAR_UPDATED = "calendar.updated"
    CALENDAR_DELETED = "calendar.deleted"
    EVENT_CREATED = "event.created"
    EVENT_UPDATED = "event.updated"
    EVENT_DELETED = "event.deleted"
    GRANT_CREATED = "grant.created"
    GRANT_UPDATED = "grant.updated"
    GRANT_DELETED = "grant.deleted"
    GRANT_EXPIRED = "grant.expired"
    MESSAGE_SEND_SUCCESS = "message.send_success"
    MESSAGE_SEND_FAILED = "message.send_failed"


@dataclass_json
@dataclass
class Webhook:
    id: str
    trigger_types: List[WebhookTriggers]
    callback_url: str
    status: WebhookStatus
    notification_email_address: str
    status_updated_at: int
    created_at: int
    updated_at: int
    description: Optional[str] = None


class WebhookWithSecret(Webhook):
    webhook_secret: str


@dataclass_json
@dataclass
class WebhookDeleteData:
    status: str


@dataclass_json
@dataclass
class WebhookDeleteResponse:
    requestId: str
    data: Optional[WebhookDeleteData] = None


@dataclass_json
@dataclass
class WebhookIpAddressesResponse:
    ip_addresses: List[str]
    updated_at: int


class CreateWebhookRequest(TypedDict):
    """
    Class representation of a Nylas create webhook request.

    Attributes:
        trigger_types: List of events that triggers the webhook.
        callback_url: The url to send webhooks to.
        description: A human-readable description of the webhook destination.
        notification_email_address: The email addresses that Nylas notifies when a webhook is down for a while.
    """

    trigger_types: List[WebhookTriggers]
    callback_url: str
    description: NotRequired[str]
    notification_email_address: NotRequired[str]


class UpdateWebhookRequest(TypedDict):
    """
    Class representation of a Nylas update webhook request.

    Attributes:
        trigger_types: List of events that triggers the webhook.
        callback_url: The url to send webhooks to.
        description: A human-readable description of the webhook destination.
        notification_email_address: The email addresses that Nylas notifies when a webhook is down for a while.
    """

    trigger_types: NotRequired[List[WebhookTriggers]]
    callback_url: NotRequired[str]
    description: NotRequired[str]
    notification_email_address: NotRequired[str]

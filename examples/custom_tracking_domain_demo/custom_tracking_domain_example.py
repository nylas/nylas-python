#!/usr/bin/env python3
"""Use an organization-owned custom hostname for email tracking.

Choose one operation with ``NYLAS_CUSTOM_TRACKING_OPERATION``:
``regular``, ``draft``, ``scheduled``, or ``transactional``.
"""

import os
import sys
from typing import Optional

from nylas import Client
from nylas.models.drafts import (
    CreateDraftRequest,
    SendMessageRequest,
    TrackingOptions,
)
from nylas.models.transactional_send import TransactionalSendMessageRequest


SUPPORTED_OPERATIONS = {"regular", "draft", "scheduled", "transactional"}


def get_env_or_exit(name: str) -> str:
    """Return a required environment variable or exit."""
    value = os.getenv(name)
    if not value:
        print(f"Error: {name} environment variable is required")
        sys.exit(1)
    return value


def build_tracking_options(tracking_hostname: str) -> TrackingOptions:
    """Enable link and open tracking on the selected custom hostname."""
    return {
        "links": True,
        "opens": True,
        "domain_name": tracking_hostname,
    }


def send_regular_message(
    client: Client, grant_id: str, recipient: str, tracking_hostname: str
) -> None:
    """Send a grant-based message immediately."""
    request_body: SendMessageRequest = {
        "subject": "Tracked update",
        "to": [{"email": recipient}],
        "body": '<a href="https://example.com">Open example</a>',
        "tracking_options": build_tracking_options(tracking_hostname),
    }
    response = client.messages.send(identifier=grant_id, request_body=request_body)
    print(f"Sent message: {response.data.id}")


def create_tracked_draft(
    client: Client, grant_id: str, recipient: str, tracking_hostname: str
) -> None:
    """Create a draft that uses the custom tracking hostname."""
    request_body: CreateDraftRequest = {
        "subject": "Tracked draft",
        "to": [{"email": recipient}],
        "body": '<a href="https://example.com">Open example</a>',
        "tracking_options": build_tracking_options(tracking_hostname),
    }
    response = client.drafts.create(identifier=grant_id, request_body=request_body)
    print(f"Created draft: {response.data.id}")


def schedule_tracked_message(
    client: Client,
    grant_id: str,
    recipient: str,
    tracking_hostname: str,
    send_at: int,
) -> None:
    """Schedule a grant-based message with the custom tracking hostname."""
    request_body: SendMessageRequest = {
        "subject": "Scheduled tracked update",
        "to": [{"email": recipient}],
        "body": '<a href="https://example.com">Open example</a>',
        "send_at": send_at,
        "tracking_options": build_tracking_options(tracking_hostname),
    }
    response = client.messages.send(identifier=grant_id, request_body=request_body)
    print(f"Scheduled message: {response.data.schedule_id}")


def send_transactional_message(
    client: Client,
    sender_domain: str,
    sender_email: str,
    recipient: str,
    tracking_hostname: str,
) -> None:
    """Send from one verified domain while tracking on a separate hostname."""
    request_body: TransactionalSendMessageRequest = {
        "subject": "Transactional tracked update",
        "to": [{"email": recipient}],
        "from_": {"email": sender_email},
        "body": '<a href="https://example.com">Open example</a>',
        "tracking_options": build_tracking_options(tracking_hostname),
    }
    response = client.transactional_send.send(
        # This route value is the verified sender domain, not the tracking hostname.
        domain_name=sender_domain,
        request_body=request_body,
    )
    print(f"Sent transactional message: {response.data.id}")


def parse_send_at(value: Optional[str]) -> int:
    """Parse the scheduled send timestamp."""
    if not value:
        print("Error: NYLAS_SEND_AT is required for the scheduled operation")
        sys.exit(1)
    try:
        return int(value)
    except ValueError:
        print("Error: NYLAS_SEND_AT must be a Unix timestamp")
        sys.exit(1)


def main() -> None:
    """Run one custom tracking hostname example."""
    operation = os.getenv("NYLAS_CUSTOM_TRACKING_OPERATION", "regular")
    if operation not in SUPPORTED_OPERATIONS:
        supported = ", ".join(sorted(SUPPORTED_OPERATIONS))
        print(f"Error: unsupported operation {operation!r}; choose one of {supported}")
        sys.exit(1)

    client = Client(api_key=get_env_or_exit("NYLAS_API_KEY"))
    recipient = get_env_or_exit("RECIPIENT_EMAIL")
    tracking_hostname = get_env_or_exit("NYLAS_TRACKING_HOSTNAME")

    if operation == "transactional":
        send_transactional_message(
            client=client,
            sender_domain=get_env_or_exit("NYLAS_TRANSACTIONAL_SENDER_DOMAIN"),
            sender_email=get_env_or_exit("SENDER_EMAIL"),
            recipient=recipient,
            tracking_hostname=tracking_hostname,
        )
        return

    grant_id = get_env_or_exit("NYLAS_GRANT_ID")
    if operation == "regular":
        send_regular_message(client, grant_id, recipient, tracking_hostname)
    elif operation == "draft":
        create_tracked_draft(client, grant_id, recipient, tracking_hostname)
    else:
        schedule_tracked_message(
            client,
            grant_id,
            recipient,
            tracking_hostname,
            parse_send_at(os.getenv("NYLAS_SEND_AT")),
        )


if __name__ == "__main__":
    main()

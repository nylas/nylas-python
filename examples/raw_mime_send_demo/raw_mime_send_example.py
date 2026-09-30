#!/usr/bin/env python3
"""
Nylas SDK Example: Sending a Raw MIME Message

This example demonstrates how to use messages.send_raw_mime() to send a message
built as raw RFC 822 MIME data. This gives you full control over the outgoing
message, including headers such as Importance and X-Priority.

Required Environment Variables:
    NYLAS_API_KEY: Your Nylas API key
    NYLAS_GRANT_ID: Your Nylas grant ID
    NYLAS_RECIPIENT_EMAIL: The email address to send the test message to

Optional Environment Variables:
    NYLAS_API_URI: The Nylas API URI (defaults to https://api.us.nylas.com)

Usage:
    First, install the SDK in development mode:
    cd /path/to/nylas-python
    pip install -e .

    Then set environment variables and run:
    export NYLAS_API_KEY="your_api_key"
    export NYLAS_GRANT_ID="your_grant_id"
    export NYLAS_RECIPIENT_EMAIL="recipient@example.com"
    python examples/raw_mime_send_demo/raw_mime_send_example.py
"""

import os
import sys
from email.message import EmailMessage
from email.policy import SMTP

from nylas import Client


def get_env_or_exit(var_name: str) -> str:
    """Get an environment variable or exit if not found."""
    value = os.getenv(var_name)
    if not value:
        print(f"Error: {var_name} environment variable is required")
        sys.exit(1)
    return value


def build_high_importance_mime(sender: str, recipient: str) -> bytes:
    """Build a multipart/alternative MIME message marked as high importance."""
    message = EmailMessage()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = "Raw MIME send from the Nylas Python SDK"
    message["Importance"] = "High"
    message["X-Priority"] = "1"
    message.set_content("Hello from a raw MIME message!")
    message.add_alternative(
        "<p>Hello from a <strong>raw MIME</strong> message!</p>", subtype="html"
    )

    # The SMTP policy uses CRLF line endings, as required by RFC 822.
    return message.as_bytes(policy=SMTP)


def main() -> None:
    """Send a raw MIME message and print the result."""
    api_key = get_env_or_exit("NYLAS_API_KEY")
    grant_id = get_env_or_exit("NYLAS_GRANT_ID")
    recipient = get_env_or_exit("NYLAS_RECIPIENT_EMAIL")

    client = Client(
        api_key=api_key,
        api_uri=os.environ.get("NYLAS_API_URI", "https://api.us.nylas.com"),
    )

    grant = client.grants.find(grant_id=grant_id)
    mime = build_high_importance_mime(sender=grant.data.email, recipient=recipient)

    print("Sending raw MIME message...")
    response = client.messages.send_raw_mime(
        identifier=grant_id,
        request_body={"mime": mime},
    )

    print(f"✓ Message sent! ID: {response.data.id}")
    print(f"  Request ID: {response.request_id}")


if __name__ == "__main__":
    main()

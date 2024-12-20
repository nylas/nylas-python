#!/usr/bin/env python3
"""
Nylas SDK Example: Using Metadata Fields with Drafts and Messages

This example demonstrates how to use metadata fields when creating drafts
and sending messages using the Nylas Python SDK.

Required Environment Variables:
    NYLAS_API_KEY: Your Nylas API key
    NYLAS_GRANT_ID: Your Nylas grant ID
    TEST_EMAIL: Email address for sending test messages (optional)

Usage:
    First, install the SDK in development mode:
    cd /path/to/nylas-python
    pip install -e .

    Then set environment variables and run:
    export NYLAS_API_KEY="your_api_key"
    export NYLAS_GRANT_ID="your_grant_id"
    export TEST_EMAIL="recipient@example.com"
    python examples/metadata_field_demo/metadata_example.py
"""

import os
import sys
from typing import Dict, Any, Optional

# Import from local nylas package
from nylas import Client
from nylas.models.errors import NylasAPIError


def get_env_or_exit(var_name: str, required: bool = True) -> Optional[str]:
    """Get an environment variable or exit if required and not found."""
    value = os.getenv(var_name)
    if required and not value:
        print(f"Error: {var_name} environment variable is required")
        sys.exit(1)
    return value


def create_draft_with_metadata(
    client: Client, grant_id: str, metadata: Dict[str, Any], recipient: str
) -> str:
    """Create a draft message with metadata fields."""
    try:
        draft_request = {
            "subject": "Test Draft with Metadata",
            "to": [{"email": recipient}],
            "body": "This is a test draft with metadata fields.",
            "metadata": metadata
        }

        draft, request_id = client.drafts.create(
            identifier=grant_id,
            request_body=draft_request
        )
        print(f"✓ Created draft with ID: {draft.id}")
        print(f"  Request ID: {request_id}")
        return draft.id
    except NylasAPIError as e:
        print(f"✗ Failed to create draft: {e}")
        sys.exit(1)


def send_message_with_metadata(
    client: Client, grant_id: str, metadata: Dict[str, Any], recipient: str
) -> None:
    """Send a message directly with metadata fields."""
    try:
        message_request = {
            "subject": "Test Message with Metadata",
            "to": [{"email": recipient}],
            "body": "This is a test message with metadata fields.",
            "metadata": metadata
        }

        message, request_id = client.messages.send(
            identifier=grant_id,
            request_body=message_request
        )
        print(f"✓ Sent message with ID: {message.id}")
        print(f"  Request ID: {request_id}")
    except NylasAPIError as e:
        print(f"✗ Failed to send message: {e}")
        sys.exit(1)


def main():
    """Main function demonstrating metadata field usage."""
    # Get required environment variables
    api_key = get_env_or_exit("NYLAS_API_KEY")
    grant_id = get_env_or_exit("NYLAS_GRANT_ID")
    recipient = get_env_or_exit("TEST_EMAIL", required=False) or "recipient@example.com"

    # Initialize Nylas client
    client = Client(
        api_key=api_key,
    )

    # Example metadata
    metadata = {
        "campaign_id": "example-123",
        "user_id": "user-456",
        "custom_field": "test-value"
    }

    print("\nDemonstrating Metadata Field Usage")
    print("=================================")

    # Create a draft with metadata
    print("\n1. Creating draft with metadata...")
    draft_id = create_draft_with_metadata(client, grant_id, metadata, recipient)

    # Send a message with metadata
    print("\n2. Sending message with metadata...")
    send_message_with_metadata(client, grant_id, metadata, recipient)

    print("\nExample completed successfully!")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Nylas SDK Example: Handling Provider Errors

This example demonstrates how to handle provider errors when working with the Nylas API,
specifically when trying to access a non-existent calendar.

Required Environment Variables:
    NYLAS_API_KEY: Your Nylas API key
    NYLAS_GRANT_ID: Your Nylas grant ID

Usage:
    First, install the SDK in development mode:
    cd /path/to/nylas-python
    pip install -e .

    Then set environment variables and run:
    export NYLAS_API_KEY="your_api_key"
    export NYLAS_GRANT_ID="your_grant_id"
    python examples/provider_error_demo/provider_error_example.py
"""

import os
import sys
from typing import Optional

from nylas import Client
from nylas.models.errors import NylasApiError


def get_env_or_exit(var_name: str) -> str:
    """Get an environment variable or exit if not found."""
    value = os.getenv(var_name)
    if not value:
        print(f"Error: {var_name} environment variable is required")
        sys.exit(1)
    return value


def demonstrate_provider_error(client: Client, grant_id: str) -> None:
    """Demonstrate how to handle provider errors."""
    # Use a non-existent calendar ID to trigger a provider error
    non_existent_calendar_id = "non-existent-calendar-123"

    try:
        print(f"\nAttempting to fetch events from non-existent calendar: {non_existent_calendar_id}")
        print("------------------------------------------------------------------")
        
        # Attempt to list events with the invalid calendar ID
        events, request_id = client.events.list(
            identifier=grant_id,
            query_params={"calendar_id": non_existent_calendar_id}
        )
        
        # Note: We won't reach this code due to the error
        print("Events retrieved:", events)
        
    except NylasApiError as e:
        print("\nCaught NylasApiError:")
        print(f"✗ Error Type: {e.type}")
        print(f"✗ Provider Error: {e.provider_error}")
        print(f"✗ Request ID: {e.request_id}")
        print(f"✗ Status Code: {e.status_code}")


def main():
    """Main function demonstrating provider error handling."""
    # Get required environment variables
    api_key = get_env_or_exit("NYLAS_API_KEY")
    grant_id = get_env_or_exit("NYLAS_GRANT_ID")

    # Initialize Nylas client
    client = Client(
        api_key=api_key,
    )

    print("\nDemonstrating Provider Error Handling")
    print("====================================")

    # Demonstrate provider error handling
    demonstrate_provider_error(client, grant_id)

    print("\nExample completed!")


if __name__ == "__main__":
    main() 
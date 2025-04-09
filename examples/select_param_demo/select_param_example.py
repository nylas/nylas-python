#!/usr/bin/env python3
"""
Nylas SDK Example: Using Select Parameters

This example demonstrates how to use the 'select' query parameter across different Nylas resources
to optimize API response size and performance by requesting only specific fields.

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
    python examples/select_param_demo/select_param_example.py
"""

import os
import sys
import json
from nylas import Client


def get_env_or_exit(var_name: str) -> str:
    """Get an environment variable or exit if not found."""
    value = os.getenv(var_name)
    if not value:
        print(f"Error: {var_name} environment variable is required")
        sys.exit(1)
    return value


def print_data(data: list, title: str) -> None:
    """Pretty print the data with a title."""
    print(f"\n{title}:")
    for item in data:
        # Convert to dict and pretty print
        item_dict = item.to_dict()
        print(json.dumps(item_dict, indent=2))


def demonstrate_messages(client: Client, grant_id: str) -> None:
    """Demonstrate select parameter usage with Messages resource."""
    print("\n=== Messages Resource ===")
    
    # Backwards compatibility - fetch all fields
    print("\nFetching messages (all fields):")
    messages = client.messages.list(identifier=grant_id, query_params={"limit": 2})
    print_data(messages.data, "Full message data (all fields)")
    
    # Using select parameter - fetch only specific fields
    print("\nFetching messages with select (only id and subject):")
    messages = client.messages.list(
        identifier=grant_id,
        query_params={"limit": 2, "select": "id,subject"}
    )
    print_data(messages.data, "Minimal message data (only selected fields)")


def demonstrate_calendars(client: Client, grant_id: str) -> None:
    """Demonstrate select parameter usage with Calendars resource."""
    print("\n=== Calendars Resource ===")
    
    # Backwards compatibility - fetch all fields
    print("\nFetching calendars (all fields):")
    calendars = client.calendars.list(identifier=grant_id, query_params={"limit": 2})
    print_data(calendars.data, "Full calendar data (all fields)")
    
    # Using select parameter - fetch only specific fields
    print("\nFetching calendars with select (only id and name):")
    calendars = client.calendars.list(
        identifier=grant_id,
        query_params={"limit": 2, "select": "id,name"}
    )
    print_data(calendars.data, "Minimal calendar data (only selected fields)")


def demonstrate_events(client: Client, grant_id: str) -> None:
    """Demonstrate select parameter usage with Events resource."""
    print("\n=== Events Resource ===")
    
    # First, get a calendar ID
    print("\nFetching first calendar to use for events...")
    calendars = client.calendars.list(identifier=grant_id, query_params={"limit": 1})
    if not calendars.data:
        print("No calendars found. Skipping events demonstration.")
        return
    
    calendar_id = calendars.data[0].id
    print(f"Using calendar: {calendars.data[0].name} (ID: {calendar_id})")
    
    # Backwards compatibility - fetch all fields
    print("\nFetching events (all fields):")
    events = client.events.list(
        identifier=grant_id,
        query_params={"limit": 2, "calendar_id": calendar_id}
    )
    print_data(events.data, "Full event data (all fields)")
    
    # Using select parameter - fetch only specific fields
    print("\nFetching events with select (only id and title):")
    events = client.events.list(
        identifier=grant_id,
        query_params={
            "limit": 2,
            "calendar_id": calendar_id,
            "select": "id,title"
        }
    )
    print_data(events.data, "Minimal event data (only selected fields)")


def demonstrate_drafts(client: Client, grant_id: str) -> None:
    """Demonstrate select parameter usage with Drafts resource."""
    print("\n=== Drafts Resource ===")
    
    # Backwards compatibility - fetch all fields
    print("\nFetching drafts (all fields):")
    drafts = client.drafts.list(identifier=grant_id, query_params={"limit": 2})
    print_data(drafts.data, "Full draft data (all fields)")
    
    # Using select parameter - fetch only specific fields
    print("\nFetching drafts with select (only id and subject):")
    drafts = client.drafts.list(
        identifier=grant_id,
        query_params={"limit": 2, "select": "id,subject"}
    )
    print_data(drafts.data, "Minimal draft data (only selected fields)")


def demonstrate_contacts(client: Client, grant_id: str) -> None:
    """Demonstrate select parameter usage with Contacts resource."""
    print("\n=== Contacts Resource ===")
    
    # Backwards compatibility - fetch all fields
    print("\nFetching contacts (all fields):")
    contacts = client.contacts.list(identifier=grant_id, query_params={"limit": 2})
    print_data(contacts.data, "Full contact data (all fields)")
    
    # Using select parameter - fetch only specific fields
    print("\nFetching contacts with select (only id, grant_id, and given_name):")
    contacts = client.contacts.list(
        identifier=grant_id,
        query_params={"limit": 2, "select": "id,grant_id,given_name"}
    )
    print_data(contacts.data, "Minimal contact data (only selected fields)")


def main():
    """Main function demonstrating select parameter usage across resources."""
    # Get required environment variables
    api_key = get_env_or_exit("NYLAS_API_KEY")
    grant_id = get_env_or_exit("NYLAS_GRANT_ID")

    # Initialize Nylas client
    client = Client(
        api_key=api_key,
    )

    print("\nDemonstrating Select Parameter Usage")
    print("===================================")
    print("This shows both backwards compatibility and selective field fetching")

    # Demonstrate select parameter across different resources
    demonstrate_messages(client, grant_id)
    demonstrate_calendars(client, grant_id)
    demonstrate_events(client, grant_id)
    demonstrate_drafts(client, grant_id)
    demonstrate_contacts(client, grant_id)

    print("\nExample completed!")


if __name__ == "__main__":
    main() 
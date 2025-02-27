#!/usr/bin/env python3
"""
Nylas SDK Example: Using Import Events

This example demonstrates how to use the 'list_import_events' method to import and
synchronize events from a calendar within a given time frame.

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
    python examples/import_events_demo/import_events_example.py
"""

import os
import sys
import json
import time
from datetime import datetime, timedelta
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


def demonstrate_basic_import(client: Client, grant_id: str) -> None:
    """Demonstrate basic usage of list_import_events with primary calendar."""
    print("\n=== Basic Import Events ===")
    
    print("\nFetching events from primary calendar:")
    events = client.events.list_import_events(
        identifier=grant_id,
        query_params={"calendar_id": "primary", "max_results": 2}
    )
    print_data(events.data, "Basic import events")


def demonstrate_time_filtered_import(client: Client, grant_id: str) -> None:
    """Demonstrate import events with time filtering."""
    print("\n=== Time Filtered Import Events ===")
    
    # Get timestamps for a one-month period
    now = int(time.time())
    one_month_ago = now - (30 * 24 * 60 * 60)  # 30 days ago
    one_month_future = now + (30 * 24 * 60 * 60)  # 30 days in future
    
    # Format dates for display
    from_date = datetime.fromtimestamp(one_month_ago).strftime("%Y-%m-%d")
    to_date = datetime.fromtimestamp(one_month_future).strftime("%Y-%m-%d")
    
    print(f"\nFetching events from {from_date} to {to_date}:")
    events = client.events.list_import_events(
        identifier=grant_id,
        query_params={
            "calendar_id": "primary",
            "start": one_month_ago,
            "end": one_month_future
        }
    )
    print_data(events.data, f"Events from {from_date} to {to_date}")


def demonstrate_max_results(client: Client, grant_id: str) -> None:
    """Demonstrate import events with max_results parameter."""
    print("\n=== Import Events with Max Results ===")
    
    print("\nFetching events with max_results=5:")
    events = client.events.list_import_events(
        identifier=grant_id,
        query_params={
            "calendar_id": "primary",
            "max_results": 5
        }
    )
    print_data(events.data, "Events with max_results=5")


def demonstrate_field_selection(client: Client, grant_id: str) -> None:
    """Demonstrate import events with field selection."""
    print("\n=== Import Events with Field Selection ===")
    
    print("\nFetching events with select parameter (only id, title, and when):")
    events = client.events.list_import_events(
        identifier=grant_id,
        query_params={
            "calendar_id": "primary",
            "max_results": 2,
            "select": "id,title,when"
        }
    )
    print_data(events.data, "Events with selected fields only")


def demonstrate_pagination(client: Client, grant_id: str) -> None:
    """Demonstrate pagination for import events."""
    print("\n=== Import Events with Pagination ===")
    
    # First page
    print("\nFetching first page of events (max_results=3):")
    first_page = client.events.list_import_events(
        identifier=grant_id,
        query_params={
            "calendar_id": "primary",
            "max_results": 3
        }
    )
    print_data(first_page.data, "First page of events")
    
    # If there's a next page, fetch it
    if hasattr(first_page, 'next_cursor') and first_page.next_cursor:
        print("\nFetching second page of events:")
        second_page = client.events.list_import_events(
            identifier=grant_id,
            query_params={
                "calendar_id": "primary",
                "max_results": 3,
                "page_token": first_page.next_cursor
            }
        )
        print_data(second_page.data, "Second page of events")
    else:
        print("\nNo second page available - not enough events to paginate")


def demonstrate_full_example(client: Client, grant_id: str) -> None:
    """Demonstrate a full example with all parameters."""
    print("\n=== Full Import Events Example ===")
    
    # Get timestamps for the current year
    now = datetime.now()
    start_of_year = datetime(now.year, 1, 1).timestamp()
    end_of_year = datetime(now.year, 12, 31, 23, 59, 59).timestamp()
    
    print(f"\nFetching events for {now.year} with all parameters:")
    events = client.events.list_import_events(
        identifier=grant_id,
        query_params={
            "calendar_id": "primary",
            "max_results": 10,
            "start": int(start_of_year),
            "end": int(end_of_year),
            "select": "id,title,description,when,participants,location"
        }
    )
    print_data(events.data, f"Events for {now.year} with all parameters")


def main():
    """Main function demonstrating the import events method."""
    # Get required environment variables
    api_key = get_env_or_exit("NYLAS_API_KEY")
    grant_id = get_env_or_exit("NYLAS_GRANT_ID")

    # Initialize Nylas client
    client = Client(
        api_key=api_key,
    )

    print("\nDemonstrating Import Events Functionality")
    print("========================================")
    
    # Demonstrate different ways to use list_import_events
    demonstrate_basic_import(client, grant_id)
    demonstrate_time_filtered_import(client, grant_id)
    demonstrate_max_results(client, grant_id)
    demonstrate_field_selection(client, grant_id)
    demonstrate_pagination(client, grant_id)
    demonstrate_full_example(client, grant_id)

    print("\nExample completed!")


if __name__ == "__main__":
    main() 
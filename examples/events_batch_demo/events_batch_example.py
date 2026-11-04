#!/usr/bin/env python3
"""
Nylas SDK Example: Creating, Updating, and Deleting Events in a Batch

This example demonstrates how to use events.batch() to run several event operations
in a single request, and how to retry only the failed operations that are safe to retry.

The example changes the calendar. It creates two events one day from now, renames one
of them, and then deletes both. The second batch also deletes an event ID that doesn't
exist, to show how the results of a partial failure (HTTP 207) are returned.

Batch operations are only available for Google and Microsoft grants.

Required Environment Variables:
    NYLAS_API_KEY: Your Nylas API key
    NYLAS_GRANT_ID: Your Nylas grant ID for a Google or Microsoft account

Optional Environment Variables:
    NYLAS_API_URI: The Nylas API URI (defaults to https://api.us.nylas.com)
    NYLAS_CALENDAR_ID: The calendar to use (defaults to "primary")

Usage:
    First, install the SDK in development mode:
    cd /path/to/nylas-python
    pip install -e .

    Then set environment variables and run:
    export NYLAS_API_KEY="your_api_key"
    export NYLAS_GRANT_ID="your_grant_id"
    python examples/events_batch_demo/events_batch_example.py
"""

import os
import sys
import time

from nylas import Client
from nylas.models.errors import NylasApiError

RETRYABLE_STATUSES = {429, 503}
DEFAULT_RETRY_SECONDS = 1
MAX_ATTEMPTS = 3


def get_env_or_exit(var_name: str) -> str:
    """Get an environment variable or exit if not found."""
    value = os.getenv(var_name)
    if not value:
        print(f"Error: {var_name} environment variable is required")
        sys.exit(1)
    return value


def run_batch(client, grant_id, calendar_id, operations):
    """
    Run a batch of event operations, and retry the failed operations that are safe to retry.

    Returns one result for each operation, in the same order as the operations.
    """
    results = [None] * len(operations)
    pending = list(range(len(operations)))

    for attempt in range(1, MAX_ATTEMPTS + 1):
        response = client.events.batch(
            identifier=grant_id,
            query_params={"calendar_id": calendar_id},
            request_body={"operations": [operations[index] for index in pending]},
        )

        retry = []
        wait_seconds = 0
        # response.data[i] is the result of the i-th operation in this request.
        for index, result in zip(pending, response.data):
            results[index] = result
            if result.error is None:
                continue
            if result.provider_event_created:
                # The provider created the event before a later step failed.
                # Retrying this operation would create a duplicate event.
                continue
            if result.status in RETRYABLE_STATUSES:
                retry.append(index)
                # retry_after can be 0, which means the operation can be retried now.
                if result.retry_after is None:
                    delay = DEFAULT_RETRY_SECONDS
                else:
                    delay = result.retry_after
                wait_seconds = max(wait_seconds, delay)

        if not retry or attempt == MAX_ATTEMPTS:
            break
        print(f"  Retrying {len(retry)} operation(s) in {wait_seconds} second(s)...")
        time.sleep(wait_seconds)
        pending = retry

    return results


def print_results(operations, results):
    """Print the outcome of each operation."""
    for operation, result in zip(operations, results):
        target = operation.get("event_id") or operation["body"]["title"]
        if result.error is None:
            print(f"  ✓ {operation['method']} {target}: HTTP {result.status}")
            continue
        print(
            f"  ✗ {operation['method']} {target}: HTTP {result.status} "
            f"{result.error.type}: {result.error.message}"
        )
        if result.provider_event_created:
            print("    The provider created this event anyway. Don't retry it.")


def run_demo(client, grant_id, calendar_id):
    """Create two events, rename one of them, and then delete both."""
    start = int(time.time()) + 24 * 60 * 60
    create_operations = [
        {
            "method": "create",
            "body": {
                "title": "Batch demo: standup",
                "when": {"start_time": start, "end_time": start + 30 * 60},
            },
        },
        {
            "method": "create",
            "body": {
                "title": "Batch demo: retro",
                "when": {"start_time": start + 60 * 60, "end_time": start + 90 * 60},
            },
        },
    ]

    print("Creating two events in one batch...")
    results = run_batch(client, grant_id, calendar_id, create_operations)
    print_results(create_operations, results)
    event_ids = [result.data.id for result in results if result.data is not None]
    if not event_ids:
        return

    try:
        change_operations = [
            {
                "method": "update",
                "event_id": event_ids[0],
                "body": {"title": "Batch demo: renamed standup"},
            },
            {"method": "delete", "event_id": "batch-demo-missing-event"},
        ]
        print("\nRenaming an event and deleting an event that doesn't exist...")
        results = run_batch(client, grant_id, calendar_id, change_operations)
        print_results(change_operations, results)
    finally:
        delete_operations = [
            {"method": "delete", "event_id": event_id} for event_id in event_ids
        ]
        print("\nDeleting the created events in one batch...")
        results = run_batch(client, grant_id, calendar_id, delete_operations)
        print_results(delete_operations, results)


def main() -> None:
    """Run the batch example."""
    api_key = get_env_or_exit("NYLAS_API_KEY")
    grant_id = get_env_or_exit("NYLAS_GRANT_ID")
    calendar_id = os.getenv("NYLAS_CALENDAR_ID", "primary")

    client = Client(
        api_key=api_key,
        api_uri=os.getenv("NYLAS_API_URI", "https://api.us.nylas.com"),
    )

    try:
        run_demo(client, grant_id, calendar_id)
    except NylasApiError as error:
        # events.batch() raises only when the API rejects the whole request,
        # for example with HTTP 400 for an invalid batch or an unsupported provider.
        print(
            f"Error: {error} (HTTP {error.status_code}, request ID {error.request_id})"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Nylas SDK Example: Response Headers Demo

This example demonstrates how to access and use response headers from various Nylas API
responses, including successful responses and error cases.

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
    python examples/response_headers_demo/response_headers_example.py
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


def print_response_headers(headers: dict, prefix: str = "") -> None:
    """Helper function to print response headers."""
    print(f"\n{prefix} Response Headers:")
    print("------------------------")
    for key, value in headers.items():
        print(f"{key}: {value}")


def demonstrate_list_response_headers(client: Client, grant_id: str) -> None:
    """Demonstrate headers in list responses."""
    print("\nDemonstrating List Response Headers")
    print("----------------------------------")
    
    try:
        # List messages to get a ListResponse
        messages = client.messages.list(identifier=grant_id)
        
        print("✓ Successfully retrieved messages")
        print_response_headers(messages.headers)
        print(f"Total messages count: {len(messages.data)}")
        
    except NylasApiError as e:
        print("\nError occurred while listing messages:")
        print(f"✗ Error Type: {e.type}")
        print(f"✗ Provider Error: {e.provider_error}")
        print(f"✗ Request ID: {e.request_id}")
        print_response_headers(e.headers, "Error")


def demonstrate_list_response_headers_with_pagination(client: Client, grant_id: str) -> None:
    """Demonstrate headers in list responses with pagination."""
    print("\nDemonstrating List Response Headers with Pagination")
    print("--------------------------------------------------")

    try:
        # List messages to get a ListResponse
        threads = client.threads.list(identifier=grant_id, query_params={"limit": 1})
        
        print("✓ Successfully retrieved threads")
        print_response_headers(threads.headers)
        print(f"Total threads count: {len(threads.data)}")
        
    except NylasApiError as e:
        print("\nError occurred while listing threads:")
        print(f"✗ Error Type: {e.type}")
        print(f"✗ Provider Error: {e.provider_error}")
        print(f"✗ Request ID: {e.request_id}")
        print_response_headers(e.headers, "Error")


def demonstrate_find_response_headers(client: Client, grant_id: str) -> None:
    """Demonstrate headers in find/single-item responses."""
    print("\nDemonstrating Find Response Headers")
    print("----------------------------------")
    
    try:
        # Get the first message to demonstrate single-item response
        messages = client.messages.list(identifier=grant_id)
        if not messages.data:
            print("No messages found to demonstrate find response")
            return
            
        message_id = messages.data[0].id
        message = client.messages.find(identifier=grant_id, message_id=message_id)
        
        print("✓ Successfully retrieved single message")
        print_response_headers(message.headers)
        
    except NylasApiError as e:
        print("\nError occurred while finding message:")
        print(f"✗ Error Type: {e.type}")
        print(f"✗ Provider Error: {e.provider_error}")
        print(f"✗ Request ID: {e.request_id}")
        print_response_headers(e.headers, "Error")


def demonstrate_error_response_headers(client: Client, grant_id: str) -> None:
    """Demonstrate headers in error responses."""
    print("\nDemonstrating Error Response Headers")
    print("---------------------------------")
    
    try:
        # Attempt to find a non-existent message
        message = client.messages.find(
            identifier=grant_id,
            message_id="non-existent-id-123"
        )
        
    except NylasApiError as e:
        print("✓ Successfully caught expected error")
        print(f"✗ Error Type: {e.type}")
        print(f"✗ Provider Error: {e.provider_error}")
        print(f"✗ Request ID: {e.request_id}")
        print(f"✗ Status Code: {e.status_code}")
        print_response_headers(e.headers, "Error")


def main():
    """Main function demonstrating response headers."""
    # Get required environment variables
    api_key = get_env_or_exit("NYLAS_API_KEY")
    grant_id = get_env_or_exit("NYLAS_GRANT_ID")

    # Initialize Nylas client
    client = Client(
        api_key=api_key,
    )

    print("\nDemonstrating Response Headers")
    print("============================")

    # Demonstrate different types of responses and their headers
    demonstrate_list_response_headers(client, grant_id)
    demonstrate_list_response_headers_with_pagination(client, grant_id)
    demonstrate_find_response_headers(client, grant_id)
    demonstrate_error_response_headers(client, grant_id)

    print("\nExample completed!")


if __name__ == "__main__":
    main() 
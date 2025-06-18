#!/usr/bin/env python3
"""
Nylas SDK Example: Using Single Level Parameter for Folders

This example demonstrates how to use the 'single_level' query parameter when listing folders
to control the folder hierarchy traversal for Microsoft accounts.

Required Environment Variables:
    NYLAS_API_KEY: Your Nylas API key
    NYLAS_GRANT_ID: Your Nylas grant ID (must be a Microsoft account)

Usage:
    First, install the SDK in development mode:
    cd /path/to/nylas-python
    pip install -e .

    Then set environment variables and run:
    export NYLAS_API_KEY="your_api_key"
    export NYLAS_GRANT_ID="your_microsoft_grant_id"
    python examples/folders_demo/folders_single_level_example.py
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


def print_folders(folders: list, title: str) -> None:
    """Pretty print the folders with a title."""
    print(f"\n{title}:")
    if not folders:
        print("  No folders found.")
        return

    for folder in folders:
        # Convert to dict and pretty print relevant fields
        folder_dict = folder.to_dict()
        print(
            f"  - {folder_dict.get('name', 'Unknown')} (ID: {folder_dict.get('id', 'Unknown')})"
        )
        if folder_dict.get("parent_id"):
            print(f"    Parent ID: {folder_dict['parent_id']}")
        if folder_dict.get("child_count") is not None:
            print(f"    Child Count: {folder_dict['child_count']}")


def demonstrate_multi_level_folders(client: Client, grant_id: str) -> None:
    """Demonstrate multi-level folder hierarchy (default behavior)."""
    print("\n=== Multi-Level Folder Hierarchy (Default) ===")

    # Default behavior - retrieves folders across multi-level hierarchy
    print("\nFetching folders with multi-level hierarchy (single_level=False):")
    folders = client.folders.list(
        identifier=grant_id, query_params={"single_level": False}
    )
    print_folders(folders.data, "Multi-level folder hierarchy")

    # Also demonstrate without explicitly setting single_level (default behavior)
    print("\nFetching folders without single_level parameter (default behavior):")
    folders = client.folders.list(identifier=grant_id)
    print_folders(folders.data, "Default folder hierarchy (multi-level)")


def demonstrate_single_level_folders(client: Client, grant_id: str) -> None:
    """Demonstrate single-level folder hierarchy."""
    print("\n=== Single-Level Folder Hierarchy ===")

    # Single-level hierarchy - only retrieves folders from the top level
    print("\nFetching folders with single-level hierarchy (single_level=True):")
    folders = client.folders.list(
        identifier=grant_id, query_params={"single_level": True}
    )
    print_folders(folders.data, "Single-level folder hierarchy")


def demonstrate_combined_parameters(client: Client, grant_id: str) -> None:
    """Demonstrate single_level combined with other parameters."""
    print("\n=== Combined Parameters ===")

    # Combine single_level with other query parameters
    print("\nFetching limited single-level folders with select fields:")
    folders = client.folders.list(
        identifier=grant_id,
        query_params={
            "single_level": True,
            "limit": 5,
            "select": "id,name,parent_id,child_count",
        },
    )
    print_folders(folders.data, "Limited single-level folders with selected fields")


def compare_hierarchies(client: Client, grant_id: str) -> None:
    """Compare single-level vs multi-level folder counts."""
    print("\n=== Hierarchy Comparison ===")

    # Get multi-level count
    multi_level_folders = client.folders.list(
        identifier=grant_id, query_params={"single_level": False}
    )
    multi_level_count = len(multi_level_folders.data)

    # Get single-level count
    single_level_folders = client.folders.list(
        identifier=grant_id, query_params={"single_level": True}
    )
    single_level_count = len(single_level_folders.data)

    print(f"\nFolder count comparison:")
    print(f"  Multi-level hierarchy: {multi_level_count} folders")
    print(f"  Single-level hierarchy: {single_level_count} folders")

    if multi_level_count > single_level_count:
        print(
            f"  Difference: {multi_level_count - single_level_count} folders in sub-hierarchies"
        )
    elif single_level_count == multi_level_count:
        print("  No nested folders detected in this account")


def main():
    """Main function demonstrating single_level parameter usage for folders."""
    # Get required environment variables
    api_key = get_env_or_exit("NYLAS_API_KEY")
    grant_id = get_env_or_exit("NYLAS_GRANT_ID")

    # Initialize Nylas client
    client = Client(api_key=api_key)

    print("\nDemonstrating Single Level Parameter for Folders")
    print("===============================================")
    print("This parameter is Microsoft-only and controls folder hierarchy traversal")
    print(f"Using Grant ID: {grant_id}")

    try:
        # Demonstrate different folder hierarchy options
        demonstrate_multi_level_folders(client, grant_id)
        demonstrate_single_level_folders(client, grant_id)
        demonstrate_combined_parameters(client, grant_id)
        compare_hierarchies(client, grant_id)

        print("\n=== Summary ===")
        print("• single_level=True: Returns only top-level folders (Microsoft only)")
        print("• single_level=False: Returns folders from all levels (default)")
        print("• This parameter helps optimize performance for Microsoft accounts")
        print("• Can be combined with other query parameters like limit and select")

    except Exception as e:
        print(f"\nError: {e}")
        print("\nNote: This example requires a Microsoft grant ID.")
        print("The single_level parameter only works with Microsoft accounts.")

    print("\nExample completed!")


if __name__ == "__main__":
    main()

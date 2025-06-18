import os
from nylas import Client


def main():
    """
    This example demonstrates how to use the include_hidden_folders parameter
    when listing folders with the Nylas SDK.

    The include_hidden_folders parameter is Microsoft-specific and when set to True,
    it includes hidden folders in the response.
    """

    # Initialize the client
    nylas = Client(
        api_key=os.environ.get("NYLAS_API_KEY"),
        api_uri=os.environ.get("NYLAS_API_URI", "https://api.us.nylas.com"),
    )

    # Get the grant ID from environment variable
    grant_id = os.environ.get("NYLAS_GRANT_ID")

    if not grant_id:
        print("Please set the NYLAS_GRANT_ID environment variable")
        return

    try:
        print("Listing folders without hidden folders (default behavior):")
        print("=" * 60)

        # List folders without hidden folders (default)
        folders_response = nylas.folders.list(
            identifier=grant_id, query_params={"limit": 10}
        )

        for folder in folders_response.data:
            print(f"- {folder.name} (ID: {folder.id})")

        print(f"\nTotal folders found: {len(folders_response.data)}")

        # Now list folders WITH hidden folders (Microsoft only)
        print("\n\nListing folders with hidden folders included (Microsoft only):")
        print("=" * 70)

        folders_with_hidden_response = nylas.folders.list(
            identifier=grant_id,
            query_params={"include_hidden_folders": True, "limit": 10},
        )

        for folder in folders_with_hidden_response.data:
            print(f"- {folder.name} (ID: {folder.id})")

        print(
            f"\nTotal folders found (including hidden): {len(folders_with_hidden_response.data)}"
        )

        # Compare the counts
        hidden_count = len(folders_with_hidden_response.data) - len(
            folders_response.data
        )
        if hidden_count > 0:
            print(f"\nFound {hidden_count} additional hidden folder(s)")
        else:
            print("\nNo additional hidden folders found")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

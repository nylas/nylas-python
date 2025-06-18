# Include Hidden Folders Example

This example demonstrates how to use the `include_hidden_folders` query parameter when listing folders with the Nylas Python SDK.

## Overview

The `include_hidden_folders` parameter is Microsoft-specific and allows you to include hidden folders in the folder listing response. By default, this parameter is `False` and hidden folders are not included.

## Prerequisites

1. A Nylas application with Microsoft OAuth configured
2. A valid Nylas API key
3. A grant ID for a Microsoft account

## Setup

1. Set your environment variables:
   ```bash
   export NYLAS_API_KEY="your_api_key_here"
   export NYLAS_GRANT_ID="your_grant_id_here"
   export NYLAS_API_URI="https://api.us.nylas.com"  # Optional, defaults to US
   ```

2. Install the Nylas Python SDK:
   ```bash
   pip install nylas
   ```

## Running the Example

```bash
python include_hidden_folders_example.py
```

## Code Explanation

The example demonstrates two scenarios:

1. **Default behavior**: Lists folders without hidden folders
   ```python
   folders_response = nylas.folders.list(
       identifier=grant_id,
       query_params={"limit": 10}
   )
   ```

2. **With hidden folders**: Lists folders including hidden folders (Microsoft only)
   ```python
   folders_with_hidden_response = nylas.folders.list(
       identifier=grant_id,
       query_params={
           "include_hidden_folders": True,
           "limit": 10
       }
   )
   ```

## Expected Output

The example will show:
- List of regular folders
- List of folders including hidden ones (if any)
- Comparison showing how many additional hidden folders were found

## Note

This feature is **Microsoft-specific only**. For other providers (Google, IMAP), the `include_hidden_folders` parameter will be ignored. 
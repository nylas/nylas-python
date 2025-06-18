# Folders Single Level Parameter Example

This example demonstrates how to use the `single_level` query parameter when listing folders to control folder hierarchy traversal for Microsoft accounts.

## Overview

The `single_level` parameter is a Microsoft-only feature that allows you to control whether the folders API returns:
- **`single_level=true`**: Only top-level folders (single-level hierarchy)
- **`single_level=false`**: All folders including nested ones (multi-level hierarchy, default)

This parameter is useful for:
- **Performance optimization**: Reducing response size when you only need top-level folders
- **UI simplification**: Building folder trees incrementally 
- **Microsoft-specific behavior**: Taking advantage of Microsoft's folder hierarchy structure

## Prerequisites

- Nylas API key
- Nylas grant ID for a Microsoft account (this parameter only works with Microsoft accounts)

## Setup

1. Install the SDK in development mode:
   ```bash
   cd /path/to/nylas-python
   pip install -e .
   ```

2. Set your environment variables:
   ```bash
   export NYLAS_API_KEY="your_api_key"
   export NYLAS_GRANT_ID="your_microsoft_grant_id"
   ```

## Running the Example

```bash
python examples/folders_demo/folders_single_level_example.py
```

## What the Example Demonstrates

1. **Multi-level folder hierarchy** (default behavior)
2. **Single-level folder hierarchy** using `single_level=true`
3. **Combined parameters** showing how to use `single_level` with other query parameters
4. **Hierarchy comparison** showing the difference in folder counts

## Expected Output

The example will show:
- Folders returned with multi-level hierarchy
- Folders returned with single-level hierarchy only
- Count comparison between the two approaches
- How to combine the parameter with other options like `limit` and `select`

## Use Cases

- **Folder tree UI**: Load top-level folders first, then expand as needed
- **Performance**: Reduce API response size for Microsoft accounts with deep folder structures
- **Microsoft-specific integrations**: Take advantage of Microsoft's native folder organization

## Note

This parameter only works with Microsoft accounts. If you use it with other providers, it will be ignored. 
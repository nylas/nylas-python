# Provider Error Handling Example

This example demonstrates how to properly handle provider errors when working with the Nylas API. It specifically shows how to catch and process errors that occur when trying to access a non-existent calendar.

## Features

- Demonstrates proper error handling for Nylas API provider errors
- Shows how to access error details including:
  - Error message
  - Error type
  - Provider error message
  - Request ID
  - Status code
- Includes clear output and status messages

## Prerequisites

1. A Nylas account with API access
2. Python 3.x installed
3. Local installation of the Nylas Python SDK (this repository)

## Setup

1. Install the SDK in development mode from the repository root:
```bash
cd /path/to/nylas-python
pip install -e .
```

2. Set your environment variables:
```bash
export NYLAS_API_KEY="your_api_key"
export NYLAS_GRANT_ID="your_grant_id"
```

3. Run the example from the repository root:
```bash
python examples/provider_error_demo/provider_error_example.py
```

## Example Output

```
Demonstrating Provider Error Handling
====================================

Attempting to fetch events from non-existent calendar: non-existent-calendar-123
------------------------------------------------------------------

Caught NylasApiError:
✗ Error Message: Calendar not found
✗ Error Type: invalid_request_error
✗ Provider Error: The calendar ID provided does not exist
✗ Request ID: req-abc-123
✗ Status Code: 404

Example completed!
```

## Error Handling

The example demonstrates how to handle:
- Missing environment variables
- API authentication errors
- Provider-specific errors
- Non-existent resource errors

## Documentation

For more information about the Nylas Python SDK and its features, visit:
- [Nylas Python SDK Documentation](https://developer.nylas.com/docs/sdks/python/)
- [Nylas API Reference](https://developer.nylas.com/docs/api/) 
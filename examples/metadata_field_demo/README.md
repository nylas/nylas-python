# Metadata Field Example

This example demonstrates how to use metadata fields when creating drafts and sending messages using the Nylas Python SDK.

## Features

- Create drafts with custom metadata fields
- Send messages with custom metadata fields
- Error handling and environment variable configuration
- Clear output and status messages

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
export TEST_EMAIL="recipient@example.com"  # Optional
```

3. Run the example from the repository root:
```bash
python examples/metadata_field_demo/metadata_example.py
```

## Example Output

```
Demonstrating Metadata Field Usage
=================================

1. Creating draft with metadata...
✓ Created draft with ID: draft-abc123
  Request ID: req-xyz789

2. Sending message with metadata...
✓ Sent message with ID: msg-def456
  Request ID: req-uvw321

Example completed successfully!
```

## Error Handling

The example includes proper error handling for:
- Missing environment variables
- API authentication errors
- Draft creation failures
- Message sending failures

## Documentation

For more information about the Nylas Python SDK and its features, visit:
- [Nylas Python SDK Documentation](https://developer.nylas.com/docs/sdks/python/)
- [Nylas API Reference](https://developer.nylas.com/docs/api/)

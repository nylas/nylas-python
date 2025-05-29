# Message Fields Demo

This example demonstrates the usage of the new message `fields` query parameter values (`include_tracking_options` and `raw_mime`) introduced in the Nylas API. These fields allow you to access tracking information and raw MIME data for messages.

## Features Demonstrated

1. **include_tracking_options Field**: Shows how to fetch messages with their tracking options (opens, thread_replies, links, and label).
2. **raw_mime Field**: Demonstrates how to retrieve the raw MIME content of messages as Base64url-encoded data.
3. **Backwards Compatibility**: Shows that existing code continues to work as expected without specifying the new fields.
4. **TrackingOptions Model**: Demonstrates working with the new TrackingOptions dataclass for serialization and deserialization.

## API Fields Overview

### include_tracking_options
When using `fields=include_tracking_options`, the API returns messages with their tracking settings:
- `opens`: Boolean indicating if message open tracking is enabled
- `thread_replies`: Boolean indicating if thread replied tracking is enabled  
- `links`: Boolean indicating if link clicked tracking is enabled
- `label`: String label describing the message tracking purpose

### raw_mime
When using `fields=raw_mime`, the API returns only essential fields plus the raw MIME content:
- `grant_id`: The grant identifier
- `object`: The object type ("message")  
- `id`: The message identifier
- `raw_mime`: Base64url-encoded string containing the complete message data

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
python examples/message_fields_demo/message_fields_example.py
```

## Example Output

```
Demonstrating Message Fields Usage
=================================

=== Standard Message Fetching (Backwards Compatible) ===
Fetching messages with standard fields...
✓ Found 2 messages with standard payload

=== Include Tracking Options ===
Fetching messages with tracking options...
✓ Found 2 messages with tracking data
Message tracking: opens=True, links=False, label="Campaign A"

=== Raw MIME Content ===
Fetching messages with raw MIME data...
✓ Found 2 messages with raw MIME content
Raw MIME length: 1245 characters

=== TrackingOptions Model Demo ===
Creating and serializing TrackingOptions...
✓ TrackingOptions serialization works correctly

Example completed successfully!
```

## Use Cases

### Tracking Options
- **Email Campaign Analytics**: Monitor open rates, link clicks, and thread engagement
- **Marketing Automation**: Track customer engagement with promotional emails
- **CRM Integration**: Feed tracking data into customer relationship management systems

### Raw MIME
- **Email Archival**: Store complete email data including headers and formatting
- **Email Migration**: Transfer emails between systems with full fidelity
- **Security Analysis**: Examine email headers and structure for security purposes
- **Custom Email Parsing**: Build custom email processing pipelines

## Error Handling

The example includes proper error handling for:
- Missing environment variables
- API authentication errors
- Empty message collections
- Invalid field parameters

## Documentation

For more information about the Nylas Python SDK and message fields, visit:
- [Nylas Python SDK Documentation](https://developer.nylas.com/docs/sdks/python/)
- [Nylas API Messages Reference](https://developer.nylas.com/docs/api/v3/ecc/#tag--Messages) 
# is_plaintext Demo

This example demonstrates the usage of the new `is_plaintext` property for messages and drafts in the Nylas API. This property controls whether message content is sent as plain text or HTML in the MIME data.

## Features Demonstrated

1. **Plain Text Messages**: Shows how to send messages with `is_plaintext=True` to send content as plain text without HTML in MIME data.
2. **HTML Messages**: Demonstrates sending messages with `is_plaintext=False` to include HTML formatting in MIME data.
3. **Backwards Compatibility**: Shows that existing code continues to work without specifying the `is_plaintext` property.
4. **Draft Operations**: Demonstrates using `is_plaintext` with draft creation and updates.

## API Property Overview

### is_plaintext

- **Type**: `boolean`
- **Default**: `false`
- **Available in**: 
  - `messages.send()` - Send message endpoint
  - `drafts.create()` - Create draft endpoint
  - `drafts.update()` - Update draft endpoint

When `is_plaintext` is:
- `true`: The message body is sent as plain text and the MIME data doesn't include the HTML version of the message
- `false`: The message body is sent as HTML and MIME data includes HTML formatting
- Not specified: Uses API default behavior (same as `false`)

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
python examples/is_plaintext_demo/is_plaintext_example.py
```

## Example Output

```
Demonstrating is_plaintext Property Usage
=======================================

=== Sending Plain Text Message ===
Sending message with is_plaintext=True...
✓ Message request prepared with is_plaintext=True
📧 Message configured to be sent as plain text (MIME without HTML version)

=== Sending HTML Message ===
Sending message with is_plaintext=False (HTML)...
✓ Message request prepared with is_plaintext=False
🌐 Message configured to be sent as HTML (MIME includes HTML version)

=== Backwards Compatibility (No is_plaintext specified) ===
Sending message without is_plaintext property...
✓ Existing code continues to work without modification

=== Creating Plain Text Draft ===
Creating draft with is_plaintext=True...
✓ Draft request prepared with is_plaintext=True
📝 Draft configured to be sent as plain text when sent

Example completed successfully!
```

## Use Cases

### Plain Text (is_plaintext=true)
- **Simple Notifications**: System alerts, password resets, account confirmations
- **Text-Only Emails**: Newsletters or announcements that don't need formatting
- **Lightweight Messaging**: Reduce message size and improve compatibility
- **Accessibility**: Better support for screen readers and text-only email clients

### HTML (is_plaintext=false)
- **Marketing Emails**: Rich formatting, images, and branded content
- **Newsletters**: Complex layouts with multiple sections and styling
- **Transactional Emails**: Formatted receipts, invoices, and reports
- **Interactive Content**: Buttons, links, and styled call-to-action elements

## Code Examples

### Send Plain Text Message
```python
message_request = {
    "to": [{"email": "user@example.com", "name": "User"}],
    "subject": "Plain Text Notification",
    "body": "This is a plain text message.",
    "is_plaintext": True
}

response = client.messages.send(
    identifier=grant_id, 
    request_body=message_request
)
```

### Send HTML Message
```python
message_request = {
    "to": [{"email": "user@example.com", "name": "User"}],
    "subject": "HTML Newsletter",
    "body": "<h1>Welcome!</h1><p>This is <strong>HTML</strong> content.</p>",
    "is_plaintext": False
}

response = client.messages.send(
    identifier=grant_id, 
    request_body=message_request
)
```

### Create Plain Text Draft
```python
draft_request = {
    "to": [{"email": "user@example.com", "name": "User"}],
    "subject": "Draft Message",
    "body": "This draft will be sent as plain text.",
    "is_plaintext": True
}

response = client.drafts.create(
    identifier=grant_id, 
    request_body=draft_request
)
```

## Important Notes

- **Backwards Compatibility**: Existing code without `is_plaintext` continues to work unchanged
- **Default Behavior**: When `is_plaintext` is not specified, it defaults to `false` (HTML)
- **Content Type**: The property affects MIME structure, not just content rendering
- **Safety**: The example includes commented API calls to prevent unintended message sends

## Error Handling

The example includes proper error handling for:
- Missing environment variables
- API authentication errors
- Invalid request parameters
- Network connectivity issues

## Documentation

For more information about the Nylas Python SDK and message properties, visit:
- [Nylas Python SDK Documentation](https://developer.nylas.com/docs/sdks/python/)
- [Nylas API Messages Reference](https://developer.nylas.com/docs/api/v3/ecc/#tag--Messages)
- [Nylas API Drafts Reference](https://developer.nylas.com/docs/api/v3/ecc/#tag--Drafts)

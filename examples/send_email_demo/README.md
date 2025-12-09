# Send Email Example

This example demonstrates how to send an email with special characters (accented letters) in the subject line using the Nylas Python SDK.

## Overview

The example sends an email with the subject **"De l'idée à la post-prod, sans friction"** to demonstrate proper handling of UTF-8 characters in email subjects.

## Prerequisites

- Python 3.8 or higher
- Nylas Python SDK installed
- Nylas API key
- Nylas grant ID
- Email address for testing

## Setup

1. Install the SDK in development mode:
   ```bash
   cd /path/to/nylas-python
   pip install -e .
   ```

2. Set the required environment variables:
   ```bash
   export NYLAS_API_KEY="your_api_key"
   export NYLAS_GRANT_ID="your_grant_id"
   export RECIPIENT_EMAIL="recipient@example.com"
   ```

## Running the Example

```bash
python examples/send_email_demo/send_email_example.py
```

## What This Example Demonstrates

- Sending an email with special characters (accented letters) in the subject
- Proper UTF-8 encoding of email subjects
- Using the `messages.send()` method to send emails directly

## Expected Output

```
============================================================
  Nylas SDK: Send Email with Special Characters Example
============================================================

This example sends an email with the subject:
  "De l'idée à la post-prod, sans friction"

Grant ID: your_grant_id
Recipient: recipient@example.com

Sending email...
  To: recipient@example.com
  Subject: De l'idée à la post-prod, sans friction

✓ Email sent successfully!
  Message ID: message-id-here
  Subject: De l'idée à la post-prod, sans friction

✅ Special characters in subject are correctly preserved

============================================================
Example completed successfully! ✅
============================================================
```

## Notes

- The SDK properly handles UTF-8 characters in email subjects and bodies
- Special characters like é, à, and other accented letters are preserved correctly
- The email will be delivered with the subject exactly as specified


# Raw MIME Send Demo

This example demonstrates how to send a message as raw RFC 822 MIME data using `messages.send_raw_mime()`.

## When to Use It

The standard `messages.send()` method builds the MIME message for you from structured fields. Use `send_raw_mime()` when you need full control over the outgoing message, for example to:

- Set headers that the structured send request doesn't expose, such as `Importance: High` and `X-Priority: 1`.
- Control the exact encoding and MIME structure of the message.
- Send a message that another system has already built as MIME.

## Usage

```python
from nylas import Client

client = Client(api_key="NYLAS_API_KEY")

mime = (
    b"MIME-Version: 1.0\r\n"
    b"From: Sender <sender@example.com>\r\n"
    b"To: Recipient <recipient@example.com>\r\n"
    b"Subject: Hello\r\n"
    b"Importance: High\r\n"
    b"X-Priority: 1\r\n"
    b"Content-Type: text/plain; charset=\"UTF-8\"\r\n"
    b"\r\n"
    b"Hello from a raw MIME message!\r\n"
)

response = client.messages.send_raw_mime(
    identifier="NYLAS_GRANT_ID",
    request_body={"mime": mime},
)
print(response.data.id)
```

`mime` can be a `str` or `bytes`. Pass `bytes` to send the message exactly as encoded. Strings are encoded as UTF-8.

The SDK sends the message to `POST /v3/grants/{grant_id}/messages/send?type=mime` as a `multipart/form-data` request, with the message in a `mime` file part.

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
export NYLAS_RECIPIENT_EMAIL="recipient@example.com"
export NYLAS_API_URI="https://api.us.nylas.com"  # Optional, defaults to US
```

## Running the Example

```bash
python examples/raw_mime_send_demo/raw_mime_send_example.py
```

The example builds a high-importance `multipart/alternative` message with Python's `email` package, then sends it with `send_raw_mime()`.

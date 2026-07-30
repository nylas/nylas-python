# Custom Tracking Hostname Example

This example shows how to set the optional `tracking_options.domain_name` field for:

- a regular grant-based message;
- a draft;
- a scheduled grant-based message; and
- a Transactional Send message.

The hostname must belong to the authenticated organization and have an active certificate. Enable `links`, `opens`, or both when you provide it. If you omit `domain_name`, Nylas keeps using its regional tracking hostname and existing request behavior is unchanged.

For Transactional Send, the two domain values are intentionally different:

- `NYLAS_TRANSACTIONAL_SENDER_DOMAIN` is the verified sender domain used in `/v3/domains/{domain_name}/messages/send`.
- `NYLAS_TRACKING_HOSTNAME` is the custom hostname serialized as `tracking_options.domain_name`.

## Setup

Install the SDK from the repository root and set the shared environment variables:

```bash
pip install -e .

export NYLAS_API_KEY="your_api_key"
export RECIPIENT_EMAIL="recipient@example.com"
export NYLAS_TRACKING_HOSTNAME="tracking.example.com"
```

For regular, draft, and scheduled grant-based operations, also set:

```bash
export NYLAS_GRANT_ID="your_grant_id"
```

For Transactional Send, use a verified sender domain and an address on that domain:

```bash
export NYLAS_TRANSACTIONAL_SENDER_DOMAIN="sender.example.com"
export SENDER_EMAIL="support@sender.example.com"
```

## Run an operation

The default operation is `regular`. Set `NYLAS_CUSTOM_TRACKING_OPERATION` to choose another:

```bash
NYLAS_CUSTOM_TRACKING_OPERATION=regular \
  python examples/custom_tracking_domain_demo/custom_tracking_domain_example.py

NYLAS_CUSTOM_TRACKING_OPERATION=draft \
  python examples/custom_tracking_domain_demo/custom_tracking_domain_example.py

NYLAS_CUSTOM_TRACKING_OPERATION=scheduled \
NYLAS_SEND_AT=1893456000 \
  python examples/custom_tracking_domain_demo/custom_tracking_domain_example.py

NYLAS_CUSTOM_TRACKING_OPERATION=transactional \
  python examples/custom_tracking_domain_demo/custom_tracking_domain_example.py
```

`NYLAS_SEND_AT` is a Unix timestamp. Scheduled messages validate the custom tracking hostname when the schedule is created and again before delivery.

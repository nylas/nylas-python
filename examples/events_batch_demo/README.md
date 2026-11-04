# Events Batch Demo

This example demonstrates how to create, update, and delete events in a single request with `events.batch()`, and how to retry the operations that failed.

Batch operations are available for Google and Microsoft grants. For other providers, the API returns a 400 error.

## Usage

```python
from nylas import Client

nylas = Client(api_key="NYLAS_API_KEY")

operations = [
    {
        "method": "create",
        "body": {
            "title": "Standup",
            "when": {"start_time": 1798794000, "end_time": 1798795800},
        },
    },
    {"method": "update", "event_id": "EVENT_ID_1", "body": {"title": "Renamed"}},
    {"method": "delete", "event_id": "EVENT_ID_2"},
]

response = nylas.events.batch(
    identifier="NYLAS_GRANT_ID",
    query_params={"calendar_id": "primary"},
    request_body={"operations": operations},
)

# response.data[i] is the result of operations[i].
for operation, result in zip(operations, response.data):
    if result.error is None:
        print(operation["method"], "succeeded with status", result.status)
    else:
        print(operation["method"], "failed:", result.status, result.error.type, result.error.message)
```

Each operation has a `method` of `create`, `update`, or `delete`:

- `create` needs a `body`. The body has the same fields as the request body of `events.create()`.
- `update` needs an `event_id` and a `body`. The body has the same fields as the request body of `events.update()`.
- `delete` needs an `event_id`.

The query parameters (`calendar_id`, `notify_participants`, `grant_email`, `tentative_as_busy`, and `select`) apply to every operation in the batch. `calendar_id` is required. An event can appear in only one operation per batch.

## Results

`response.data` has one result for each operation, in the same order as the operations. Each result has these fields:

| Field | Description |
| --- | --- |
| `status` | The HTTP status code of the operation. |
| `data` | The created or updated `Event`. `None` for delete operations and for failed operations. |
| `error` | The `type`, `message`, and `provider_error` of the error. `None` if the operation succeeded. |
| `retry_after` | The number of seconds to wait before a retry. Only set if the provider throttled the request. Can be `0`. |
| `provider_event_created` | `True` if the provider created the event before a later step failed. |

If some or all of the operations fail, the API returns HTTP 207. `events.batch()` doesn't raise an error for a 207 response. It returns the results, so check the `status` or `error` of each result.

If the request itself is invalid, the API returns HTTP 400 and runs none of the operations. For example, the request is invalid if `calendar_id` is missing, if the batch has too many operations, or if two operations use the same `event_id`. `events.batch()` then raises a `NylasApiError`, as for any other API error.

## Retrying Failed Operations

The SDK doesn't retry failed operations. Use these rules to retry them yourself:

- Retry an operation if its `status` is `429` or `503`. If `retry_after` is set, wait that number of seconds first. A `retry_after` of `0` means that you can retry now, so compare it with `None` instead of checking whether it is truthy.
- **Never** retry an operation if `provider_event_created` is `True`. The provider already created the event, so a retry creates a duplicate event.
- Send only the failed operations again. Don't send the operations that succeeded.

```python
import time

RETRYABLE_STATUSES = {429, 503}


def run_batch(nylas, grant_id, calendar_id, operations, max_attempts=3):
    """Run a batch, and retry the failed operations that are safe to retry."""
    results = [None] * len(operations)
    pending = list(range(len(operations)))

    for attempt in range(1, max_attempts + 1):
        response = nylas.events.batch(
            identifier=grant_id,
            query_params={"calendar_id": calendar_id},
            request_body={"operations": [operations[index] for index in pending]},
        )

        retry = []
        wait_seconds = 0
        for index, result in zip(pending, response.data):
            results[index] = result
            if result.error is None or result.provider_event_created:
                continue
            if result.status in RETRYABLE_STATUSES:
                retry.append(index)
                delay = 1 if result.retry_after is None else result.retry_after
                wait_seconds = max(wait_seconds, delay)

        if not retry or attempt == max_attempts:
            break
        time.sleep(wait_seconds)
        pending = retry

    return results
```

## Setup

1. Install the SDK in development mode from the repository root:
```bash
cd /path/to/nylas-python
pip install -e .
```

2. Set your environment variables:
```bash
export NYLAS_API_KEY="your_api_key"
export NYLAS_GRANT_ID="your_grant_id"            # A Google or Microsoft grant
export NYLAS_CALENDAR_ID="primary"               # Optional, defaults to primary
export NYLAS_API_URI="https://api.us.nylas.com"  # Optional, defaults to US
```

## Running the Example

```bash
python examples/events_batch_demo/events_batch_example.py
```

The example changes the calendar of the grant:

1. It creates two events one day from now, in one batch.
2. It renames one of the events. In the same batch, it deletes an event ID that doesn't exist, so the API returns HTTP 207 with one failed result.
3. It deletes both events in one batch.

# Response Headers Demo

This example demonstrates how to access and use response headers from various Nylas API responses. It shows how headers are available in different types of responses:

1. List responses (from methods like `list()`)
2. Single-item responses (from methods like `find()`)
3. Error responses (when API calls fail)

## What You'll Learn

- How to access response headers from successful API calls
- How to access headers from error responses
- Common headers you'll encounter in Nylas API responses
- How headers differ between list and single-item responses

## Headers Demonstrated

The example will show various headers that Nylas includes in responses, such as:

- `request-id`: Unique identifier for the API request
- `x-ratelimit-limit`: Your rate limit for the endpoint
- `x-ratelimit-remaining`: Remaining requests within the current window
- `x-ratelimit-reset`: When the rate limit window resets
- And more...

## Prerequisites

Before running this example, make sure you have:

1. A Nylas API key
2. A Nylas grant ID
3. Python 3.7 or later installed
4. The Nylas Python SDK installed

## Setup

1. First, install the SDK in development mode:
   ```bash
   cd /path/to/nylas-python
   pip install -e .
   ```

2. Set up your environment variables:
   ```bash
   export NYLAS_API_KEY="your_api_key"
   export NYLAS_GRANT_ID="your_grant_id"
   ```

## Running the Example

Run the example with:
```bash
python examples/response_headers_demo/response_headers_example.py
```

The script will:
1. Demonstrate headers from a list response by fetching messages
2. Show headers from a single-item response by fetching one message
3. Trigger and catch an error to show error response headers

## Example Output

You'll see output similar to this:

```
Demonstrating Response Headers
============================

Demonstrating List Response Headers
----------------------------------
✓ Successfully retrieved messages

Response Headers:
------------------------
request-id: req_abcd1234
x-ratelimit-limit: 1000
x-ratelimit-remaining: 999
...

Demonstrating Find Response Headers
----------------------------------
✓ Successfully retrieved single message

Response Headers:
------------------------
request-id: req_efgh5678
...

Demonstrating Error Response Headers
---------------------------------
✓ Successfully caught expected error
✗ Error Type: invalid_request
✗ Request ID: req_ijkl9012
✗ Status Code: 404

Error Response Headers:
------------------------
request-id: req_ijkl9012
...
```

## Error Handling

The example includes proper error handling and will show you how to:
- Catch `NylasApiError` exceptions
- Access error details and headers
- Handle different types of API errors gracefully 
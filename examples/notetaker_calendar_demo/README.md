# Notetaker Calendar Integration Demo

This demo showcases how to use the Nylas Notetaker API in conjunction with calendar and event APIs to create and manage notes associated with calendar events.

## Features Demonstrated

- Creating notes linked to calendar events
- Retrieving notes associated with events
- Managing event-related notes
- Syncing notes with event updates
- Using note metadata for event organization

## Prerequisites

- Python 3.8+
- Nylas Python SDK (local version from this repository)
- Nylas API credentials (Client ID and Client Secret)

## Setup

1. Install the SDK in development mode:
```bash
# From the root of the nylas-python repository
pip install -e .
```

2. Set up your environment variables:
```bash
export NYLAS_API_KEY='your_api_key'
export NYLAS_API_URI='https://api.nylas.com'  # Optional, defaults to https://api.nylas.com
```

## Running the Demo

From the root of the repository:
```bash
python examples/notetaker_calendar_demo/notetaker_calendar_demo.py
```

## Code Examples

The demo includes examples of:

1. Creating a calendar event with associated notes
2. Retrieving notes linked to specific events
3. Updating event notes when the event changes
4. Managing note metadata for event organization
5. Syncing notes across multiple events

Each example is documented with comments explaining the functionality and expected output. 
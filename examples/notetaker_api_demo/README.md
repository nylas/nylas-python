# Notetaker API Demo

This demo showcases how to use the Nylas Notetaker API to create, manage, and interact with notes.

## Features Demonstrated

- Creating new notes
- Retrieving notes
- Updating notes
- Deleting notes
- Managing note metadata
- Sharing notes with other users

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
python examples/notetaker_api_demo/notetaker_demo.py
```

## Code Examples

The demo includes examples of:

1. Creating a new note
2. Retrieving a list of notes
3. Updating an existing note
4. Deleting a note
5. Managing note metadata
6. Sharing notes with other users

Each example is documented with comments explaining the functionality and expected output. 
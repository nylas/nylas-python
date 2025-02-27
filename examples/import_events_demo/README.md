# Import Events Demo

This example demonstrates the usage of the `list_import_events` method in the Nylas SDK. This method returns a list of recurring events, recurring event exceptions, and single events from a specified calendar within a given time frame. It's particularly useful when you want to import, store, and synchronize events from a calendar to your application.

## Features Demonstrated

1. **Basic Usage**: Shows how to use `list_import_events` with required parameters.
2. **Time Filtering**: Demonstrates filtering events by start and end time.
3. **Pagination**: Shows how to handle paginated results with `max_results` and `page_token`.
4. **Field Selection**: Demonstrates how to use the `select` parameter to request only specific fields.
5. **Multiple Scenarios**: Shows various parameter combinations for different use cases.

## Setup

1. Create a `.env` file in the root directory with your Nylas API credentials:
   ```
   NYLAS_API_KEY=your_api_key_here
   NYLAS_GRANT_ID=your_grant_id_here
   ```

2. Install the required dependencies:
   ```bash
   pip install nylas python-dotenv
   ```

## Running the Example

Run the example script:
```bash
python examples/import_events_demo/import_events_example.py
```

The script will demonstrate different ways to use the `list_import_events` method with various parameters.

## Example Output

The script will show output similar to this:
```
=== Import Events Demo ===

Basic import (primary calendar):
Event - Title: Team Meeting, ID: abc123...

Time-filtered import (Jan 1, 2023 - Dec 31, 2023):
Event - Title: Annual Review, ID: def456...

Limited results with field selection (only id, title and when):
Event - Title: Client Call, ID: ghi789...
```

## Benefits of Using Import Events

1. **Efficient Syncing**: Easily synchronize calendar events to your application or database.
2. **Better Performance**: Using time filters and limiting results can improve performance.
3. **Selective Data**: Using the select parameter allows you to request only the fields you need.

## Available Parameters

The `list_import_events` method accepts the following parameters:

- `calendar_id` (required): Specify the calendar ID to import events from. You can use "primary" for the user's primary calendar.
- `max_results`: Maximum number of events to return in a single page.
- `start`: Filter for events starting at or after this Unix timestamp.
- `end`: Filter for events ending at or before this Unix timestamp.
- `select`: Comma-separated list of fields to return in the response.
- `limit`: Maximum number of objects to return (defaults to 50, max 200).
- `page_token`: Token for retrieving the next page of results.

For more information, refer to the [Nylas API documentation](https://developer.nylas.com/). 
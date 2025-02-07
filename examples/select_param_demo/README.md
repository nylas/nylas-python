# Select Parameter Demo

This example demonstrates the usage of the `select` query parameter across different Nylas resources. The `select` parameter allows you to specify which fields you want to receive in the API response, helping to optimize your API calls by reducing the amount of data transferred.

## Features Demonstrated

1. **Backwards Compatibility**: Shows that existing code that doesn't use the `select` parameter continues to work as expected, receiving all fields.
2. **Field Selection**: Demonstrates how to use the `select` parameter to request only specific fields for better performance.
3. **Multiple Resources**: Shows the `select` parameter working across different resources:
   - Messages
   - Calendars
   - Events
   - Drafts
   - Contacts

## Setup

1. Create a `.env` file in the root directory with your Nylas API credentials:
   ```
   NYLAS_API_KEY=your_api_key_here
   ```

2. Install the required dependencies:
   ```bash
   pip install nylas python-dotenv
   ```

## Running the Example

Run the example script:
```bash
python select_param_example.py
```

The script will demonstrate both the traditional way of fetching all fields and the new selective field fetching for each resource type.

## Example Output

The script will show output similar to this for each resource:
```
=== Messages Resource ===

Fetching messages (all fields):
Full message - Subject: Example Subject, ID: abc123...

Fetching messages with select (only id and subject):
Minimal message - Subject: Example Subject, ID: abc123...
```

## Benefits of Using Select

1. **Reduced Data Transfer**: By selecting only the fields you need, you reduce the amount of data transferred over the network.
2. **Improved Performance**: Smaller payloads mean faster API responses and less processing time.
3. **Bandwidth Optimization**: Especially useful in mobile applications or when dealing with limited bandwidth.

## Available Fields

The fields available for selection vary by resource type. Refer to the [Nylas API documentation](https://developer.nylas.com/) for a complete list of available fields for each resource type. 
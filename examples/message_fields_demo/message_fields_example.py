#!/usr/bin/env python3
"""
Nylas SDK Example: Using Message Fields (include_tracking_options and raw_mime)

This example demonstrates how to use the new 'fields' query parameter values 
'include_tracking_options' and 'raw_mime' to access message tracking data and raw MIME content.

Required Environment Variables:
    NYLAS_API_KEY: Your Nylas API key
    NYLAS_GRANT_ID: Your Nylas grant ID

Usage:
    First, install the SDK in development mode:
    cd /path/to/nylas-python
    pip install -e .

    Then set environment variables and run:
    export NYLAS_API_KEY="your_api_key"
    export NYLAS_GRANT_ID="your_grant_id"
    python examples/message_fields_demo/message_fields_example.py
"""

import os
import sys
import json
import base64
from nylas import Client
from nylas.models.messages import TrackingOptions


def get_env_or_exit(var_name: str) -> str:
    """Get an environment variable or exit if not found."""
    value = os.getenv(var_name)
    if not value:
        print(f"Error: {var_name} environment variable is required")
        sys.exit(1)
    return value


def print_separator(title: str) -> None:
    """Print a formatted section separator."""
    print(f"\n=== {title} ===")


def demonstrate_standard_fields(client: Client, grant_id: str) -> None:
    """Demonstrate backwards compatible message fetching (standard fields)."""
    print_separator("Standard Message Fetching (Backwards Compatible)")
    
    try:
        print("Fetching messages with standard fields...")
        messages = client.messages.list(
            identifier=grant_id,
            query_params={"limit": 2}
        )
        
        if not messages.data:
            print("⚠️  No messages found in this account")
            return
            
        print(f"✓ Found {len(messages.data)} messages with standard payload")
        
        for i, message in enumerate(messages.data, 1):
            print(f"\nMessage {i}:")
            print(f"  ID: {message.id}")
            print(f"  Subject: {message.subject or 'No subject'}")
            print(f"  From: {message.from_[0].email if message.from_ else 'Unknown'}")
            print(f"  Tracking Options: {message.tracking_options}")  # Should be None
            print(f"  Raw MIME: {message.raw_mime}")  # Should be None
            
    except Exception as e:
        print(f"❌ Error fetching standard messages: {e}")


def demonstrate_tracking_options(client: Client, grant_id: str) -> None:
    """Demonstrate fetching messages with tracking options."""
    print_separator("Include Tracking Options")
    
    try:
        print("Fetching messages with tracking options...")
        messages = client.messages.list(
            identifier=grant_id,
            query_params={
                "limit": 2,
                "fields": "include_tracking_options"
            }
        )
        
        if not messages.data:
            print("⚠️  No messages found in this account")
            return
            
        print(f"✓ Found {len(messages.data)} messages with tracking data")
        
        for i, message in enumerate(messages.data, 1):
            print(f"\nMessage {i}:")
            print(f"  ID: {message.id}")
            print(f"  Subject: {message.subject or 'No subject'}")
            
            if message.tracking_options:
                print(f"  Tracking Options:")
                print(f"    Opens: {message.tracking_options.opens}")
                print(f"    Thread Replies: {message.tracking_options.thread_replies}")
                print(f"    Links: {message.tracking_options.links}")
                print(f"    Label: {message.tracking_options.label}")
            else:
                print("  Tracking Options: None (tracking not enabled for this message)")
                
    except Exception as e:
        print(f"❌ Error fetching messages with tracking options: {e}")


def demonstrate_raw_mime(client: Client, grant_id: str) -> None:
    """Demonstrate fetching messages with raw MIME content."""
    print_separator("Raw MIME Content")
    
    try:
        print("Fetching messages with raw MIME data...")
        messages = client.messages.list(
            identifier=grant_id,
            query_params={
                "limit": 2,
                "fields": "raw_mime"
            }
        )
        
        if not messages.data:
            print("⚠️  No messages found in this account")
            return
            
        print(f"✓ Found {len(messages.data)} messages with raw MIME content")
        
        for i, message in enumerate(messages.data, 1):
            print(f"\nMessage {i}:")
            print(f"  ID: {message.id}")
            print(f"  Grant ID: {message.grant_id}")
            print(f"  Object: {message.object}")
            
            if message.raw_mime:
                print(f"  Raw MIME length: {len(message.raw_mime)} characters")
                
                # Decode a small portion to show it's real MIME data
                try:
                    # Show first 200 characters of decoded MIME
                    decoded_sample = base64.urlsafe_b64decode(
                        message.raw_mime + '=' * (4 - len(message.raw_mime) % 4)
                    ).decode('utf-8', errors='ignore')[:200]
                    print(f"  MIME preview: {decoded_sample}...")
                except Exception as decode_error:
                    print(f"  MIME preview: Unable to decode preview ({decode_error})")
            else:
                print("  Raw MIME: None")
                
            # Note: In raw_mime mode, most other fields should be None
            print(f"  Subject (should be None): {message.subject}")
            print(f"  Body (should be None): {getattr(message, 'body', 'N/A')}")
            
    except Exception as e:
        print(f"❌ Error fetching messages with raw MIME: {e}")


def demonstrate_single_message_fields(client: Client, grant_id: str) -> None:
    """Demonstrate fetching a single message with different field options."""
    print_separator("Single Message with Different Fields")
    
    try:
        # First get a message ID
        print("Finding a message to demonstrate single message field options...")
        messages = client.messages.list(
            identifier=grant_id,
            query_params={"limit": 1}
        )
        
        if not messages.data:
            print("⚠️  No messages found for single message demo")
            return
            
        message_id = messages.data[0].id
        print(f"Using message ID: {message_id}")
        
        # Fetch with tracking options
        print("\nFetching single message with tracking options...")
        message = client.messages.find(
            identifier=grant_id,
            message_id=message_id,
            query_params={"fields": "include_tracking_options"}
        )
        
        print(f"✓ Message fetched with tracking: {message.tracking_options is not None}")
        
        # Fetch with raw MIME
        print("\nFetching single message with raw MIME...")
        message = client.messages.find(
            identifier=grant_id,
            message_id=message_id,
            query_params={"fields": "raw_mime"}
        )
        
        print(f"✓ Message fetched with raw MIME: {message.raw_mime is not None}")
        if message.raw_mime:
            print(f"  Raw MIME size: {len(message.raw_mime)} characters")
            
    except Exception as e:
        print(f"❌ Error in single message demo: {e}")


def demonstrate_tracking_options_model() -> None:
    """Demonstrate working with the TrackingOptions model directly."""
    print_separator("TrackingOptions Model Demo")
    
    try:
        print("Creating TrackingOptions object...")
        
        # Create a TrackingOptions instance
        tracking = TrackingOptions(
            opens=True,
            thread_replies=False,
            links=True,
            label="Marketing Campaign Demo"
        )
        
        print("✓ TrackingOptions created:")
        print(f"  Opens: {tracking.opens}")
        print(f"  Thread Replies: {tracking.thread_replies}")
        print(f"  Links: {tracking.links}")
        print(f"  Label: {tracking.label}")
        
        # Demonstrate serialization
        print("\nSerializing to dict...")
        tracking_dict = tracking.to_dict()
        print(f"✓ Serialized: {json.dumps(tracking_dict, indent=2)}")
        
        # Demonstrate deserialization
        print("\nDeserializing from dict...")
        restored_tracking = TrackingOptions.from_dict(tracking_dict)
        print(f"✓ Deserialized: opens={restored_tracking.opens}, label='{restored_tracking.label}'")
        
        # Demonstrate JSON serialization
        print("\nJSON serialization...")
        tracking_json = tracking.to_json()
        print(f"✓ JSON: {tracking_json}")
        
        restored_from_json = TrackingOptions.from_json(tracking_json)
        print(f"✓ From JSON: {restored_from_json.to_dict()}")
        
    except Exception as e:
        print(f"❌ Error in TrackingOptions demo: {e}")


def main():
    """Main function demonstrating message fields usage."""
    # Get required environment variables
    api_key = get_env_or_exit("NYLAS_API_KEY")
    grant_id = get_env_or_exit("NYLAS_GRANT_ID")

    # Initialize Nylas client
    client = Client(api_key=api_key)

    print("Demonstrating Message Fields Usage")
    print("=================================")
    print("This shows the new 'include_tracking_options' and 'raw_mime' field options")

    # Demonstrate different field options
    demonstrate_standard_fields(client, grant_id)
    demonstrate_tracking_options(client, grant_id)
    demonstrate_raw_mime(client, grant_id)
    demonstrate_single_message_fields(client, grant_id)
    demonstrate_tracking_options_model()

    print("\n" + "="*50)
    print("Example completed successfully!")
    print("="*50)


if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Nylas SDK Example: Using is_plaintext for Messages and Drafts

This example demonstrates how to use the new 'is_plaintext' property when sending 
messages and creating drafts to control whether content is sent as plain text or HTML.

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
    python examples/is_plaintext_demo/is_plaintext_example.py
"""

import os
import sys
from nylas import Client


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


def demonstrate_plaintext_message(client: Client, grant_id: str) -> None:
    """Demonstrate sending a message with is_plaintext=True."""
    print_separator("Sending Plain Text Message")
    
    try:
        print("Sending message with is_plaintext=True...")
        
        # Example message content with HTML tags that will be sent as plain text
        body_content = """Hello World!

This is a test message sent as plain text.
Even if this contained <strong>HTML tags</strong>, they would be sent as plain text.

Best regards,
The Nylas SDK Team"""

        # Send message with is_plaintext=True
        message_request = {
            "to": [{"email": "test@example.com", "name": "Test Recipient"}],
            "subject": "Plain Text Message Example",
            "body": body_content,
            "is_plaintext": True
        }
        
        print("✓ Message request prepared with is_plaintext=True")
        print(f"  Subject: {message_request['subject']}")
        print(f"  Body preview: {body_content[:100]}...")
        print(f"  is_plaintext: {message_request['is_plaintext']}")
        
        # Note: Uncomment the following line to actually send the message
        # response = client.messages.send(identifier=grant_id, request_body=message_request)
        # print(f"✓ Message sent! ID: {response.data.id}")
        
        print("📧 Message configured to be sent as plain text (MIME without HTML version)")
        
    except Exception as e:
        print(f"❌ Error sending plain text message: {e}")


def demonstrate_html_message(client: Client, grant_id: str) -> None:
    """Demonstrate sending a message with is_plaintext=False (HTML)."""
    print_separator("Sending HTML Message")
    
    try:
        print("Sending message with is_plaintext=False (HTML)...")
        
        # Example message content with HTML formatting
        body_content = """<html>
<body>
    <h1>Hello World!</h1>
    
    <p>This is a test message sent as <strong>HTML</strong>.</p>
    
    <p>The HTML tags will be properly rendered:</p>
    <ul>
        <li><em>Emphasized text</em></li>
        <li><strong>Bold text</strong></li>
        <li><a href="https://nylas.com">Links to Nylas</a></li>
    </ul>
    
    <p>Best regards,<br>
    <strong>The Nylas SDK Team</strong></p>
</body>
</html>"""

        # Send message with is_plaintext=False (default behavior)
        message_request = {
            "to": [{"email": "test@example.com", "name": "Test Recipient"}],
            "subject": "HTML Message Example",
            "body": body_content,
            "is_plaintext": False
        }
        
        print("✓ Message request prepared with is_plaintext=False")
        print(f"  Subject: {message_request['subject']}")
        print(f"  HTML body includes formatting tags")
        print(f"  is_plaintext: {message_request['is_plaintext']}")
        
        # Note: Uncomment the following line to actually send the message
        # response = client.messages.send(identifier=grant_id, request_body=message_request)
        # print(f"✓ Message sent! ID: {response.data.id}")
        
        print("🌐 Message configured to be sent as HTML (MIME includes HTML version)")
        
    except Exception as e:
        print(f"❌ Error sending HTML message: {e}")


def demonstrate_backwards_compatibility(client: Client, grant_id: str) -> None:
    """Demonstrate that existing code without is_plaintext still works."""
    print_separator("Backwards Compatibility (No is_plaintext specified)")
    
    try:
        print("Sending message without is_plaintext property...")
        
        # Traditional message request without is_plaintext
        message_request = {
            "to": [{"email": "test@example.com", "name": "Test Recipient"}],
            "subject": "Traditional Message Example",
            "body": "This message doesn't specify is_plaintext, so it uses the default behavior."
        }
        
        print("✓ Message request prepared without is_plaintext property")
        print(f"  Subject: {message_request['subject']}")
        print(f"  Body: {message_request['body']}")
        print(f"  is_plaintext: Not specified (uses API default)")
        
        # Note: Uncomment the following line to actually send the message
        # response = client.messages.send(identifier=grant_id, request_body=message_request)
        # print(f"✓ Message sent! ID: {response.data.id}")
        
        print("✓ Existing code continues to work without modification")
        
    except Exception as e:
        print(f"❌ Error sending traditional message: {e}")


def demonstrate_plaintext_draft(client: Client, grant_id: str) -> None:
    """Demonstrate creating a draft with is_plaintext=True."""
    print_separator("Creating Plain Text Draft")
    
    try:
        print("Creating draft with is_plaintext=True...")
        
        draft_request = {
            "to": [{"email": "test@example.com", "name": "Test Recipient"}],
            "subject": "Plain Text Draft Example", 
            "body": "This is a draft that will be sent as plain text when sent.",
            "is_plaintext": True
        }
        
        print("✓ Draft request prepared with is_plaintext=True")
        print(f"  Subject: {draft_request['subject']}")
        print(f"  Body: {draft_request['body']}")
        print(f"  is_plaintext: {draft_request['is_plaintext']}")
        
        # Note: Uncomment the following lines to actually create the draft
        # response = client.drafts.create(identifier=grant_id, request_body=draft_request)
        # print(f"✓ Draft created! ID: {response.data.id}")
        
        print("📝 Draft configured to be sent as plain text when sent")
        
    except Exception as e:
        print(f"❌ Error creating plain text draft: {e}")


def demonstrate_html_draft(client: Client, grant_id: str) -> None:
    """Demonstrate creating a draft with is_plaintext=False."""
    print_separator("Creating HTML Draft")
    
    try:
        print("Creating draft with is_plaintext=False...")
        
        html_body = """<html>
<body>
    <h2>Draft Message</h2>
    <p>This is a <strong>draft</strong> with <em>HTML formatting</em>.</p>
    <p>It will include HTML in the MIME data when sent.</p>
</body>
</html>"""

        draft_request = {
            "to": [{"email": "test@example.com", "name": "Test Recipient"}],
            "subject": "HTML Draft Example",
            "body": html_body,
            "is_plaintext": False
        }
        
        print("✓ Draft request prepared with is_plaintext=False")
        print(f"  Subject: {draft_request['subject']}")
        print(f"  HTML body includes formatting")
        print(f"  is_plaintext: {draft_request['is_plaintext']}")
        
        # Note: Uncomment the following lines to actually create the draft
        # response = client.drafts.create(identifier=grant_id, request_body=draft_request)
        # print(f"✓ Draft created! ID: {response.data.id}")
        
        print("📝 Draft configured to be sent as HTML when sent")
        
    except Exception as e:
        print(f"❌ Error creating HTML draft: {e}")


def demonstrate_draft_update(client: Client, grant_id: str) -> None:
    """Demonstrate updating a draft with is_plaintext property."""
    print_separator("Updating Draft with is_plaintext")
    
    try:
        print("Demonstrating draft update with is_plaintext...")
        
        # Example update request
        update_request = {
            "subject": "Updated Draft with Plain Text",
            "body": "This draft has been updated to use plain text format.",
            "is_plaintext": True
        }
        
        print("✓ Draft update request prepared with is_plaintext=True")
        print(f"  Updated subject: {update_request['subject']}")
        print(f"  Updated body: {update_request['body']}")
        print(f"  is_plaintext: {update_request['is_plaintext']}")
        
        # Note: Uncomment the following lines to actually update a draft
        # draft_id = "your_draft_id_here"
        # response = client.drafts.update(
        #     identifier=grant_id, 
        #     draft_id=draft_id, 
        #     request_body=update_request
        # )
        # print(f"✓ Draft updated! ID: {response.data.id}")
        
        print("📝 Draft update includes is_plaintext configuration")
        
    except Exception as e:
        print(f"❌ Error updating draft: {e}")


def main():
    """Main function demonstrating is_plaintext usage."""
    # Get required environment variables
    api_key = get_env_or_exit("NYLAS_API_KEY")
    grant_id = get_env_or_exit("NYLAS_GRANT_ID")

    # Initialize Nylas client
    client = Client(api_key=api_key)

    print("Demonstrating is_plaintext Property Usage")
    print("=======================================")
    print("This shows the new 'is_plaintext' property for messages and drafts")
    print("Note: Actual API calls are commented out to prevent unintended sends")

    # Demonstrate message sending with different is_plaintext values
    demonstrate_plaintext_message(client, grant_id)
    demonstrate_html_message(client, grant_id)
    demonstrate_backwards_compatibility(client, grant_id)
    
    # Demonstrate draft creation and updating with is_plaintext
    demonstrate_plaintext_draft(client, grant_id)
    demonstrate_html_draft(client, grant_id)
    demonstrate_draft_update(client, grant_id)

    print("\n" + "="*60)
    print("Example completed successfully!")
    print("="*60)
    print("\n💡 Key Takeaways:")
    print("• is_plaintext=True: Sends content as plain text (no HTML in MIME)")
    print("• is_plaintext=False: Sends content as HTML (includes HTML in MIME)")
    print("• Not specified: Uses API default behavior (backwards compatible)")
    print("• Available in: messages.send(), drafts.create(), drafts.update()")


if __name__ == "__main__":
    main()

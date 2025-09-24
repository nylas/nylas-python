#!/usr/bin/env python3

import io
import os
from nylas import Client


def send_message_with_inline_attachment():
    """
    This example demonstrates how to send a message with an inline attachment
    that uses a content_id for referencing in HTML email bodies.
    
    This is particularly useful for embedding images directly in HTML emails
    where the image is referenced using 'cid:' in the src attribute.
    """
    
    # Initialize the Nylas client
    nylas = Client(
        api_key=os.environ.get("NYLAS_API_KEY"),  # Replace with your API key
    )
    
    # Create a sample image content (you would typically read from a file)
    # For demonstration, we'll create a small PNG-like binary data
    image_content = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\nIDATx\x9cc\xf8\x00\x00\x00\x01\x00\x01\x00\x00\x00\x00IEND\xaeB`\x82'
    
    # Create the message with inline attachment
    message_request = {
        "to": [{"email": "recipient@example.com", "name": "Recipient Name"}],
        "from": [{"email": "sender@example.com", "name": "Sender Name"}],
        "subject": "Message with Inline Image",
        "body": """
        <html>
        <body>
            <h1>Hello!</h1>
            <p>This email contains an inline image:</p>
            <img src="cid:my-inline-image" alt="Inline Image" style="max-width: 200px;">
            <p>The image above is embedded directly in the email using content_id.</p>
        </body>
        </html>
        """,
        "attachments": [
            {
                "filename": "inline-image.png",
                "content_type": "image/png",
                "content": io.BytesIO(image_content),
                "size": len(image_content),
                "content_id": "my-inline-image",  # This is the key for inline attachments
                "is_inline": True,
                "content_disposition": "inline"
            },
            {
                # Regular attachment without content_id for comparison
                "filename": "regular-attachment.txt",
                "content_type": "text/plain",
                "content": io.BytesIO(b"This is a regular attachment"),
                "size": 28,
                # No content_id - this will use the default file{index} naming
            }
        ]
    }
    
    try:
        # Send the message
        response = nylas.messages.send(
            identifier="your-grant-id",  # Replace with your grant ID
            request_body=message_request
        )
        
        print("Message sent successfully!")
        print(f"Message ID: {response.data.id}")
        print(f"Thread ID: {response.data.thread_id}")
        
        # The inline attachment will be referenced by its content_id in the form data
        # instead of a generic file{index} name, allowing proper inline display
        
    except Exception as e:
        print(f"Error sending message: {e}")


def send_draft_with_inline_attachment():
    """
    This example demonstrates how to create and send a draft with an inline attachment.
    """
    
    # Initialize the Nylas client
    nylas = Client(
        api_key=os.environ.get("NYLAS_API_KEY"),  # Replace with your API key
    )
    
    # Create a larger image content to trigger form data usage (>3MB threshold)
    # For demo purposes, we'll create a smaller example but in real usage,
    # large images would automatically use the content_id functionality
    large_image_content = b'LARGE_IMAGE_DATA_PLACEHOLDER' * 1000  # Simulated large content
    
    # Create the draft with inline attachment
    draft_request = {
        "to": [{"email": "recipient@example.com", "name": "Recipient Name"}],
        "from": [{"email": "sender@example.com", "name": "Sender Name"}],
        "subject": "Draft with Inline Image",
        "body": """
        <html>
        <body>
            <h1>Draft Email</h1>
            <p>This draft contains an inline image:</p>
            <img src="cid:logo-image" alt="Company Logo" style="max-width: 300px;">
            <p>Best regards,<br>Your Team</p>
        </body>
        </html>
        """,
        "attachments": [
            {
                "filename": "company-logo.png",
                "content_type": "image/png",
                "content": io.BytesIO(large_image_content),
                "size": len(large_image_content),
                "content_id": "logo-image",  # Content ID for inline reference
                "is_inline": True,
                "content_disposition": "inline"
            }
        ]
    }
    
    try:
        # Create the draft
        draft_response = nylas.drafts.create(
            identifier="your-grant-id",  # Replace with your grant ID
            request_body=draft_request
        )
        
        print("Draft created successfully!")
        print(f"Draft ID: {draft_response.data.id}")
        
        # Send the draft
        send_response = nylas.drafts.send(
            identifier="your-grant-id",  # Replace with your grant ID
            draft_id=draft_response.data.id
        )
        
        print("Draft sent successfully!")
        print(f"Message ID: {send_response.data.id}")
        
    except Exception as e:
        print(f"Error with draft: {e}")


if __name__ == "__main__":
    print("Inline Attachment Example")
    print("=" * 50)
    print()
    
    # Check if API key is set
    if not os.environ.get("NYLAS_API_KEY"):
        print("Please set the NYLAS_API_KEY environment variable")
        print("export NYLAS_API_KEY='your-api-key-here'")
        exit(1)
    
    print("1. Sending message with inline attachment...")
    send_message_with_inline_attachment()
    
    print("\n2. Creating and sending draft with inline attachment...")
    send_draft_with_inline_attachment()
    
    print("\nNote: The content_id field ensures that large inline attachments")
    print("are properly referenced in the multipart form data, allowing")
    print("email clients to display them inline correctly.")

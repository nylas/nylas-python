#!/usr/bin/env python3

import base64
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

    # Get test email
    test_email = os.environ.get("TEST_EMAIL")

    # Get grant
    grant_id = os.environ.get("NYLAS_GRANT_ID")
    
    # Create a sample image content using base64 decoded data
    # This is a small PNG image that can be used for demonstration
    base64_image = "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAEQUlEQVRYhe2WW2wUVRyHv5nZS7vb3XbLdrfXjSZ9AxOqDRANGjDRSKLRKoIYNLENpEgJRQIKKvSi0tI28oImhtISqg9cTEzUhIgmSkAQY4UWQ2yALi3d7S4UaPcyO7MzPkwlJXG3S02sD5yH8zLJ//vO7/zPmSMsqR0MMIvDBHhnU0CcTfh9gf+FgOnfFlCTIKs6mg6iABaTgFn6DwQ0DUYnNBaVW3iyMpvcHImJmMaPvTG+75PxOkSkDPKdkUBC1bFZRb76sIhyn/WubyufyePaqEJdW5DAWBKrWUhb6557QFZ13E6Jb/eUUe6zcuzkOMu3DlG0/DLPbrrKl8dvUewxc6S1lJI5EqqWvp6wpHZQzxiu6HjyJI60lCKKsLkjwI1xjfdr3PiKLYyMKnQcvE7oVpIDjSWEx1QW1w1R5Ey9zowTkBUd7xR4fVsAm1Wgc0cxD5RY6P8zRrHHTPtbhZS6TXzxzU3cLhNVC7NJqKnXmJGArOgUuiQOtxrwjbsDOG0ijW96kRM6T2+4yorGIAuqB1FUnc2vu9lz9BYAC+ZmkVBT155WQFZ0ilwSh1tKEQXY0DqCK0ekYZ2HeEJn6Xo/t6MahU6RuKJztj9Kfq7EwA1j8y1mkXR7nFZASeoU50scai1FEKCuZQS3U2JHrYe4rLGgZpDmmjn4CiRkVcdmFaica2PsdpLyfKN0QtFIdw5SHkNdB6tZ4FBLKQDrd43gdUm8t9ZDTNaorPbzycYCHq+0Y8sSWdMe4sTeMswmgd1dYTZU5QJwpj+OJc1hT5uApsGAX6Zu1wiF+ZPwuMbD1X4+rTfgv5yPUtUU5MTeMhx2kY4DYQaDKquW5REeUzl6OobFlDqDlAKCYKSwuP4aZV4T767xEI1rVFT7+WxTAYsfsXPmfJTnGoL07fPhsIu0d4c5e1Gm54MSANa1BCiwp2+ztDfheFxny/MO6le7icY0Kmr8dG4u4LEKO6fPRXmhKciFTh8up8TurjC9AzKfT8Jf3T7M0PUkWdPchCkFlCQ8Mc9K/Wo3kZix8q4tBTw6387Pv0d4sXmUC50+8hwSrftDnLuUoKfZgK/aPszlUZXsaeCQZgskEa4EVH76NcKitX66txrwU70RXpoCb+kM0XcpwcEmA/7KtmGuZAhPm4AoQHhcY1lTkO+aCln4kI2Tv0VY8dEo/ft95OZI7NoX4o/BBAcm4Su3DeMPqdPGnpEAQHhC44fmQirnGfA32kL0d/pw5hixX7qm0N1owFe8M8TV8PR7nrFARNZpeM1lwHsjPLUzyLGdXpw5Em3dYT7+eoLjrUUAvPz2UEYN908j5d8woeosnZ/N3ActNPTcxOMQybOJlHkkTl1M4MgSUJNGryQ1HbN07/C0An9LKEmwW43img5JjTtPLn1yEmbGBqbpAYtJuOsaFQUQp7z3hDvTzMesv4rvC8y6gAmIzKbAX+u0pDGsEb6KAAAAAElFTkSuQmCC"
    image_content = base64.b64decode(base64_image)
    
    # Create the message with inline attachment
    message_request = {
        "to": [{"email": test_email, "name": "Recipient Name"}],
        "from": [{"email": test_email, "name": "Sender Name"}],
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
            identifier=grant_id,  # Replace with your grant ID
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
    
    # Get test email
    test_email = os.environ.get("TEST_EMAIL")

    # Get grant
    grant_id = os.environ.get("NYLAS_GRANT_ID")
    
    # Create a larger image content to trigger form data usage (>3MB threshold)
    # For demo purposes, we'll replicate the same image data multiple times
    # In real usage, large images would automatically use the content_id functionality
    base64_image = "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAEQUlEQVRYhe2WW2wUVRyHv5nZS7vb3XbLdrfXjSZ9AxOqDRANGjDRSKLRKoIYNLENpEgJRQIKKvSi0tI28oImhtISqg9cTEzUhIgmSkAQY4UWQ2yALi3d7S4UaPcyO7MzPkwlJXG3S02sD5yH8zLJ//vO7/zPmSMsqR0MMIvDBHhnU0CcTfh9gf+FgOnfFlCTIKs6mg6iABaTgFn6DwQ0DUYnNBaVW3iyMpvcHImJmMaPvTG+75PxOkSkDPKdkUBC1bFZRb76sIhyn/WubyufyePaqEJdW5DAWBKrWUhb6557QFZ13E6Jb/eUUe6zcuzkOMu3DlG0/DLPbrrKl8dvUewxc6S1lJI5EqqWvp6wpHZQzxiu6HjyJI60lCKKsLkjwI1xjfdr3PiKLYyMKnQcvE7oVpIDjSWEx1QW1w1R5Ey9zowTkBUd7xR4fVsAm1Wgc0cxD5RY6P8zRrHHTPtbhZS6TXzxzU3cLhNVC7NJqKnXmJGArOgUuiQOtxrwjbsDOG0ijW96kRM6T2+4yorGIAuqB1FUnc2vu9lz9BYAC+ZmkVBT155WQFZ0ilwSh1tKEQXY0DqCK0ekYZ2HeEJn6Xo/t6MahU6RuKJztj9Kfq7EwA1j8y1mkXR7nFZASeoU50scai1FEKCuZQS3U2JHrYe4rLGgZpDmmjn4CiRkVcdmFaica2PsdpLyfKN0QtFIdw5SHkNdB6tZ4FBLKQDrd43gdUm8t9ZDTNaorPbzycYCHq+0Y8sSWdMe4sTeMswmgd1dYTZU5QJwpj+OJc1hT5uApsGAX6Zu1wiF+ZPwuMbD1X4+rTfgv5yPUtUU5MTeMhx2kY4DYQaDKquW5REeUzl6OobFlDqDlAKCYKSwuP4aZV4T767xEI1rVFT7+WxTAYsfsXPmfJTnGoL07fPhsIu0d4c5e1Gm54MSANa1BCiwp2+ztDfheFxny/MO6le7icY0Kmr8dG4u4LEKO6fPRXmhKciFTh8up8TurjC9AzKfT8Jf3T7M0PUkWdPchCkFlCQ8Mc9K/Wo3kZix8q4tBTw6387Pv0d4sXmUC50+8hwSrftDnLuUoKfZgK/aPszlUZXsaeCQZgskEa4EVH76NcKitX66txrwU70RXpoCb+kM0XcpwcEmA/7KtmGuZAhPm4AoQHhcY1lTkO+aCln4kI2Tv0VY8dEo/ft95OZI7NoX4o/BBAcm4Su3DeMPqdPGnpEAQHhC44fmQirnGfA32kL0d/pw5hixX7qm0N1owFe8M8TV8PR7nrFARNZpeM1lwHsjPLUzyLGdXpw5Em3dYT7+eoLjrUUAvPz2UEYN908j5d8woeosnZ/N3ActNPTcxOMQybOJlHkkTl1M4MgSUJNGryQ1HbN07/C0An9LKEmwW43img5JjTtPLn1yEmbGBqbpAYtJuOsaFQUQp7z3hDvTzMesv4rvC8y6gAmIzKbAX+u0pDGsEb6KAAAAAElFTkSuQmCC"
    large_image_content = base64.b64decode(base64_image) * 1000  # Replicated to make it large
    
    # Create the draft with inline attachment
    draft_request = {
        "to": [{"email": test_email, "name": "Recipient Name"}],
        "from": [{"email": test_email, "name": "Sender Name"}],
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
            identifier=grant_id,  # Replace with your grant ID
            request_body=draft_request
        )
        
        print("Draft created successfully!")
        print(f"Draft ID: {draft_response.data.id}")
        
        # Send the draft
        send_response = nylas.drafts.send(
            identifier=grant_id,  # Replace with your grant ID
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
    
    # Check if grant ID is set
    if not os.environ.get("NYLAS_GRANT_ID"):
        print("Please set the NYLAS_GRANT_ID environment variable")
        print("export NYLAS_GRANT_ID='your-grant-id-here'")
        exit(1)
    
    # Check if test email is set
    if not os.environ.get("TEST_EMAIL"):
        print("Please set the TEST_EMAIL environment variable")
        print("export TEST_EMAIL='your-test-email-here'")
        exit(1)
    
    print("1. Sending message with inline attachment...")
    send_message_with_inline_attachment()
    
    print("\n2. Creating and sending draft with inline attachment...")
    send_draft_with_inline_attachment()
    
    print("\nNote: The content_id field ensures that large inline attachments")
    print("are properly referenced in the multipart form data, allowing")
    print("email clients to display them inline correctly.")

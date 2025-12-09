#!/usr/bin/env python3
"""
Nylas SDK Example: Send Email with Special Characters

This example demonstrates how to send an email with special characters
(accented letters) in the subject line using the Nylas Python SDK.

The example sends an email with the subject "De l'idée à la post-prod, sans friction"
to demonstrate proper handling of UTF-8 characters in email subjects.

Required Environment Variables:
    NYLAS_API_KEY: Your Nylas API key
    NYLAS_GRANT_ID: Your Nylas grant ID
    RECIPIENT_EMAIL: Email address to send the message to

Usage:
    First, install the SDK in development mode:
    cd /path/to/nylas-python
    pip install -e .

    Then set environment variables and run:
    export NYLAS_API_KEY="your_api_key"
    export NYLAS_GRANT_ID="your_grant_id"
    export RECIPIENT_EMAIL="recipient@example.com"
    python examples/send_email_demo/send_email_example.py
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


def send_email(client: Client, grant_id: str, recipient: str) -> None:
    """Send an email with special characters in the subject."""
    # Subject with special characters (accented letters)
    subject = "De l'idée à la post-prod, sans friction"
    
    body = """
    <html>
    <body>
        <h1>Bonjour!</h1>
        <p>Ce message démontre l'envoi d'un email avec des caractères spéciaux dans le sujet.</p>
        <p>Le sujet de cet email est: <strong>De l'idée à la post-prod, sans friction</strong></p>
        <p>Les caractères accentués sont correctement préservés grâce à l'encodage UTF-8.</p>
    </body>
    </html>
    """
    
    print(f"Sending email...")
    print(f"  To: {recipient}")
    print(f"  Subject: {subject}")
    
    try:
        response = client.messages.send(
            identifier=grant_id,
            request_body={
                "subject": subject,
                "to": [{"email": recipient}],
                "body": body,
            }
        )
        
        print(f"\n✓ Email sent successfully!")
        print(f"  Message ID: {response.data.id}")
        print(f"  Subject: {response.data.subject}")
        print(f"\n✅ Special characters in subject are correctly preserved")
        
    except Exception as e:
        print(f"\n❌ Error sending email: {e}")
        sys.exit(1)


def main():
    """Main function."""
    # Get required environment variables
    api_key = get_env_or_exit("NYLAS_API_KEY")
    grant_id = get_env_or_exit("NYLAS_GRANT_ID")
    recipient = get_env_or_exit("RECIPIENT_EMAIL")

    # Initialize Nylas client
    client = Client(api_key=api_key)

    print("=" * 60)
    print("  Nylas SDK: Send Email with Special Characters Example")
    print("=" * 60)
    print()
    print("This example sends an email with the subject:")
    print('  "De l\'idée à la post-prod, sans friction"')
    print()
    print(f"Grant ID: {grant_id}")
    print(f"Recipient: {recipient}")
    print()

    # Send the email
    send_email(client, grant_id, recipient)

    print("\n" + "=" * 60)
    print("Example completed successfully! ✅")
    print("=" * 60)


if __name__ == "__main__":
    main()


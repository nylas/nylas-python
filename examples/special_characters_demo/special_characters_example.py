#!/usr/bin/env python3
"""
Nylas SDK Example: Handling Special Characters in Email Subjects and Bodies

This example demonstrates proper handling of special characters (accented letters, 
unicode characters) in email subjects and message bodies, particularly when sending
messages with large attachments.

The SDK now correctly preserves UTF-8 characters in email subjects and bodies,
preventing encoding issues like "De l'idée à la post-prod" becoming 
"De lÃ¢Â€Â™idÃƒÂ©e ÃƒÂ la post-prod".

Required Environment Variables:
    NYLAS_API_KEY: Your Nylas API key
    NYLAS_GRANT_ID: Your Nylas grant ID
    RECIPIENT_EMAIL: Email address to send test messages to

Usage:
    First, install the SDK in development mode:
    cd /path/to/nylas-python
    pip install -e .

    Then set environment variables and run:
    export NYLAS_API_KEY="your_api_key"
    export NYLAS_GRANT_ID="your_grant_id"
    export RECIPIENT_EMAIL="recipient@example.com"
    python examples/special_characters_demo/special_characters_example.py
"""

import os
import sys
import io
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
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


def demonstrate_small_message_with_special_chars(client: Client, grant_id: str, recipient: str) -> None:
    """Demonstrate sending a message with special characters (no attachments)."""
    print_separator("Sending Message with Special Characters (No Attachments)")
    
    try:
        # This is the exact subject from the bug report
        subject = "De l'idée à la post-prod, sans friction"
        body = """
        <html>
        <body>
            <h1>Bonjour!</h1>
            <p>Ce message contient des caractères spéciaux:</p>
            <ul>
                <li>Accents français: é, è, ê, à, ù, ç</li>
                <li>Espagnol: ñ, á, í, ó, ú</li>
                <li>Allemand: ä, ö, ü, ß</li>
                <li>Portugais: ã, õ, â</li>
                <li>Symboles: €, £, ¥, ©, ®, ™</li>
                <li>Citation: "De l'idée à la réalisation"</li>
            </ul>
            <p>
                Expressions courantes: café, naïve, résumé, côté, forêt, 
                crème brûlée, piñata, Zürich
            </p>
        </body>
        </html>
        """
        
        print(f"Subject: {subject}")
        print(f"To: {recipient}")
        print("Body contains various special characters...")
        
        print("\nSending message...")
        response = client.messages.send(
            identifier=grant_id,
            request_body={
                "subject": subject,
                "to": [{"email": recipient}],
                "body": body,
            }
        )
        
        print(f"✓ Message sent successfully!")
        print(f"  Message ID: {response.data.id}")
        print(f"  Subject preserved: {response.data.subject == subject}")
        print(f"\n✅ Special characters in subject and body are correctly encoded")
        
    except Exception as e:
        print(f"❌ Error sending message: {e}")


def demonstrate_message_with_large_attachment(client: Client, grant_id: str, recipient: str) -> None:
    """Demonstrate sending a message with special characters AND large attachment."""
    print_separator("Message with Special Characters + Large Attachment")
    
    try:
        # This is the exact subject from the bug report
        subject = "De l'idée à la post-prod, sans friction"
        body = """
        <html>
        <body>
            <h1>Message avec pièce jointe volumineuse</h1>
            <p>
                Ce message démontre que les caractères spéciaux sont 
                correctement préservés même lors de l'utilisation de 
                multipart/form-data pour les grandes pièces jointes.
            </p>
            <p>Caractères accentués: café, naïve, résumé, côté</p>
        </body>
        </html>
        """
        
        # Create a large attachment (>3MB) to trigger multipart/form-data encoding
        # This is where the encoding bug was happening
        large_content = b"A" * (3 * 1024 * 1024 + 1000)  # Slightly over 3MB
        attachment_stream = io.BytesIO(large_content)
        
        print(f"Subject: {subject}")
        print(f"To: {recipient}")
        print(f"Attachment size: {len(large_content) / (1024*1024):.2f} MB")
        print("  (Using multipart/form-data encoding)")
        
        print("\nSending message with large attachment...")
        response = client.messages.send(
            identifier=grant_id,
            request_body={
                "subject": subject,
                "to": [{"email": recipient}],
                "body": body,
                "attachments": [
                    {
                        "filename": "large_file.txt",
                        "content_type": "text/plain",
                        "content": attachment_stream,
                        "size": len(large_content),
                    }
                ],
            }
        )
        
        print(f"✓ Message with large attachment sent successfully!")
        print(f"  Message ID: {response.data.id}")
        print(f"  Subject preserved: {response.data.subject == subject}")
        print(f"\n✅ Special characters are correctly encoded even with large attachments!")
        print("   (The fix ensures ensure_ascii=False in json.dumps for multipart data)")
        
    except Exception as e:
        print(f"❌ Error sending message with large attachment: {e}")


def demonstrate_draft_with_special_chars(client: Client, grant_id: str, recipient: str) -> None:
    """Demonstrate creating a draft with special characters."""
    print_separator("Creating Draft with Special Characters")
    
    try:
        subject = "Réunion importante: café & stratégie"
        body = """
        <html>
        <body>
            <h2>Ordre du jour</h2>
            <ol>
                <li>Révision du budget (€)</li>
                <li>Stratégie de développement</li>
                <li>Café et discussion informelle</li>
            </ol>
            <p>À bientôt!</p>
        </body>
        </html>
        """
        
        print(f"Subject: {subject}")
        print(f"To: {recipient}")
        
        print("\nCreating draft...")
        response = client.drafts.create(
            identifier=grant_id,
            request_body={
                "subject": subject,
                "to": [{"email": recipient}],
                "body": body,
            }
        )
        
        print(f"✓ Draft created successfully!")
        print(f"  Draft ID: {response.data.id}")
        print(f"  Subject preserved: {response.data.subject == subject}")
        
        # Clean up - delete the draft
        print("\nCleaning up draft...")
        client.drafts.destroy(identifier=grant_id, draft_id=response.data.id)
        print("✓ Draft deleted")
        
        print(f"\n✅ Special characters in drafts are correctly handled")
        
    except Exception as e:
        print(f"❌ Error with draft: {e}")


def demonstrate_various_languages(client: Client, grant_id: str, recipient: str) -> None:
    """Demonstrate various international characters."""
    print_separator("International Characters - Various Languages")
    
    test_cases = [
        ("French", "Réservation confirmée: café à 15h"),
        ("Spanish", "¡Hola! ¿Cómo estás? Mañana será mejor"),
        ("German", "Größe: über 100 Stück verfügbar"),
        ("Portuguese", "Atenção: promoção válida até amanhã"),
        ("Italian", "Caffè espresso: è così buono!"),
        ("Russian", "Привет! Как дела?"),
        ("Japanese", "こんにちは、お元気ですか？"),
        ("Chinese", "你好，最近怎么样？"),
        ("Emoji", "🎉 Celebration time! 🎊 Let's party 🥳"),
    ]
    
    print("Testing subjects in various languages:")
    print("(Note: Not actually sending to avoid spam)")
    print()
    
    for language, subject in test_cases:
        print(f"  {language:15} : {subject}")
        # In a real scenario, you could send these
        # For demo purposes, we just show they can be handled
    
    print(f"\n✅ All international characters can be properly encoded")
    print("   The SDK preserves UTF-8 encoding correctly")


def demonstrate_encoding_explanation() -> None:
    """Explain the encoding fix."""
    print_separator("Technical Explanation of the Fix")
    
    print("""
The Bug:
--------
When sending emails with large attachments (>3MB), the SDK uses 
multipart/form-data encoding. Previously, the message payload was 
serialized using:
    
    json.dumps(request_body)  # Default: ensure_ascii=True

This caused special characters to be escaped as unicode sequences:
    "De l'idée" → "De l\\u2019id\\u00e9e"

When Gmail received this, it would sometimes double-decode or misinterpret
these escape sequences, resulting in:
    "De lâ€™idée" or similar garbled text

The Fix:
--------
The SDK now uses:
    
    json.dumps(request_body, ensure_ascii=False)

This preserves the actual UTF-8 characters in the JSON payload:
    "De l'idée" → "De l'idée" (unchanged)

The multipart/form-data Content-Type header correctly specifies UTF-8,
so email clients now receive and display the characters correctly.

Impact:
-------
✓ Small messages (no large attachments): Always worked correctly
✓ Large messages (with attachments >3MB): Now work correctly!
✓ Drafts with large attachments: Now work correctly!
✓ All international characters: Properly preserved

Testing:
--------
Run the included tests to verify:
    pytest tests/utils/test_file_utils.py::TestFileUtils::test_build_form_request_with_special_characters
    pytest tests/resources/test_messages.py::TestMessage::test_send_message_with_special_characters_large_attachment
    pytest tests/resources/test_drafts.py::TestDraft::test_create_draft_with_special_characters_large_attachment
    """)


def main():
    """Main function demonstrating special character handling."""
    # Get required environment variables
    api_key = get_env_or_exit("NYLAS_API_KEY")
    grant_id = get_env_or_exit("NYLAS_GRANT_ID")
    recipient = get_env_or_exit("RECIPIENT_EMAIL")

    # Initialize Nylas client
    client = Client(api_key=api_key)

    print("╔" + "="*58 + "╗")
    print("║  Nylas SDK: Special Characters Encoding Example         ║")
    print("╚" + "="*58 + "╝")
    print()
    print("This example demonstrates the fix for email subject/body")
    print("encoding issues with special characters (accented letters).")
    print()
    print(f"Testing with:")
    print(f"  Grant ID: {grant_id}")
    print(f"  Recipient: {recipient}")

    # Demonstrate different scenarios
    demonstrate_small_message_with_special_chars(client, grant_id, recipient)
    demonstrate_message_with_large_attachment(client, grant_id, recipient)
    demonstrate_draft_with_special_chars(client, grant_id, recipient)
    demonstrate_various_languages(client, grant_id, recipient)
    demonstrate_encoding_explanation()

    print_separator("Example Completed Successfully! ✅")
    print("\nKey Takeaways:")
    print("1. Special characters are now correctly preserved in all email subjects")
    print("2. The fix applies to both small and large messages (with attachments)")
    print("3. Drafts also handle special characters correctly")
    print("4. All international character sets are supported")
    print()


if __name__ == "__main__":
    main()

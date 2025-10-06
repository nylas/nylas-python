# Special Characters Encoding Example

This example demonstrates how the Nylas Python SDK correctly handles special characters (accented letters, unicode characters) in email subjects and message bodies.

## The Problem

Previously, when sending emails with large attachments (>3MB), special characters in the subject line would be incorrectly encoded. For example:

- **Intended Subject:** "De l'idée à la post-prod, sans friction"
- **What Recipients Saw:** "De lâ€™idée à la post-prod, sans friction"

This issue occurred because the SDK was using `json.dumps()` with the default `ensure_ascii=True` parameter when creating multipart/form-data requests for large attachments.

## The Solution

The SDK now uses `json.dumps(request_body, ensure_ascii=False)` to preserve UTF-8 characters correctly in the JSON payload, ensuring that special characters are displayed properly in recipient inboxes.

## What This Example Demonstrates

1. **Small Messages** - Sending messages with special characters (no attachments)
2. **Large Messages** - Sending messages with special characters AND large attachments (>3MB)
3. **Drafts** - Creating drafts with special characters
4. **International Support** - Handling various international character sets

## Usage

### Prerequisites

1. Install the SDK in development mode:
   ```bash
   cd /path/to/nylas-python
   pip install -e .
   ```

2. Set up environment variables:
   ```bash
   export NYLAS_API_KEY="your_api_key"
   export NYLAS_GRANT_ID="your_grant_id"
   export RECIPIENT_EMAIL="recipient@example.com"
   ```

### Run the Example

```bash
python examples/special_characters_demo/special_characters_example.py
```

## Test Coverage

This fix is covered by comprehensive tests:

```bash
# Test the core fix in file_utils
pytest tests/utils/test_file_utils.py::TestFileUtils::test_build_form_request_with_special_characters

# Test message sending with special characters
pytest tests/resources/test_messages.py::TestMessage::test_send_message_with_special_characters_in_subject
pytest tests/resources/test_messages.py::TestMessage::test_send_message_with_special_characters_large_attachment

# Test draft creation with special characters
pytest tests/resources/test_drafts.py::TestDraft::test_create_draft_with_special_characters_in_subject
pytest tests/resources/test_drafts.py::TestDraft::test_create_draft_with_special_characters_large_attachment
```

## Supported Character Sets

The SDK correctly handles:

- **French:** é, è, ê, à, ù, ç, œ
- **Spanish:** ñ, á, í, ó, ú, ¿, ¡
- **German:** ä, ö, ü, ß
- **Portuguese:** ã, õ, â, ê
- **Italian:** à, è, é, ì, ò, ù
- **Russian:** Cyrillic characters
- **Japanese:** Hiragana, Katakana, Kanji
- **Chinese:** Simplified and Traditional characters
- **Emoji:** 🎉 🎊 🥳 and many more
- **Special symbols:** €, £, ¥, ©, ®, ™

## Technical Details

### The Bug

When using multipart/form-data encoding (for large attachments), the message payload was serialized as:

```python
message_payload = json.dumps(request_body)  # Default: ensure_ascii=True
```

This caused special characters to be escaped as unicode sequences:
```json
{"subject": "De l\u2019id\u00e9e"}
```

### The Fix

The payload is now serialized as:

```python
message_payload = json.dumps(request_body, ensure_ascii=False)
```

This preserves the actual UTF-8 characters:
```json
{"subject": "De l'idée"}
```

The multipart/form-data Content-Type header correctly specifies UTF-8 encoding, ensuring email clients display the characters properly.

## Related Files

- **Core Fix:** `nylas/utils/file_utils.py` - Line 70
- **Tests:** `tests/utils/test_file_utils.py`, `tests/resources/test_messages.py`, `tests/resources/test_drafts.py`
- **Example:** `examples/special_characters_demo/special_characters_example.py`

## Impact

✅ **Before Fix:** Special characters in subjects were garbled when sending emails with large attachments  
✅ **After Fix:** All special characters are correctly preserved and displayed

The fix ensures backwards compatibility - all existing code continues to work without changes.

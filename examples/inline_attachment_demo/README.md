# Inline Attachment Example

This example demonstrates how to send messages and drafts with inline attachments using the `content_id` field in the Nylas Python SDK.

## What This Example Shows

- How to create inline attachments with `content_id` for HTML emails
- How the SDK properly handles `content_id` for large attachments (>3MB)
- The difference between inline attachments and regular attachments
- How to reference inline attachments in HTML email bodies using `cid:` syntax

## Key Features Demonstrated

### Content ID Usage
When an attachment includes a `content_id` field, the SDK will use this as the field name in multipart form data instead of the generic `file{index}` pattern. This is crucial for inline attachments that need to be referenced in the email body.

### HTML Email with Inline Images
The example shows how to:
1. Set the `content_id` field in the attachment
2. Reference the attachment in HTML using `src="cid:your-content-id"`
3. Set appropriate inline properties (`is_inline: True`, `content_disposition: "inline"`)

### Large Attachment Handling
For attachments larger than 3MB, the SDK automatically switches from JSON to multipart form data. With this fix, the `content_id` is now properly respected in the form field names.

## Running the Example

1. Set your Nylas API key:
   ```bash
   export NYLAS_API_KEY='your-api-key-here'
   ```

2. Update the grant ID and email addresses in the script

3. Run the example:
   ```bash
   python inline_attachment_example.py
   ```

## Important Notes

- **Content ID Format**: Use a unique identifier for each inline attachment (e.g., `"image1@example.com"`, `"logo"`, `"banner-image"`)
- **HTML Reference**: Reference inline attachments in HTML using `src="cid:your-content-id"`
- **Backward Compatibility**: Attachments without `content_id` still work as before using `file{index}` naming
- **File Size Threshold**: The 3MB threshold determines whether JSON or form data is used for the request

## Expected Behavior

### Before the Fix (Problematic)
```
Form data fields:
- message: (JSON payload)
- file0: (inline image - content_id ignored)
- file1: (regular attachment)
```

### After the Fix (Correct)
```
Form data fields:
- message: (JSON payload)
- my-inline-image: (inline image - uses content_id)
- file1: (regular attachment - fallback to file{index})
```

This ensures that email clients can properly display inline images by matching the `content_id` in the HTML `cid:` reference with the multipart form field name.

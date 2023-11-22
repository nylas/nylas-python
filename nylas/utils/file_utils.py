import json
import mimetypes
import os

from requests_toolbelt import MultipartEncoder


def _build_form_request(request_body: dict) -> MultipartEncoder:
    """
    Build a form-data request.

    Attributes:
        request_body: The request body to send.

    Returns:
        The multipart/form-data request.
    """
    attachments = request_body.get("attachments", [])
    request_body.pop("attachments", None)
    message_payload = json.dumps(request_body)

    # Create the multipart/form-data encoder
    return MultipartEncoder(
        fields={
            "message": message_payload,
            **{
                f"file{index}": {
                    "filename": attachment.filename,
                    "content_type": attachment.content_type,
                    "content": attachment.content,
                }
                for index, attachment in enumerate(attachments)
            },
        }
    )

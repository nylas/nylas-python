import json
import mimetypes
import os
from pathlib import Path

from requests_toolbelt import MultipartEncoder

from nylas.models.attachments import CreateAttachmentRequest


def attach_file_request_builder(file_path) -> CreateAttachmentRequest:
    """
    Build a request to attach a file.

    Attributes:
        file_path: The path to the file to attach.

    Returns:
        A properly-formatted request to attach the file.
    """
    path = Path(file_path)
    filename = path.name
    size = os.path.getsize(file_path)
    content_type = mimetypes.guess_type(file_path)[0]
    file_stream = open(file_path, "rb")

    return {
        "filename": filename,
        "content_type": content_type if content_type else "application/octet-stream",
        "content": file_stream,
        "size": size,
    }


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

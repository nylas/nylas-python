import base64
import json
import mimetypes
import os
from pathlib import Path
from typing import BinaryIO

from requests_toolbelt import MultipartEncoder

from nylas.models.attachments import CreateAttachmentRequest


MAXIMUM_JSON_ATTACHMENT_SIZE = 3 * 1024 * 1024
"""The maximum size of an attachment that can be sent using json."""


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
    file_stream = open(file_path, "rb")  # pylint: disable=consider-using-with

    return {
        "filename": filename,
        "content_type": content_type if content_type else "application/octet-stream",
        "content": file_stream,
        "size": size,
    }


def encode_stream_to_base64(binary_stream: BinaryIO) -> str:
    """
    Encode the content of a binary stream to a base64 string.

    Attributes:
        binary_stream: The binary stream to encode.

    Returns:
        The base64 encoded content of the binary stream.
    """
    binary_stream.seek(0)
    binary_content = binary_stream.read()
    return base64.b64encode(binary_content).decode("utf-8")


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
    fields = {"message": ("", message_payload, "application/json")}
    for index, attachment in enumerate(attachments):
        fields[f"file{index}"] = (
            attachment["filename"],
            attachment["content"],
            attachment["content_type"],
        )

    return MultipartEncoder(fields=fields)

from io import BytesIO
from unittest.mock import Mock

from nylas.models.attachments import Attachment, CreateAttachmentRequest, FindAttachmentQueryParams
from nylas.resources.attachments import Attachments


class TestAttachmentModel:
    """Tests for the Attachment dataclass model."""

    def test_attachment_deserialization(self):
        """Test full deserialization of Attachment from dict."""
        attach_json = {
            "content_type": "image/png",
            "filename": "pic.png",
            "grant_id": "41009df5-bf11-4c97-aa18-b285b5f2e386",
            "id": "185e56cb50e12e82",
            "is_inline": True,
            "size": 13068,
            "content_id": "<ce9b9547-9eeb-43b2-ac4e-58768bdf04e4>",
            "content_disposition": "inline",
        }

        attachment = Attachment.from_dict(attach_json)

        assert attachment.content_type == "image/png"
        assert attachment.filename == "pic.png"
        assert attachment.grant_id == "41009df5-bf11-4c97-aa18-b285b5f2e386"
        assert attachment.id == "185e56cb50e12e82"
        assert attachment.is_inline is True
        assert attachment.size == 13068
        assert attachment.content_id == "<ce9b9547-9eeb-43b2-ac4e-58768bdf04e4>"
        assert attachment.content_disposition == "inline"

    def test_attachment_serialization(self):
        """Test serialization of Attachment to dict."""
        attachment = Attachment(
            id="185e56cb50e12e82",
            grant_id="41009df5-bf11-4c97-aa18-b285b5f2e386",
            filename="document.pdf",
            content_type="application/pdf",
            size=2048,
            content_id="<doc-123>",
            content_disposition="attachment",
            is_inline=False,
        )

        result = attachment.to_dict()

        assert result["id"] == "185e56cb50e12e82"
        assert result["grant_id"] == "41009df5-bf11-4c97-aa18-b285b5f2e386"
        assert result["filename"] == "document.pdf"
        assert result["content_type"] == "application/pdf"
        assert result["size"] == 2048
        assert result["content_id"] == "<doc-123>"
        assert result["content_disposition"] == "attachment"
        assert result["is_inline"] is False

    def test_attachment_deserialization_partial_fields(self):
        """Test deserialization with only required fields."""
        attach_json = {
            "id": "abc123",
            "filename": "test.txt",
        }

        attachment = Attachment.from_dict(attach_json)

        assert attachment.id == "abc123"
        assert attachment.filename == "test.txt"
        assert attachment.grant_id is None
        assert attachment.content_type is None
        assert attachment.size is None
        assert attachment.content_id is None
        assert attachment.content_disposition is None
        assert attachment.is_inline is None

    def test_attachment_deserialization_empty_dict(self):
        """Test deserialization from empty dict."""
        attachment = Attachment.from_dict({})

        assert attachment.id is None
        assert attachment.grant_id is None
        assert attachment.filename is None
        assert attachment.content_type is None
        assert attachment.size is None
        assert attachment.content_id is None
        assert attachment.content_disposition is None
        assert attachment.is_inline is None

    def test_attachment_default_values(self):
        """Test Attachment instantiation with default values."""
        attachment = Attachment()

        assert attachment.id is None
        assert attachment.grant_id is None
        assert attachment.filename is None
        assert attachment.content_type is None
        assert attachment.size is None
        assert attachment.content_id is None
        assert attachment.content_disposition is None
        assert attachment.is_inline is None

    def test_attachment_content_disposition_attachment(self):
        """Test attachment with content_disposition set to 'attachment'."""
        attach_json = {
            "id": "file-123",
            "filename": "report.xlsx",
            "content_disposition": "attachment",
            "is_inline": False,
        }

        attachment = Attachment.from_dict(attach_json)

        assert attachment.content_disposition == "attachment"
        assert attachment.is_inline is False

    def test_attachment_content_disposition_inline(self):
        """Test inline attachment with content_disposition."""
        attach_json = {
            "id": "img-456",
            "filename": "logo.png",
            "content_disposition": "inline",
            "is_inline": True,
            "content_id": "<logo@example.com>",
        }

        attachment = Attachment.from_dict(attach_json)

        assert attachment.content_disposition == "inline"
        assert attachment.is_inline is True
        assert attachment.content_id == "<logo@example.com>"

    def test_attachment_roundtrip_serialization(self):
        """Test that serialization and deserialization are inverses."""
        original = Attachment(
            id="test-id",
            grant_id="grant-123",
            filename="file.txt",
            content_type="text/plain",
            size=100,
            content_id="<cid123>",
            content_disposition="attachment",
            is_inline=False,
        )

        serialized = original.to_dict()
        deserialized = Attachment.from_dict(serialized)

        assert deserialized.id == original.id
        assert deserialized.grant_id == original.grant_id
        assert deserialized.filename == original.filename
        assert deserialized.content_type == original.content_type
        assert deserialized.size == original.size
        assert deserialized.content_id == original.content_id
        assert deserialized.content_disposition == original.content_disposition
        assert deserialized.is_inline == original.is_inline


class TestCreateAttachmentRequest:
    """Tests for the CreateAttachmentRequest TypedDict."""

    def test_create_attachment_request_with_base64_content(self):
        """Test creating attachment request with base64 encoded content."""
        request: CreateAttachmentRequest = {
            "filename": "test.txt",
            "content_type": "text/plain",
            "content": "SGVsbG8gV29ybGQh",  # base64 for "Hello World!"
            "size": 12,
        }

        assert request["filename"] == "test.txt"
        assert request["content_type"] == "text/plain"
        assert request["content"] == "SGVsbG8gV29ybGQh"
        assert request["size"] == 12

    def test_create_attachment_request_with_file_object(self):
        """Test creating attachment request with file-like object."""
        file_content = BytesIO(b"File content here")

        request: CreateAttachmentRequest = {
            "filename": "document.pdf",
            "content_type": "application/pdf",
            "content": file_content,
            "size": 17,
        }

        assert request["filename"] == "document.pdf"
        assert request["content_type"] == "application/pdf"
        assert request["content"] == file_content
        assert request["size"] == 17

    def test_create_attachment_request_with_optional_fields(self):
        """Test creating attachment request with all optional fields."""
        request: CreateAttachmentRequest = {
            "filename": "image.png",
            "content_type": "image/png",
            "content": "iVBORw0KGgo=",
            "size": 1024,
            "content_id": "<image001@example.com>",
            "content_disposition": "inline",
            "is_inline": True,
        }

        assert request["filename"] == "image.png"
        assert request["content_type"] == "image/png"
        assert request["content"] == "iVBORw0KGgo="
        assert request["size"] == 1024
        assert request["content_id"] == "<image001@example.com>"
        assert request["content_disposition"] == "inline"
        assert request["is_inline"] is True

    def test_create_attachment_request_minimal(self):
        """Test creating attachment request with only required fields."""
        request: CreateAttachmentRequest = {
            "filename": "minimal.txt",
            "content_type": "text/plain",
            "content": "data",
            "size": 4,
        }

        assert "filename" in request
        assert "content_type" in request
        assert "content" in request
        assert "size" in request
        # Optional fields should not be present
        assert "content_id" not in request
        assert "content_disposition" not in request
        assert "is_inline" not in request


class TestFindAttachmentQueryParams:
    """Tests for the FindAttachmentQueryParams TypedDict."""

    def test_find_attachment_query_params(self):
        """Test creating find attachment query params."""
        params: FindAttachmentQueryParams = {
            "message_id": "msg-12345",
        }

        assert params["message_id"] == "msg-12345"

    def test_find_attachment_query_params_various_message_ids(self):
        """Test find attachment query params with various message ID formats."""
        # Simple ID
        params1: FindAttachmentQueryParams = {"message_id": "abc123"}
        assert params1["message_id"] == "abc123"

        # UUID format
        params2: FindAttachmentQueryParams = {"message_id": "550e8400-e29b-41d4-a716-446655440000"}
        assert params2["message_id"] == "550e8400-e29b-41d4-a716-446655440000"

        # Complex message ID (email message-id format)
        params3: FindAttachmentQueryParams = {"message_id": "<CABcd123@mail.example.com>"}
        assert params3["message_id"] == "<CABcd123@mail.example.com>"


class TestAttachments:
    """Tests for the Attachments resource API calls."""

    def test_find_attachment(self, http_client_response):
        attachments = Attachments(http_client_response)
        query_params = FindAttachmentQueryParams(message_id="message-123")

        attachments.find(
            identifier="abc-123",
            attachment_id="attachment-123",
            query_params=query_params,
        )

        http_client_response._execute.assert_called_once_with(
            "GET",
            "/v3/grants/abc-123/attachments/attachment-123",
            None,
            query_params,
            None,
            overrides=None,
        )

    def test_download_attachment(self):
        mock_http_client = Mock()
        mock_http_client._execute_download_request.return_value = b"mock data"
        attachments = Attachments(mock_http_client)
        query_params = FindAttachmentQueryParams(message_id="message-123")

        attachments.download(
            identifier="abc-123",
            attachment_id="attachment-123",
            query_params=query_params,
            overrides=None,
        )

        mock_http_client._execute_download_request.assert_called_once_with(
            path="/v3/grants/abc-123/attachments/attachment-123/download",
            query_params=query_params,
            stream=True,
            overrides=None,
        )

    def test_download_bytes(self):
        mock_http_client = Mock()
        mock_http_client._execute_download_request.return_value = b"mock data"
        attachments = Attachments(mock_http_client)
        query_params = FindAttachmentQueryParams(message_id="message-123")

        attachments.download_bytes(
            identifier="abc-123",
            attachment_id="attachment-123",
            query_params=query_params,
            overrides=None,
        )

        mock_http_client._execute_download_request.assert_called_once_with(
            path="/v3/grants/abc-123/attachments/attachment-123/download",
            query_params=query_params,
            stream=False,
            overrides=None,
        )

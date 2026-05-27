from io import BytesIO
from unittest.mock import Mock

from nylas.models.attachments import (
    Attachment,
    CreateAttachmentRequest,
    FindAttachmentQueryParams,
    AttachmentUploadSession,
    AttachmentUploadSessionComplete,
    CreateAttachmentUploadSessionRequest,
)
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

    def test_create_upload_session(self, http_client_response):
        attachments = Attachments(http_client_response)
        request_body: CreateAttachmentUploadSessionRequest = {
            "filename": "document.pdf",
            "content_type": "application/pdf",
            "size": 5242880,
        }

        attachments.create_upload_session(
            identifier="abc-123",
            request_body=request_body,
        )

        http_client_response._execute.assert_called_once_with(
            "POST",
            "/v3/grants/abc-123/attachment-uploads",
            None,
            None,
            request_body,
            overrides=None,
        )

    def test_create_upload_session_without_size(self, http_client_response):
        attachments = Attachments(http_client_response)
        request_body: CreateAttachmentUploadSessionRequest = {
            "filename": "report.xlsx",
            "content_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        }

        attachments.create_upload_session(
            identifier="abc-123",
            request_body=request_body,
        )

        http_client_response._execute.assert_called_once_with(
            "POST",
            "/v3/grants/abc-123/attachment-uploads",
            None,
            None,
            request_body,
            overrides=None,
        )

    def test_complete_upload_session(self, http_client_response):
        attachments = Attachments(http_client_response)

        attachments.complete_upload_session(
            identifier="abc-123",
            attachment_id="session-id-123",
        )

        http_client_response._execute.assert_called_once_with(
            "POST",
            "/v3/grants/abc-123/attachment-uploads/session-id-123/complete",
            None,
            None,
            {},
            overrides=None,
        )


class TestAttachmentUploadSession:
    """Tests for the AttachmentUploadSession dataclass model."""

    def test_deserialization_full(self):
        session_json = {
            "attachment_id": "session-abc-123",
            "method": "PUT",
            "url": "https://storage.example.com/upload/session-abc-123",
            "headers": {"x-ms-blob-type": "BlockBlob"},
            "expires_at": "2026-05-05T12:00:00Z",
            "max_size": 157286400,
            "size": 5242880,
            "content_type": "application/pdf",
            "filename": "document.pdf",
            "grant_id": "grant-abc-123",
        }

        session = AttachmentUploadSession.from_dict(session_json)

        assert session.attachment_id == "session-abc-123"
        assert session.method == "PUT"
        assert session.url == "https://storage.example.com/upload/session-abc-123"
        assert session.headers == {"x-ms-blob-type": "BlockBlob"}
        assert session.expires_at == "2026-05-05T12:00:00Z"
        assert session.max_size == 157286400
        assert session.size == 5242880
        assert session.content_type == "application/pdf"
        assert session.filename == "document.pdf"
        assert session.grant_id == "grant-abc-123"

    def test_deserialization_without_size(self):
        """When size is omitted from the request, the API echoes 0."""
        session_json = {
            "attachment_id": "session-no-size",
            "method": "PUT",
            "url": "https://storage.example.com/upload/session-no-size",
            "headers": {},
            "expires_at": "2026-05-05T12:00:00Z",
            "max_size": 157286400,
            "size": 0,
            "content_type": "text/plain",
            "filename": "notes.txt",
            "grant_id": "grant-xyz",
        }

        session = AttachmentUploadSession.from_dict(session_json)

        assert session.attachment_id == "session-no-size"
        assert session.size == 0
        assert session.headers == {}

    def test_deserialization_partial(self):
        """Partial response should not raise; unset fields default to None."""
        session = AttachmentUploadSession.from_dict({"attachment_id": "partial-session"})

        assert session.attachment_id == "partial-session"
        assert session.method is None
        assert session.url is None
        assert session.headers is None
        assert session.expires_at is None
        assert session.max_size is None
        assert session.size is None
        assert session.content_type is None
        assert session.filename is None
        assert session.grant_id is None

    def test_deserialization_empty_dict(self):
        session = AttachmentUploadSession.from_dict({})

        assert session.attachment_id is None
        assert session.grant_id is None

    def test_roundtrip_serialization(self):
        original = AttachmentUploadSession(
            attachment_id="rt-session",
            method="PUT",
            url="https://example.com/upload",
            headers={"Content-Type": "application/octet-stream"},
            expires_at="2026-05-05T12:00:00Z",
            max_size=157286400,
            size=1024,
            content_type="application/octet-stream",
            filename="file.bin",
            grant_id="grant-rt",
        )

        serialized = original.to_dict()
        deserialized = AttachmentUploadSession.from_dict(serialized)

        assert deserialized.attachment_id == original.attachment_id
        assert deserialized.method == original.method
        assert deserialized.url == original.url
        assert deserialized.headers == original.headers
        assert deserialized.expires_at == original.expires_at
        assert deserialized.max_size == original.max_size
        assert deserialized.size == original.size
        assert deserialized.content_type == original.content_type
        assert deserialized.filename == original.filename
        assert deserialized.grant_id == original.grant_id


class TestAttachmentUploadSessionComplete:
    """Tests for the AttachmentUploadSessionComplete dataclass model."""

    def test_deserialization_ready(self):
        complete_json = {
            "attachment_id": "session-abc-123",
            "grant_id": "grant-abc-123",
            "status": "ready",
        }

        complete = AttachmentUploadSessionComplete.from_dict(complete_json)

        assert complete.attachment_id == "session-abc-123"
        assert complete.grant_id == "grant-abc-123"
        assert complete.status == "ready"

    def test_deserialization_various_statuses(self):
        for status in ("uploading", "failed", "expired"):
            complete = AttachmentUploadSessionComplete.from_dict({
                "attachment_id": "session-123",
                "grant_id": "grant-123",
                "status": status,
            })
            assert complete.status == status

    def test_deserialization_empty_dict(self):
        complete = AttachmentUploadSessionComplete.from_dict({})

        assert complete.attachment_id is None
        assert complete.grant_id is None
        assert complete.status is None

    def test_roundtrip_serialization(self):
        original = AttachmentUploadSessionComplete(
            attachment_id="session-rt",
            grant_id="grant-rt",
            status="ready",
        )

        serialized = original.to_dict()
        deserialized = AttachmentUploadSessionComplete.from_dict(serialized)

        assert deserialized.attachment_id == original.attachment_id
        assert deserialized.grant_id == original.grant_id
        assert deserialized.status == original.status


class TestCreateAttachmentUploadSessionRequest:
    """Tests for the CreateAttachmentUploadSessionRequest TypedDict."""

    def test_required_fields_only(self):
        request: CreateAttachmentUploadSessionRequest = {
            "filename": "document.pdf",
            "content_type": "application/pdf",
        }

        assert request["filename"] == "document.pdf"
        assert request["content_type"] == "application/pdf"
        assert "size" not in request

    def test_with_size(self):
        request: CreateAttachmentUploadSessionRequest = {
            "filename": "video.mp4",
            "content_type": "video/mp4",
            "size": 104857600,  # 100 MB
        }

        assert request["filename"] == "video.mp4"
        assert request["content_type"] == "video/mp4"
        assert request["size"] == 104857600

    def test_max_allowed_size(self):
        request: CreateAttachmentUploadSessionRequest = {
            "filename": "archive.zip",
            "content_type": "application/zip",
            "size": 157286400,  # 150 MB max
        }

        assert request["size"] == 157286400

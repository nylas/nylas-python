from unittest.mock import Mock

from nylas.models.attachments import Attachment, FindAttachmentQueryParams
from nylas.resources.attachments import Attachments


class TestAttachments:
    def test_attachment_deserialization(self, http_client):
        attach_json = {
            "content_type": "image/png",
            "filename": "pic.png",
            "grant_id": "41009df5-bf11-4c97-aa18-b285b5f2e386",
            "id": "185e56cb50e12e82",
            "is_inline": True,
            "size": 13068,
            "content_id": "<ce9b9547-9eeb-43b2-ac4e-58768bdf04e4>",
        }

        attachment = Attachment.from_dict(attach_json)

        assert attachment.content_type == "image/png"
        assert attachment.filename == "pic.png"
        assert attachment.grant_id == "41009df5-bf11-4c97-aa18-b285b5f2e386"
        assert attachment.id == "185e56cb50e12e82"
        assert attachment.is_inline is True
        assert attachment.size == 13068
        assert attachment.content_id == "<ce9b9547-9eeb-43b2-ac4e-58768bdf04e4>"

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
            overrides=None
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
            overrides=None
        )

        mock_http_client._execute_download_request.assert_called_once_with(
            path="/v3/grants/abc-123/attachments/attachment-123/download",
            query_params=query_params,
            stream=True,
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
            overrides=None
        )

        mock_http_client._execute_download_request.assert_called_once_with(
            path="/v3/grants/abc-123/attachments/attachment-123/download",
            query_params=query_params,
            stream=False,
        )

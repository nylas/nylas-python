from unittest.mock import patch, mock_open

from nylas.utils.file_utils import attach_file_request_builder, _build_form_request


class TestFileUtils:
    def test_attach_file_request_builder(self):
        file_path = "tests/data/attachment.txt"
        file_size = 1234
        content_type = "text/plain"
        mocked_open = mock_open(read_data="test data")

        with patch("os.path.getsize", return_value=file_size):
            with patch("mimetypes.guess_type", return_value=(content_type, None)):
                with patch("builtins.open", mocked_open):
                    attach_file_request = attach_file_request_builder(file_path)

                    assert attach_file_request["filename"] == "attachment.txt"
                    assert attach_file_request["content_type"] == content_type
                    assert attach_file_request["size"] == file_size
                    mocked_open.assert_called_once_with(file_path, "rb")

    def test_build_form_request(self):
        request_body = {
            "to": [{"email": "test@gmail.com"}],
            "subject": "test subject",
            "body": "test body",
            "attachments": [
                {
                    "filename": "attachment.txt",
                    "content_type": "text/plain",
                    "content": b"test data",
                    "size": 1234,
                }
            ],
        }

        request = _build_form_request(request_body)

        assert len(request.fields) == 2
        assert "message" in request.fields
        assert "file0" in request.fields
        assert len(request.fields["message"]) == 3
        assert request.fields["message"][0] == ""
        assert (
            request.fields["message"][1]
            == '{"to": [{"email": "test@gmail.com"}], "subject": "test subject", "body": "test body"}'
        )
        assert request.fields["message"][2] == "application/json"
        assert len(request.fields["file0"]) == 3
        assert request.fields["file0"][0] == "attachment.txt"
        assert request.fields["file0"][1] == b"test data"
        assert request.fields["file0"][2] == "text/plain"

    def test_build_form_request_no_attachments(self):
        request_body = {
            "to": [{"email": "test@gmail.com"}],
            "subject": "test subject",
            "body": "test body",
        }

        request = _build_form_request(request_body)

        assert len(request.fields) == 1
        assert "message" in request.fields
        assert len(request.fields["message"]) == 3
        assert request.fields["message"][0] == ""
        assert (
            request.fields["message"][1]
            == '{"to": [{"email": "test@gmail.com"}], "subject": "test subject", "body": "test body"}'
        )
        assert request.fields["message"][2] == "application/json"

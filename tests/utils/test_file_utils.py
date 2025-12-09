from unittest.mock import patch, mock_open

from nylas.utils.file_utils import attach_file_request_builder, _build_form_request, encode_stream_to_base64


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

    def test_encode_stream_to_base64(self):
        """Test that binary streams are properly encoded to base64."""
        import io
        
        # Create a binary stream with test data
        test_data = b"Hello, World! This is test data."
        binary_stream = io.BytesIO(test_data)
        
        # Move the stream position to simulate it being read
        binary_stream.seek(10)
        
        # Encode to base64
        encoded = encode_stream_to_base64(binary_stream)
        
        # Verify the result
        import base64
        expected = base64.b64encode(test_data).decode("utf-8")
        assert encoded == expected
        
        # Verify the stream position was reset to 0 and read completely
        assert binary_stream.tell() == len(test_data)

    def test_build_form_request_with_content_id(self):
        """Test that content_id is used as field name when provided."""
        request_body = {
            "to": [{"email": "test@gmail.com"}],
            "subject": "test subject",
            "body": "test body",
            "attachments": [
                {
                    "filename": "inline_image.png",
                    "content_type": "image/png",
                    "content": b"image data",
                    "size": 1234,
                    "content_id": "image1@example.com",
                },
                {
                    "filename": "regular_attachment.txt",
                    "content_type": "text/plain",
                    "content": b"text data",
                    "size": 5678,
                    # No content_id, should fallback to file{index}
                }
            ],
        }

        request = _build_form_request(request_body)

        assert len(request.fields) == 3
        assert "message" in request.fields
        assert "image1@example.com" in request.fields  # Uses content_id
        assert "file1" in request.fields  # Falls back to file{index} for attachment without content_id
        
        # Verify the inline attachment with content_id
        assert len(request.fields["image1@example.com"]) == 3
        assert request.fields["image1@example.com"][0] == "inline_image.png"
        assert request.fields["image1@example.com"][1] == b"image data"
        assert request.fields["image1@example.com"][2] == "image/png"
        
        # Verify the regular attachment without content_id
        assert len(request.fields["file1"]) == 3
        assert request.fields["file1"][0] == "regular_attachment.txt"
        assert request.fields["file1"][1] == b"text data"
        assert request.fields["file1"][2] == "text/plain"

    def test_build_form_request_backwards_compatibility(self):
        """Test that existing behavior is preserved when no content_id is provided."""
        request_body = {
            "to": [{"email": "test@gmail.com"}],
            "subject": "test subject",
            "body": "test body",
            "attachments": [
                {
                    "filename": "attachment1.txt",
                    "content_type": "text/plain",
                    "content": b"test data 1",
                    "size": 1234,
                },
                {
                    "filename": "attachment2.txt",
                    "content_type": "text/plain",
                    "content": b"test data 2",
                    "size": 5678,
                }
            ],
        }

        request = _build_form_request(request_body)

        assert len(request.fields) == 3
        assert "message" in request.fields
        assert "file0" in request.fields  # First attachment
        assert "file1" in request.fields  # Second attachment
        
        # Verify first attachment
        assert request.fields["file0"][0] == "attachment1.txt"
        assert request.fields["file0"][1] == b"test data 1"
        assert request.fields["file0"][2] == "text/plain"
        
        # Verify second attachment
        assert request.fields["file1"][0] == "attachment2.txt"
        assert request.fields["file1"][1] == b"test data 2"
        assert request.fields["file1"][2] == "text/plain"

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

    def test_build_form_request_with_special_characters(self):
        """Test that special characters (accented letters) are properly encoded in form requests."""
        import json
        
        # This is the exact subject from the bug report
        request_body = {
            "to": [{"email": "test@gmail.com"}],
            "subject": "De l'idée à la post-prod, sans friction",
            "body": "Test body with special chars: café, naïve, résumé",
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

        # Verify the message field exists
        assert "message" in request.fields
        message_content = request.fields["message"][1]
        
        # Parse the JSON to verify it contains the correct characters
        parsed_message = json.loads(message_content)
        assert parsed_message["subject"] == "De l'idée à la post-prod, sans friction"
        assert "café" in parsed_message["body"]
        assert "naïve" in parsed_message["body"]
        assert "résumé" in parsed_message["body"]
        
        # Verify that ASCII characters are NOT escaped (they remain as-is)
        # Non-ASCII characters are preserved as UTF-8 in the JSON string
        assert "é" in message_content  # Non-ASCII characters preserved as UTF-8
        assert "à" in message_content
        assert "ï" in message_content
        # Verify ASCII characters like apostrophe are not escaped
        assert "'" in message_content  # ASCII apostrophe should not be escaped
        assert "idée" in message_content  # Full word with special chars preserved
        
    def test_build_form_request_encoding_comparison(self):
        """Test to demonstrate the difference between ensure_ascii=True and ensure_ascii=False."""
        import json
        
        test_subject = "De l'idée à la post-prod, sans friction"
        
        # With ensure_ascii=True (default - this causes the bug)
        encoded_with_ascii = json.dumps({"subject": test_subject}, ensure_ascii=True)
        # This will produce escape sequences like \u00e9 for é
        
        # With ensure_ascii=False (the fix)
        encoded_without_ascii = json.dumps({"subject": test_subject}, ensure_ascii=False)
        # This will preserve the actual UTF-8 characters
        
        # Verify the difference
        assert "\\u" in encoded_with_ascii or test_subject not in encoded_with_ascii
        assert test_subject in encoded_without_ascii
        assert "idée" in encoded_without_ascii
        assert "café" not in encoded_with_ascii  # Would be escaped
        
        # Both should decode to the same value
        assert json.loads(encoded_with_ascii)["subject"] == test_subject
        assert json.loads(encoded_without_ascii)["subject"] == test_subject

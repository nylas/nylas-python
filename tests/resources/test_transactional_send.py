from unittest.mock import Mock, patch

from nylas.resources.transactional_send import TransactionalSend


class TestTransactionalSend:
    def test_send_transactional_message(self, http_client_response):
        transactional_send = TransactionalSend(http_client_response)
        request_body = {
            "subject": "Welcome",
            "to": [{"name": "Jane Doe", "email": "jane.doe@example.com"}],
            "from_": {"name": "ACME Support", "email": "support@acme.com"},
            "body": "Welcome to ACME.",
        }

        transactional_send.send(domain_name="mail.acme.com", request_body=request_body)

        http_client_response._execute.assert_called_once_with(
            method="POST",
            path="/v3/domains/mail.acme.com/messages/send",
            request_body={
                "subject": "Welcome",
                "to": [{"name": "Jane Doe", "email": "jane.doe@example.com"}],
                "from": {"name": "ACME Support", "email": "support@acme.com"},
                "body": "Welcome to ACME.",
            },
            data=None,
            overrides=None,
        )

    def test_send_domain_name_url_encoded(self, http_client_response):
        transactional_send = TransactionalSend(http_client_response)
        request_body = {
            "to": [{"email": "a@b.com"}],
            "from_": {"email": "support@acme.com"},
        }

        transactional_send.send(
            domain_name="weird/slash.com",
            request_body=request_body,
        )

        http_client_response._execute.assert_called_once_with(
            method="POST",
            path="/v3/domains/weird%2Fslash.com/messages/send",
            request_body={
                "to": [{"email": "a@b.com"}],
                "from": {"email": "support@acme.com"},
            },
            data=None,
            overrides=None,
        )

    def test_send_small_attachment(self, http_client_response):
        transactional_send = TransactionalSend(http_client_response)
        request_body = {
            "to": [{"email": "j@example.com"}],
            "from_": {"email": "support@acme.com"},
            "attachments": [
                {
                    "filename": "file1.txt",
                    "content_type": "text/plain",
                    "content": "this is a file",
                    "size": 3,
                },
            ],
        }

        transactional_send.send(domain_name="acme.com", request_body=request_body)

        http_client_response._execute.assert_called_once_with(
            method="POST",
            path="/v3/domains/acme.com/messages/send",
            request_body=request_body,
            data=None,
            overrides=None,
        )

    def test_send_large_attachment(self, http_client_response):
        transactional_send = TransactionalSend(http_client_response)
        mock_encoder = Mock()
        request_body = {
            "to": [{"email": "j@example.com"}],
            "from_": {"email": "support@acme.com"},
            "attachments": [
                {
                    "filename": "file1.txt",
                    "content_type": "text/plain",
                    "content": "this is a file",
                    "size": 3 * 1024 * 1024,
                },
            ],
        }

        with patch(
            "nylas.resources.transactional_send._build_form_request",
            return_value=mock_encoder,
        ):
            transactional_send.send(domain_name="acme.com", request_body=request_body)

            http_client_response._execute.assert_called_once_with(
                method="POST",
                path="/v3/domains/acme.com/messages/send",
                request_body=None,
                data=mock_encoder,
                overrides=None,
            )

    def test_send_with_existing_from_field_unchanged(self, http_client_response):
        transactional_send = TransactionalSend(http_client_response)
        request_body = {
            "to": [{"email": "j@example.com"}],
            "from": {"email": "direct@acme.com"},
            "from_": {"email": "ignored@acme.com"},
        }

        transactional_send.send(domain_name="acme.com", request_body=request_body)

        http_client_response._execute.assert_called_once_with(
            method="POST",
            path="/v3/domains/acme.com/messages/send",
            request_body=request_body,
            data=None,
            overrides=None,
        )

import io
import urllib.parse

from nylas.config import RequestOverrides
from nylas.models.messages import Message
from nylas.models.response import Response
from nylas.models.transactional_send import TransactionalSendMessageRequest
from nylas.resources.resource import Resource
from nylas.utils.file_utils import (
    MAXIMUM_JSON_ATTACHMENT_SIZE,
    _build_form_request,
    encode_stream_to_base64,
)


class TransactionalSend(Resource):
    """
    Nylas Transactional Send API.

    Send email from a verified domain without a grant context.
    """

    def send(
        self,
        domain_name: str,
        request_body: TransactionalSendMessageRequest,
        overrides: RequestOverrides = None,
    ) -> Response[Message]:
        """
        Send a transactional email from the specified domain.

        Args:
            domain_name: The domain Nylas sends from (must be verified in the dashboard).
            request_body: Message fields; use ``from_`` for the sender (maps to JSON ``from``).
            overrides: Per-request overrides for the HTTP client.

        Returns:
            The sent message in a ``Response``.
        """
        path = (
            f"/v3/domains/{urllib.parse.quote(domain_name, safe='')}/messages/send"
        )
        form_data = None
        json_body = None

        if "from_" in request_body and "from" not in request_body:
            request_body["from"] = request_body["from_"]
            del request_body["from_"]

        attachment_size = sum(
            attachment.get("size", 0)
            for attachment in request_body.get("attachments", [])
        )
        if attachment_size >= MAXIMUM_JSON_ATTACHMENT_SIZE:
            form_data = _build_form_request(request_body)
        else:
            for attachment in request_body.get("attachments", []):
                if issubclass(type(attachment["content"]), io.IOBase):
                    attachment["content"] = encode_stream_to_base64(
                        attachment["content"]
                    )

            json_body = request_body

        json_response, headers = self._http_client._execute(
            method="POST",
            path=path,
            request_body=json_body,
            data=form_data,
            overrides=overrides,
        )

        return Response.from_dict(json_response, Message, headers)

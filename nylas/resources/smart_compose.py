from nylas.config import RequestOverrides
from nylas.models.response import Response

from nylas.models.smart_compose import ComposeMessageRequest, ComposeMessageResponse
from nylas.resources.resource import Resource


class SmartCompose(Resource):
    """
    A collection of Smart Compose related API endpoints.

    These endpoints allow for the generation of message suggestions.
    """

    def compose_message(
        self,
        identifier: str,
        request_body: ComposeMessageRequest,
        overrides: RequestOverrides = None,
    ) -> Response[ComposeMessageResponse]:
        """
        Compose a message.

        Args:
            identifier: The identifier of the grant to generate a message suggestion for.
            request_body: The prompt that smart compose will use to generate a message suggestion.
            overrides: The request overrides to apply to the request.

        Returns:
            The generated message.
        """
        res, headers = self._http_client._execute(
            method="POST",
            path=f"/v3/grants/{identifier}/messages/smart-compose",
            request_body=request_body,
            overrides=overrides,
        )

        return Response.from_dict(res, ComposeMessageResponse, headers)

    def compose_message_reply(
        self,
        identifier: str,
        message_id: str,
        request_body: ComposeMessageRequest,
        overrides: RequestOverrides = None,
    ) -> ComposeMessageResponse:
        """
        Compose a message reply.

        Args:
            identifier: The identifier of the grant to generate a message suggestion for.
            message_id: The id of the message to reply to.
            request_body: The prompt that smart compose will use to generate a message reply suggestion.
            overrides: The request overrides to apply to the request.

        Returns:
            The generated message reply.
        """
        res, headers = self._http_client._execute(
            method="POST",
            path=f"/v3/grants/{identifier}/messages/{message_id}/smart-compose",
            request_body=request_body,
            overrides=overrides,
        )

        return Response.from_dict(res, ComposeMessageResponse, headers)

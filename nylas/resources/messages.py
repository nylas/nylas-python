import json
from typing import Optional

from requests_toolbelt import MultipartEncoder

from nylas.handler.api_resources import (
    ListableApiResource,
    FindableApiResource,
    UpdatableApiResource,
    DestroyableApiResource,
)
from nylas.models.drafts import SendMessageRequest
from nylas.models.messages import (
    Message,
    ListMessagesQueryParams,
    FindMessageQueryParams,
    UpdateMessageRequest,
    ScheduledMessagesList,
    ScheduledMessage,
    StopScheduledMessageResponse,
)
from nylas.models.response import Response, ListResponse, DeleteResponse
from nylas.resources.smart_compose import SmartCompose


def _build_form_request(request_body: dict) -> MultipartEncoder:
    attachments = request_body.get("attachments", [])
    request_body.pop("attachments", None)
    message_payload = json.dumps(request_body)

    # Create the multipart/form-data encoder
    return MultipartEncoder(
        fields={
            "message": ("message", message_payload, "application/json"),
            **{
                f"file{index}": {
                    "filename": attachment.filename,
                    "content_type": attachment.content_type,
                }
                for index, attachment in enumerate(attachments)
            },
        }
    )


class Messages(
    ListableApiResource,
    FindableApiResource,
    UpdatableApiResource,
    DestroyableApiResource,
):
    @property
    def smart_compose(self) -> SmartCompose:
        """
        Access the Smart Compose collection of endpoints.

        Returns:
            The Smart Compose collection of endpoints.
        """
        return SmartCompose(self._http_client)

    def list(
        self, identifier: str, query_params: Optional[ListMessagesQueryParams] = None
    ) -> ListResponse[Message]:
        """
        Return all Messages.

        Args:
            identifier: The identifier of the grant to get messages for.
            query_params: The query parameters to filter messages by.

        Returns:
            A list of Messages.
        """
        return super(Messages, self).list(
            path=f"/v3/grants/{identifier}/messages",
            response_type=Message,
            query_params=query_params,
        )

    def find(
        self,
        identifier: str,
        message_id: str,
        query_params: Optional[FindMessageQueryParams] = None,
    ) -> Response[Message]:
        """
        Return a Message.

        Args:
            identifier: The identifier of the grant to get the message for.
            message_id: The identifier of the message to get.
            query_params: The query parameters to include in the request.

        Returns:
            The requested Message.
        """
        return super(Messages, self).find(
            path=f"/v3/grants/{identifier}/messages/{message_id}",
            response_type=Message,
            query_params=query_params,
        )

    def update(
        self,
        identifier: str,
        message_id: str,
        request_body: UpdateMessageRequest,
    ) -> Response[Message]:
        """
        Update a Message.

        Args:
            identifier: The identifier of the grant to update the message for.
            message_id: The identifier of the message to update.
            request_body: The request body to update the message with.
            query_params: The query parameters to include in the request.

        Returns:
            The updated Message.
        """
        return super(Messages, self).update(
            path=f"/v3/grants/{identifier}/messages/{message_id}",
            response_type=Message,
            request_body=request_body,
        )

    def destroy(self, identifier: str, message_id: str) -> DeleteResponse:
        """
        Delete a Message.

        Args:
            identifier: The identifier of the grant to delete the message for.
            message_id: The identifier of the message to delete.

        Returns:
            The deletion response.
        """
        return super(Messages, self).destroy(
            path=f"/v3/grants/{identifier}/messages/{message_id}",
        )

    def send(
        self, identifier: str, request_body: SendMessageRequest
    ) -> Response[Message]:
        """
        Send a Message.

        Args:
            identifier: The identifier of the grant to send the message for.
            request_body: The request body to send the message with.

        Returns:
            The sent message.
        """
        json_response = self._http_client._execute(
            method="POST",
            path=f"/v3/grants/{identifier}/messages/send",
            data=_build_form_request(request_body),
        )

        return Response.from_dict(json_response, Message)

    def list_scheduled_messages(
        self, identifier: str
    ) -> Response[ScheduledMessagesList]:
        """
        Retrieve your scheduled messages.

        Args:
            identifier: The identifier of the grant to delete the message for.

        Returns:
            Response: The list of scheduled messages.
        """
        json_response = self._http_client._execute(
            method="GET",
            path=f"/v3/grants/{identifier}/messages/schedules",
        )

        return Response.from_dict(json_response, ScheduledMessagesList)

    def find_scheduled_messages(
        self, identifier: str, schedule_id: str
    ) -> Response[ScheduledMessage]:
        """
        Retrieve your scheduled messages.

        Args:
            identifier: The identifier of the grant to delete the message for.
            schedule_id: The id of the scheduled message to retrieve.

        Returns:
            Response: The scheduled message.
        """
        json_response = self._http_client._execute(
            method="GET",
            path=f"/v3/grants/{identifier}/messages/schedules/{schedule_id}",
        )

        return Response.from_dict(json_response, ScheduledMessage)

    def stop_scheduled_messages(
        self, identifier: str, schedule_id: str
    ) -> Response[StopScheduledMessageResponse]:
        """
        Stop a scheduled message.

        Args:
            identifier: The identifier of the grant to delete the message for.
            schedule_id: The id of the scheduled message to stop.

        Returns:
            Response: The confirmation of the stopped scheduled message.
        """
        json_response = self._http_client._execute(
            method="DELETE",
            path=f"/v3/grants/{identifier}/messages/schedules/{schedule_id}",
        )

        return Response.from_dict(json_response, StopScheduledMessageResponse)

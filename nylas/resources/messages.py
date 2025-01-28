import io
import urllib.parse
from typing import Optional, List

from nylas.config import RequestOverrides
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
    ScheduledMessage,
    StopScheduledMessageResponse,
    CleanMessagesRequest,
    CleanMessagesResponse,
)
from nylas.models.response import Response, ListResponse, DeleteResponse
from nylas.resources.smart_compose import SmartCompose
from nylas.utils.file_utils import (
    _build_form_request,
    MAXIMUM_JSON_ATTACHMENT_SIZE,
    encode_stream_to_base64,
)


class Messages(
    ListableApiResource,
    FindableApiResource,
    UpdatableApiResource,
    DestroyableApiResource,
):
    """
    Nylas Messages API

    The messages API allows you to send, find, update, and delete messages.
    You can also use the messages API to schedule messages to be sent at a later time.
    The Smart Compose API, allowing you to generate email content using machine learning, is also available.
    """

    @property
    def smart_compose(self) -> SmartCompose:
        """
        Access the Smart Compose collection of endpoints.

        Returns:
            The Smart Compose collection of endpoints.
        """
        return SmartCompose(self._http_client)

    def list(
        self,
        identifier: str,
        query_params: Optional[ListMessagesQueryParams] = None,
        overrides: RequestOverrides = None,
    ) -> ListResponse[Message]:
        """
        Return all Messages.

        Args:
            identifier: The identifier of the grant to get messages for.
            query_params: The query parameters to filter messages by.
            overrides: The request overrides to apply to the request.

        Returns:
            A list of Messages.
        """
        return super().list(
            path=f"/v3/grants/{identifier}/messages",
            response_type=Message,
            query_params=query_params,
            overrides=overrides,
        )

    def find(
        self,
        identifier: str,
        message_id: str,
        query_params: Optional[FindMessageQueryParams] = None,
        overrides: RequestOverrides = None,
    ) -> Response[Message]:
        """
        Return a Message.

        Args:
            identifier: The identifier of the grant to get the message for.
            message_id: The identifier of the message to get.
            query_params: The query parameters to include in the request.
            overrides: The request overrides to apply to the request.

        Returns:
            The requested Message.
        """
        return super().find(
            path=f"/v3/grants/{identifier}/messages/{urllib.parse.quote(message_id, safe='')}",
            response_type=Message,
            query_params=query_params,
            overrides=overrides,
        )

    def update(
        self,
        identifier: str,
        message_id: str,
        request_body: UpdateMessageRequest,
        overrides: RequestOverrides = None,
    ) -> Response[Message]:
        """
        Update a Message.

        Args:
            identifier: The identifier of the grant to update the message for.
            message_id: The identifier of the message to update.
            request_body: The request body to update the message with.
            overrides: The request overrides to apply to the request.

        Returns:
            The updated Message.
        """
        return super().update(
            path=f"/v3/grants/{identifier}/messages/{urllib.parse.quote(message_id, safe='')}",
            response_type=Message,
            request_body=request_body,
            overrides=overrides,
        )

    def destroy(
        self, identifier: str, message_id: str, overrides: RequestOverrides = None
    ) -> DeleteResponse:
        """
        Delete a Message.

        Args:
            identifier: The identifier of the grant to delete the message for.
            message_id: The identifier of the message to delete.
            overrides: The request overrides to apply to the request.

        Returns:
            The deletion response.
        """
        return super().destroy(
            path=f"/v3/grants/{identifier}/messages/{urllib.parse.quote(message_id, safe='')}",
            overrides=overrides,
        )

    def send(
        self,
        identifier: str,
        request_body: SendMessageRequest,
        overrides: RequestOverrides = None,
    ) -> Response[Message]:
        """
        Send a Message.

        Args:
            identifier: The identifier of the grant to send the message for.
            request_body: The request body to send the message with.
            overrides: The request overrides to apply to the request.

        Returns:
            The sent message.
        """
        path = f"/v3/grants/{identifier}/messages/send"
        form_data = None
        json_body = None

        # From is a reserved keyword in Python, so we need to pull the data from 'from_' instead
        request_body["from"] = request_body.get("from_", None)

        # Use form data only if the attachment size is greater than 3mb
        attachment_size = sum(
            attachment.get("size", 0)
            for attachment in request_body.get("attachments", [])
        )
        if attachment_size >= MAXIMUM_JSON_ATTACHMENT_SIZE:
            form_data = _build_form_request(request_body)
        else:
            # Encode the content of the attachments to base64
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

    def list_scheduled_messages(
        self, identifier: str, overrides: RequestOverrides = None
    ) -> Response[List[ScheduledMessage]]:
        """
        Retrieve your scheduled messages.

        Args:
            identifier: The identifier of the grant to delete the message for.
            overrides: The request overrides to apply to the request.

        Returns:
            Response: The list of scheduled messages.
        """
        json_response, headers = self._http_client._execute(
            method="GET",
            path=f"/v3/grants/{identifier}/messages/schedules",
            overrides=overrides,
        )

        data = []
        request_id = json_response["request_id"]
        for item in json_response["data"]:
            data.append(ScheduledMessage.from_dict(item))

        return Response(data, request_id, headers)

    def find_scheduled_message(
        self, identifier: str, schedule_id: str, overrides: RequestOverrides = None
    ) -> Response[ScheduledMessage]:
        """
        Retrieve your scheduled messages.

        Args:
            identifier: The identifier of the grant to delete the message for.
            schedule_id: The id of the scheduled message to retrieve.
            overrides: The request overrides to apply to the request.

        Returns:
            Response: The scheduled message.
        """
        json_response, headers = self._http_client._execute(
            method="GET",
            path=f"/v3/grants/{identifier}/messages/schedules/{schedule_id}",
            overrides=overrides,
        )

        return Response.from_dict(json_response, ScheduledMessage, headers)

    def stop_scheduled_message(
        self, identifier: str, schedule_id: str, overrides: RequestOverrides = None
    ) -> Response[StopScheduledMessageResponse]:
        """
        Stop a scheduled message.

        Args:
            identifier: The identifier of the grant to delete the message for.
            schedule_id: The id of the scheduled message to stop.
            overrides: The request overrides to apply to the request.

        Returns:
            Response: The confirmation of the stopped scheduled message.
        """
        json_response, headers = self._http_client._execute(
            method="DELETE",
            path=f"/v3/grants/{identifier}/messages/schedules/{schedule_id}",
            overrides=overrides,
        )

        return Response.from_dict(json_response, StopScheduledMessageResponse, headers)

    def clean_messages(
        self,
        identifier: str,
        request_body: CleanMessagesRequest,
        overrides: RequestOverrides = None,
    ) -> ListResponse[CleanMessagesResponse]:
        """
        Remove extra information from a list of messages.

        Args:
            identifier: The identifier of the grant to clean the message for.
            request_body: The values to clean the message with.
            overrides: The request overrides to apply to the request.

        Returns:
            ListResponse: The list of cleaned messages.
        """
        json_response, headers = self._http_client._execute(
            method="PUT",
            path=f"/v3/grants/{identifier}/messages/clean",
            request_body=request_body,
            overrides=overrides,
        )

        return ListResponse.from_dict(json_response, CleanMessagesResponse, headers)

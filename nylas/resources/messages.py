from typing import Dict, Optional
from nylas.handler.api_resources import (
    ListableApiResource,
    FindableApiResource,
    UpdatableApiResource,
    DestroyableApiResource,
)
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


class Messages(
    ListableApiResource,
    FindableApiResource,
    UpdatableApiResource,
    DestroyableApiResource,
):
    def list(
        self, identifier: str, query_params: ListMessagesQueryParams
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
        query_params: Optional[Dict] = None,
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
            query_params=query_params,
        )

    def destroy(
        self, identifier: str, message_id: str, query_params: Optional[Dict] = None
    ) -> DeleteResponse:
        """
        Delete a Message.

        Args:
            identifier: The identifier of the grant to delete the message for.
            message_id: The identifier of the message to delete.
            query_params: The query parameters to include in the request.

        Returns:
            The deletion response.
        """
        return super(Messages, self).destroy(
            path=f"/v3/grants/{identifier}/messages/{message_id}",
            query_params=query_params,
        )

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

import urllib.parse
from nylas.config import RequestOverrides
from nylas.handler.api_resources import (
    ListableApiResource,
    FindableApiResource,
    UpdatableApiResource,
    DestroyableApiResource,
)
from nylas.models.response import ListResponse, Response, DeleteResponse
from nylas.models.threads import ListThreadsQueryParams, Thread, UpdateThreadRequest


class Threads(
    ListableApiResource,
    FindableApiResource,
    UpdatableApiResource,
    DestroyableApiResource,
):
    """
    Nylas Threads API

    The threads API allows you to find, update, and delete threads.
    """

    def list(
        self,
        identifier: str,
        query_params: ListThreadsQueryParams = None,
        overrides: RequestOverrides = None,
    ) -> ListResponse[Thread]:
        """
        Return all Threads.

        Args:
            identifier: The identifier of the grant to get threads for.
            query_params: The query parameters to filter threads by.
            overrides: The request overrides to apply to the request.

        Returns:
            A list of Threads.
        """
        return super().list(
            path=f"/v3/grants/{identifier}/threads",
            response_type=Thread,
            query_params=query_params,
            overrides=overrides,
        )

    def find(
        self, identifier: str, thread_id: str, overrides: RequestOverrides = None
    ) -> Response[Thread]:
        """
        Return a Thread.

        Args:
            identifier: The identifier of the grant to get the thread for.
            thread_id: The identifier of the thread to get.
            overrides: The request overrides to apply to the request.

        Returns:
            The requested Thread.
        """
        return super().find(
            path=f"/v3/grants/{identifier}/threads/{urllib.parse.quote(thread_id, safe='')}",
            response_type=Thread,
            overrides=overrides,
        )

    def update(
        self,
        identifier: str,
        thread_id: str,
        request_body: UpdateThreadRequest,
        overrides: RequestOverrides = None,
    ) -> Response[Thread]:
        """
        Update a Thread.

        Args:
            identifier: The identifier of the grant to update the thread for.
            thread_id: The identifier of the thread to update.
            request_body: The request body to update the thread with.
            overrides: The request overrides to apply to the request.

        Returns:
            The updated Thread.
        """
        return super().update(
            path=f"/v3/grants/{identifier}/threads/{urllib.parse.quote(thread_id, safe='')}",
            response_type=Thread,
            request_body=request_body,
            overrides=overrides,
        )

    def destroy(
        self, identifier: str, thread_id: str, overrides: RequestOverrides = None
    ) -> DeleteResponse:
        """
        Delete a Thread.

        Args:
            identifier: The identifier of the grant to delete the thread for.
            thread_id: The identifier of the thread to delete.
            overrides: The request overrides to apply to the request.

        Returns:
            The deletion response.
        """
        return super().destroy(
            path=f"/v3/grants/{identifier}/threads/{urllib.parse.quote(thread_id, safe='')}",
            overrides=overrides,
        )

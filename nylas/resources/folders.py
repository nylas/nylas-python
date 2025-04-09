from typing import Optional

from nylas.config import RequestOverrides
from nylas.handler.api_resources import (
    ListableApiResource,
    FindableApiResource,
    CreatableApiResource,
    UpdatableApiResource,
    DestroyableApiResource,
)
from nylas.models.folders import (
    Folder,
    CreateFolderRequest,
    UpdateFolderRequest,
    ListFolderQueryParams,
    FindFolderQueryParams,
)
from nylas.models.response import Response, ListResponse, DeleteResponse


class Folders(
    ListableApiResource,
    FindableApiResource,
    CreatableApiResource,
    UpdatableApiResource,
    DestroyableApiResource,
):
    """
    Nylas Folders API

    The Nylas folders API allows you to create new folders or manage existing ones.
    """

    def list(
        self,
        identifier: str,
        query_params: Optional[ListFolderQueryParams] = None,
        overrides: RequestOverrides = None,
    ) -> ListResponse[Folder]:
        """
        Return all Folders.

        Args:
            identifier: The identifier of the Grant to act upon.
            query_params: The query parameters to include in the request.
            overrides: The request overrides to use.

        Returns:
            The list of Folders.
        """

        return super().list(
            path=f"/v3/grants/{identifier}/folders",
            response_type=Folder,
            query_params=query_params,
            overrides=overrides,
        )

    def find(
        self,
        identifier: str,
        folder_id: str,
        overrides: RequestOverrides = None,
        query_params: FindFolderQueryParams = None,
    ) -> Response[Folder]:
        """
        Return a Folder.

        Args:
            identifier: The identifier of the Grant to act upon.
            folder_id: The ID of the Folder to retrieve.
            overrides: The request overrides to use.
            query_params: The query parameters to include in the request.

        Returns:
            The Folder.
        """
        return super().find(
            path=f"/v3/grants/{identifier}/folders/{folder_id}",
            response_type=Folder,
            query_params=query_params,
            overrides=overrides,
        )

    def create(
        self,
        identifier: str,
        request_body: CreateFolderRequest,
        overrides: RequestOverrides = None,
    ) -> Response[Folder]:
        """
        Create a Folder.

        Args:
            identifier: The identifier of the Grant to act upon.
            request_body: The values to create the Folder with.
            overrides: The request overrides to use.

        Returns:
            The created Folder.
        """
        return super().create(
            path=f"/v3/grants/{identifier}/folders",
            response_type=Folder,
            request_body=request_body,
            overrides=overrides,
        )

    def update(
        self,
        identifier: str,
        folder_id: str,
        request_body: UpdateFolderRequest,
        overrides: RequestOverrides = None,
    ) -> Response[Folder]:
        """
        Update a Folder.

        Args:
            identifier: The identifier of the Grant to act upon.
            folder_id: The ID of the Folder to update.
            request_body: The values to update the Folder with.
            overrides: The request overrides to use.

        Returns:
            The updated Folder.
        """
        return super().update(
            path=f"/v3/grants/{identifier}/folders/{folder_id}",
            response_type=Folder,
            request_body=request_body,
            overrides=overrides,
        )

    def destroy(
        self,
        identifier: str,
        folder_id: str,
        overrides: RequestOverrides = None,
    ) -> DeleteResponse:
        """
        Delete a Folder.

        Args:
            identifier: The identifier of the Grant to act upon.
            folder_id: The ID of the Folder to delete.
            overrides: The request overrides to use.

        Returns:
            The deletion response.
        """
        return super().destroy(
            path=f"/v3/grants/{identifier}/folders/{folder_id}", overrides=overrides
        )

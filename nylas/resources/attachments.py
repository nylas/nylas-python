from requests import Response

from nylas.config import RequestOverrides
from nylas.handler.api_resources import (
    FindableApiResource,
)
from nylas.models.attachments import Attachment, FindAttachmentQueryParams
from nylas.models.response import Response as NylasResponse


class Attachments(
    FindableApiResource,
):
    """
    Nylas Attachments API

    The Nylas Attachments API allows you to get metadata ot, and download attachments from messages.
    """

    def find(
        self,
        identifier: str,
        attachment_id: str,
        query_params: FindAttachmentQueryParams,
        overrides: RequestOverrides = None,
    ) -> NylasResponse[Attachment]:
        """
        Return metadata of an attachment.

        Args:
            identifier: The identifier of the Grant to act upon.
            attachment_id: The id of the attachment to retrieve.
            query_params: The query parameters to include in the request.
            overrides: The request overrides to use for the request.

        Returns:
            The attachment metadata.
        """
        return super().find(
            path=f"/v3/grants/{identifier}/attachments/{attachment_id}",
            response_type=Attachment,
            query_params=query_params,
            overrides=overrides,
        )

    def download(
        self,
        identifier: str,
        attachment_id: str,
        query_params: FindAttachmentQueryParams,
        overrides: RequestOverrides = None,
    ) -> Response:
        """
        Download the attachment data.

        This function returns a raw response object to allow you the ability
        to stream the file contents. The response object should be closed
        after use to ensure the connection is closed.

        Args:
            identifier: The identifier of the Grant to act upon.
            attachment_id: The id of the attachment to download.
            query_params: The query parameters to include in the request.
            overrides: The request overrides to use for the request.

        Returns:
            The Response object containing the file data.

        Example:
            Here is an example of how to use this function when streaming:

            ```python
                response = execute_request_raw_response(url, method, stream=True)
                try:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            # Process each chunk
                            pass
                finally:
                    response.close()  # Ensure the response is closed
            ```
        """
        return self._http_client._execute_download_request(
            path=f"/v3/grants/{identifier}/attachments/{attachment_id}/download",
            query_params=query_params,
            stream=True,
            overrides=overrides,
        )

    def download_bytes(
        self,
        identifier: str,
        attachment_id: str,
        query_params: FindAttachmentQueryParams,
        overrides: RequestOverrides = None,
    ) -> bytes:
        """
        Download the attachment as a byte array.

        Args:
            identifier: The identifier of the Grant to act upon.
            attachment_id: The id of the attachment to download.
            query_params: The query parameters to include in the request.
            overrides: The request overrides to use for the request.

        Returns:
            The raw file data.
        """
        return self._http_client._execute_download_request(
            path=f"/v3/grants/{identifier}/attachments/{attachment_id}/download",
            query_params=query_params,
            stream=False,
            overrides=overrides,
        )

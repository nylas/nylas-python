from requests import Response

from nylas.config import RequestOverrides
from nylas.handler.api_resources import (
    FindableApiResource,
    CreatableApiResource,
)
from nylas.models.attachments import (
    Attachment,
    FindAttachmentQueryParams,
    CreateAttachmentUploadSessionRequest,
    AttachmentUploadSession,
    AttachmentUploadSessionComplete,
)
from nylas.models.response import Response as NylasResponse


class Attachments(
    FindableApiResource,
    CreatableApiResource,
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

    def create_upload_session(
        self,
        identifier: str,
        request_body: CreateAttachmentUploadSessionRequest,
        overrides: RequestOverrides = None,
    ) -> NylasResponse[AttachmentUploadSession]:
        """
        Create a resumable upload session for a large attachment (up to 150 MB).

        After receiving the session, upload file bytes via HTTP PUT to the returned
        `url` (include the returned `headers`; no Nylas auth header needed), then
        call complete_upload_session() with the returned `attachment_id`.

        Args:
            identifier: The identifier of the Grant to act upon.
            request_body: Session parameters (filename, content_type, optional size).
            overrides: The request overrides to use for the request.

        Returns:
            The upload session, including the pre-signed URL and attachment_id.
        """
        return super().create(
            path=f"/v3/grants/{identifier}/attachment-uploads",
            response_type=AttachmentUploadSession,
            request_body=request_body,
            overrides=overrides,
        )

    def complete_upload_session(
        self,
        identifier: str,
        attachment_id: str,
        overrides: RequestOverrides = None,
    ) -> NylasResponse[AttachmentUploadSessionComplete]:
        """
        Complete an upload session after file bytes have been PUT to the pre-signed URL.

        Use the `attachment_id` from the completed session when referencing the
        attachment in a subsequent messages.send() or drafts.create() call.

        Args:
            identifier: The identifier of the Grant to act upon.
            attachment_id: The upload session ID returned by create_upload_session().
            overrides: The request overrides to use for the request.

        Returns:
            The completed session status.
        """
        return super().create(
            path=f"/v3/grants/{identifier}/attachment-uploads/{attachment_id}/complete",
            response_type=AttachmentUploadSessionComplete,
            request_body={},
            overrides=overrides,
        )

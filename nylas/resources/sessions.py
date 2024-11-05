from nylas.config import RequestOverrides
from nylas.handler.api_resources import CreatableApiResource, DestroyableApiResource
from nylas.models.response import DeleteResponse, Response
from nylas.models.scheduler import CreateSessionRequest, Session


class Sessions(CreatableApiResource, DestroyableApiResource):
    """
    Nylas Sessions API

    The Nylas Sessions API allows you to create new sessions or manage existing ones.
    """

    def create(
        self,
        request_body: CreateSessionRequest,
        overrides: RequestOverrides = None,
    ) -> Response[Session]:
        """
        Create a Session.

        Args:
          request_body: The request body to create the Session.
          overrides: The request overrides to use for the request.

        Returns:
          The Session.
        """

        return super().create(
            path="/v3/scheduling/sessions",
            request_body=request_body,
            response_type=Session,
            overrides=overrides,
        )

    def destroy(
        self,
        session_id: str,
        overrides: RequestOverrides = None,
    ) -> DeleteResponse:
        """
        Destroy a Session.

        Args:
          session_id: The identifier of the Session to destroy.
          overrides: The request overrides to use for the request.

        Returns:
          None.
        """

        return super().destroy(
            path=f"/v3/scheduling/sessions/{session_id}",
            overrides=overrides,
        )

from nylas.config import RequestOverrides
from nylas.resources.credentials import Credentials

from nylas.handler.api_resources import (
    ListableApiResource,
    FindableApiResource,
    CreatableApiResource,
    UpdatableApiResource,
    DestroyableApiResource,
)
from nylas.models.auth import Provider
from nylas.models.connectors import (
    ListConnectorQueryParams,
    Connector,
    CreateConnectorRequest,
    UpdateConnectorRequest,
)
from nylas.models.response import ListResponse, Response, DeleteResponse


class Connectors(
    ListableApiResource,
    FindableApiResource,
    CreatableApiResource,
    UpdatableApiResource,
    DestroyableApiResource,
):
    """
    Nylas Connectors API

    The Nylas Connectors API allows you to create new connectors or manage existing ones.
    In Nylas, a connector (formerly called an "integration") stores information that allows your Nylas application
    to connect to a third party services
    """

    @property
    def credentials(self) -> Credentials:
        """
        Access the Credentials API.

        Returns:
            The Credentials API.
        """
        return Credentials(self._http_client)

    def list(
        self,
        query_params: ListConnectorQueryParams = None,
        overrides: RequestOverrides = None,
    ) -> ListResponse[Connector]:
        """
        Return all Connectors.

        Args:
            query_params: The query parameters to include in the request.
            overrides: The request overrides to use.

        Returns:
            The list of Connectors.
        """

        return super().list(
            path="/v3/connectors",
            response_type=Connector,
            query_params=query_params,
            overrides=overrides,
        )

    def find(
        self, provider: Provider, overrides: RequestOverrides = None
    ) -> Response[Connector]:
        """
        Return a connector associated with the provider.

        Args:
            provider: The provider associated to the connector to retrieve.
            overrides: The request overrides to use.

        Returns:
            The Connector.
        """
        return super().find(
            path=f"/v3/connectors/{provider}",
            response_type=Connector,
            overrides=overrides,
        )

    def create(
        self, request_body: CreateConnectorRequest, overrides: RequestOverrides = None
    ) -> Response[Connector]:
        """
        Create a connector.

        Args:
            request_body: The values to create the connector with.
            overrides: The request overrides to use.

        Returns:
            The created connector.
        """
        return super().create(
            path="/v3/connectors",
            request_body=request_body,
            response_type=Connector,
            overrides=overrides,
        )

    def update(
        self,
        provider: Provider,
        request_body: UpdateConnectorRequest,
        overrides: RequestOverrides = None,
    ) -> Response[Connector]:
        """
        Create a connector.

        Args:
            provider: The provider associated to the connector to update.
            request_body: The values to update the connector with.
            overrides: The request overrides to use.

        Returns:
            The created connector.
        """
        return super().update(
            path=f"/v3/connectors/{provider}",
            request_body=request_body,
            response_type=Connector,
            method="PATCH",
            overrides=overrides,
        )

    def destroy(
        self, provider: Provider, overrides: RequestOverrides = None
    ) -> DeleteResponse:
        """
        Delete a connector.

        Args:
            provider: The provider associated to the connector to delete.
            overrides: The request overrides to use.

        Returns:
            The deleted connector.
        """
        return super().destroy(path=f"/v3/connectors/{provider}", overrides=overrides)

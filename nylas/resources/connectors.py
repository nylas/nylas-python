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
    @property
    def credentials(self) -> Credentials:
        """
        Access the Credentials API.

        Returns:
            The Credentials API.
        """
        return Credentials(self._http_client)

    def list(
        self, query_params: ListConnectorQueryParams = None
    ) -> ListResponse[Connector]:
        """
        Return all Connectors.

        Args:
            query_params: The query parameters to include in the request.

        Returns:
            The list of Connectors.
        """

        return super(Connectors, self).list(
            path="/v3/connectors", response_type=Connector, query_params=query_params
        )

    def find(self, provider: Provider) -> Response[Connector]:
        """
        Return a connector associated with the provider.

        Args:
            provider: The provider associated to the connector to retrieve.

        Returns:
            The Connector.
        """
        return super(Connectors, self).find(
            path=f"/v3/connectors/{provider}",
            response_type=Connector,
        )

    def create(self, request_body: CreateConnectorRequest) -> Response[Connector]:
        """
        Create a connector.

        Args:
            request_body: The values to create the connector with.

        Returns:
            The created connector.
        """
        return super(Connectors, self).create(
            path=f"/v3/connectors",
            request_body=request_body,
            response_type=Connector,
        )

    def update(
        self, provider: Provider, request_body: UpdateConnectorRequest
    ) -> Response[Connector]:
        """
        Create a connector.

        Args:
            provider: The provider associated to the connector to update.
            request_body: The values to update the connector with.

        Returns:
            The created connector.
        """
        return super(Connectors, self).update(
            path=f"/v3/connectors/{provider}",
            request_body=request_body,
            response_type=Connector,
            method="PATCH",
        )

    def destroy(self, provider: Provider) -> DeleteResponse:
        """
        Delete a connector.

        Args:
            provider: The provider associated to the connector to delete.

        Returns:
            The deleted connector.
        """
        return super(Connectors, self).destroy(path=f"/v3/connectors/{provider}")

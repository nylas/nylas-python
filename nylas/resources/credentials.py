from nylas.config import RequestOverrides
from nylas.handler.api_resources import (
    ListableApiResource,
    FindableApiResource,
    CreatableApiResource,
    UpdatableApiResource,
    DestroyableApiResource,
)
from nylas.models.auth import Provider
from nylas.models.credentials import (
    Credential,
    CredentialRequest,
    ListCredentialQueryParams,
    UpdateCredentialRequest,
)
from nylas.models.response import Response, ListResponse, DeleteResponse


class Credentials(
    ListableApiResource,
    FindableApiResource,
    CreatableApiResource,
    UpdatableApiResource,
    DestroyableApiResource,
):
    """
    Nylas Credentials API


    A Nylas connector credential is a special type of record that securely stores information
    that allows you to connect using an administrator account
    """

    def list(
        self,
        provider: Provider,
        query_params: ListCredentialQueryParams = None,
        overrides: RequestOverrides = None,
    ) -> ListResponse[Credential]:
        """
        Return all credentials for a particular provider.

        Args:
            provider: The provider.
            query_params: The query parameters to include in the request.
            overrides: The request overrides to use for the request.

        Returns:
            The list of credentials.
        """

        return super().list(
            path=f"/v3/connectors/{provider}/creds",
            response_type=Credential,
            query_params=query_params,
            overrides=overrides,
        )

    def find(
        self,
        provider: Provider,
        credential_id: str,
        overrides: RequestOverrides = None,
    ) -> Response[Credential]:
        """
        Return a credential.

        Args:
            provider: The provider of the credential.
            credential_id: The ID of the credential to retrieve.
            overrides: The request overrides to use for the request.

        Returns:
            The Credential.
        """

        return super().find(
            path=f"/v3/connectors/{provider}/creds/{credential_id}",
            response_type=Credential,
            overrides=overrides,
        )

    def create(
        self,
        provider: Provider,
        request_body: CredentialRequest,
        overrides: RequestOverrides = None,
    ) -> Response[Credential]:
        """
        Create a credential for a particular provider.

        Args:
            provider: The provider.
            request_body: The values to create the Credential with.
            overrides: The request overrides to use for the request.

        Returns:
            The created Credential.
        """

        return super().create(
            path=f"/v3/connectors/{provider}/creds",
            response_type=Credential,
            request_body=request_body,
            overrides=overrides,
        )

    def update(
        self,
        provider: Provider,
        credential_id: str,
        request_body: UpdateCredentialRequest,
        overrides: RequestOverrides = None,
    ) -> Response[Credential]:
        """
        Update a credential.

        Args:
            provider: The provider.
            credential_id: The ID of the credential to update.
            request_body: The values to update the credential with.
            overrides: The request overrides to use for the request.

        Returns:
            The updated credential.
        """

        return super().update(
            path=f"/v3/connectors/{provider}/creds/{credential_id}",
            response_type=Credential,
            request_body=request_body,
            method="PATCH",
            overrides=overrides,
        )

    def destroy(
        self,
        provider: Provider,
        credential_id: str,
        overrides: RequestOverrides = None,
    ) -> DeleteResponse:
        """
        Delete a credential.

        Args:
            provider: the provider for the grant
            credential_id: The ID of the credential to delete.
            overrides: The request overrides to use for the request.

        Returns:
            The deletion response.
        """

        return super().destroy(
            path=f"/v3/connectors/{provider}/creds/{credential_id}", overrides=overrides
        )

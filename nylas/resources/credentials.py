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
    CredentialRequest, ListCredentialQueryParams
)
from nylas.models.response import Response, ListResponse, DeleteResponse


class Credentials(
    ListableApiResource,
    FindableApiResource,
    CreatableApiResource,
    UpdatableApiResource,
    DestroyableApiResource,
):
    def list(self, provider: Provider, query_params: ListCredentialQueryParams) -> ListResponse[Credential]:
        """
        Return all credentials for a particular provider.

        Args:
            provider: The provider.
            query_params: The query parameters to include in the request.

        Returns:
            The list of credentials.
        """

        return super(Credentials, self).list(path=f"/v3/connectors/{provider}/creds", response_type=Credential,
                                             query_params=query_params)

    def find(self, provider: Provider, credential_id: str) -> Response[Credential]:
        """
        Return a credential.

        Args:
            provider: The provider of the credential.
            credential_id: The ID of the credential to retrieve.

        Returns:
            The Credential.
        """

        return super(Credentials, self).find(
            path=f"/v3/connectors/{provider}/creds/{credential_id}", response_type=Credential
        )

    def create(self, request_body: CredentialRequest) -> Response[Credential]:
        """
        Create a credential for a particular provider.

        Args:
            request_body: The values to create the Credential with.

        Returns:
            The created Credential.
        """

        return super(Credentials, self).create(
            path=f"/v3/connectors/{request_body.get('provider')}/creds", response_type=Credential, request_body=request_body
        )

    def update(self, credential_id: str, request_body: CredentialRequest) -> Response[Credential]:
        """
        Update a credential.

        Args:
            credential_id: The ID of the credential to update.
            request_body: The values to update the credential with.

        Returns:
            The updated credential.
        """

        return super(Credentials, self).update(
            path=f"/v3/connectors/{request_body.get('provider')}/creds/{credential_id}", response_type=Credential,
            request_body=request_body
        )

    def destroy(self, provider: Provider, credential_id: str) -> DeleteResponse[Credential]:
        """
        Delete a credential.

        Args:
            provider: the provider for the grant
            credential_id: The ID of the credential to delete.

        Returns:
            The deletion response.
        """

        return super(Credentials, self).destroy(path=f"/v3/connectors/{provider}/creds/{credential_id}")

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
        return super(Credentials, self).list(path=f"/v3/connectors/{provider}/creds", response_type=Credential,
                                             query_params=query_params)

    def find(self, provider: Provider, credential_id: str) -> Response[Credential]:
        return super(Credentials, self).find(
            path=f"/v3/connectors/{provider}/creds/{credential_id}", response_type=Credential
        )

    def create(self, request_body: CredentialRequest) -> Response[Credential]:
        return super(Credentials, self).create(
            path=f"/v3/connectors/microsoft/creds", response_type=Credential, request_body=request_body
        )

    def update(self, credential_id: str, request_body: CredentialRequest) -> Response[Credential]:
        return super(Credentials, self).update(
            path=f"/v3/connectors/{request_body.get('provider')}/creds/{credential_id}", response_type=Credential,
            request_body=request_body
        )

    def destroy(self, provider: Provider, credential_id: str) -> DeleteResponse[Credential]:
        return super(Credentials, self).destroy(path=f"/v3/connectors/{provider}/creds/{credential_id}")

from dataclasses import dataclass
from type import List, Any, Dict, Optional, Literal, Union, NotRequired

from dataclasses_json import dataclass_json
from typing_extensions import TypedDict


CredentialType = Literal["adminconsent", "serviceaccount", "connector"]

@dataclass_json
@dataclass
class Credential:
    """
    Interface representing a Nylas Credential object.
    Attributes
    id: Globally unique object identifier;
    name: Name of the credential
    credential_type: The type of credential
    hashed_data: Hashed value of the credential that you created
    created_at: Timestamp of when the credential was created
    updated_at: Timestamp of when the credential was updated;
    """
    id: str
    name: str
    credential_type: Optional[CredentialType]
    hashed_data: Optional[str] = None
    created_at: Optional[int] = None
    updated_at: Optional[int] = None


class MicrosoftAdminConsentSettings(TypedDict):
    client_id: str
    client_secret: str


class CreateCredentialBaseRequest(TypedDict):
    """
        Interface representing a request to create a credential.

        Attributes:
            provider: OAuth provider.
            settings: Settings required to create a credential
            credential_type: Type of credential you want to create.
            credential_data: The data required to successfully create the credential object
    """
    provider: str
    name: Optional[str]
    credential_type: CredentialType


class GoogleServiceAccountCredential(CreateCredentialBaseRequest):
    credential_data: Dict[str, any]


class AdminConsentCredential(CreateCredentialBaseRequest):
    credential_data: MicrosoftAdminConsentSettings


class ConnectorOverrideCredential(CreateCredentialBaseRequest):
    credential_data: Dict[str, any]


class ListCredentialQueryParams(TypedDict):
    """
    Interface representing the query parameters for credentials .

    Attributes:
        offset: Offset results
        sort_by: Sort entries by field name
        order_by: Order results by the specified field.
            Currently only start is supported.
        limit: The maximum number of objects to return.
            This field defaults to 50. The maximum allowed value is 200.
    """

    limit: NotRequired[int]
    offset: NotRequired[int]
    order_by: NotRequired[str]
    sort_by: NotRequired[str]


CredentialRequest = Union[AdminConsentCredential, GoogleServiceAccountCredential, ConnectorOverrideCredential]

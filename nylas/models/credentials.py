from dataclasses import dataclass
from typing import Dict, Optional, Literal, Union

from dataclasses_json import dataclass_json
from typing_extensions import TypedDict, Protocol, NotRequired

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
    credential_type: Optional[CredentialType] = None
    hashed_data: Optional[str] = None
    created_at: Optional[int] = None
    updated_at: Optional[int] = None


class MicrosoftAdminConsentSettings(Protocol):
    client_id: str
    client_secret: str


class GoogleServiceAccountCredential(Protocol):
    private_key_id: str
    private_key: str
    client_email: str


CredentialData = Union[MicrosoftAdminConsentSettings, GoogleServiceAccountCredential, Dict[str, any]]


class CredentialRequest(TypedDict):
    """
        Interface representing a request to create a credential.

        Attributes:
            name: Name of the credential
            credential_type: Type of credential you want to create.
            credential_data: The data required to successfully create the credential object
    """
    name: Optional[str]
    credential_type: CredentialType
    credential_data: CredentialData

class UpdateCredentialRequest(TypedDict):
    """
    Interface representing a request to update a credential.

    Attributes:
        name: Name of the credential
        credential_data: The data required to successfully create the credential object
    """
    name: Optional[str]
    credential_data: Optional[CredentialData]

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

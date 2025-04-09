from dataclasses import dataclass
from enum import Enum
from typing import Optional, List
from typing_extensions import TypedDict, NotRequired

from dataclasses_json import dataclass_json

from nylas.models.list_query_params import ListQueryParams


class SourceType(str, Enum):
    """Enum representing the different types of sources for a contact."""

    ADDRESS_BOOK = "address_book"
    INBOX = "inbox"
    DOMAIN = "domain"


@dataclass_json
@dataclass
class PhoneNumber:
    """
    A phone number for a contact.

    Attributes:
        number: The phone number.
        type: The type of phone number.
    """

    number: Optional[str] = None
    type: Optional[str] = None


@dataclass_json
@dataclass
class PhysicalAddress:
    """
    A physical address for a contact.

    Attributes:
        format: The format of the address.
        street_address: The street address of the contact.
        city: The city of the contact.
        postal_code: The postal code of the contact.
        state: The state of the contact.
        country: The country of the contact.
        type: The type of address.
    """

    format: Optional[str] = None
    street_address: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    type: Optional[str] = None


@dataclass_json
@dataclass
class WebPage:
    """
    A web page for a contact.

    Attributes:
        url: The URL of the web page.
        type: The type of web page.
    """

    url: Optional[str] = None
    type: Optional[str] = None


@dataclass_json
@dataclass
class ContactEmail:
    """
    An email address for a contact.

    Attributes:
        email: The email address.
        type: The type of email address.
    """

    email: Optional[str] = None
    type: Optional[str] = None


@dataclass_json
@dataclass
class ContactGroupId:
    """
    A contact group ID for a contact.

    Attributes:
        id: The contact group ID.
    """

    id: str


@dataclass_json
@dataclass
class InstantMessagingAddress:
    """
    An instant messaging address for a contact.

    Attributes:
        im_address: The instant messaging address.
        type: The type of instant messaging address.
    """

    im_address: Optional[str] = None
    type: Optional[str] = None


@dataclass_json
@dataclass
class Contact:
    """
    Class representation of a Nylas contact object.

    Attributes:
        id: Globally unique object identifier.
        grant_id: Grant ID representing the user's account.
        object: The type of object.
        birthday: The contact's birthday.
        company_name: The contact's company name.
        display_name: The contact's display name.
        emails: The contact's email addresses.
        im_addresses: The contact's instant messaging addresses.
        given_name: The contact's given name.
        job_title: The contact's job title.
        manager_name: The contact's manager name.
        middle_name: The contact's middle name.
        nickname: The contact's nickname.
        notes: The contact's notes.
        office_location: The contact's office location.
        picture_url: The contact's picture URL.
        picture: The contact's picture.
        suffix: The contact's suffix.
        surname: The contact's surname.
        source: The contact's source.
        phone_numbers: The contact's phone numbers.
        physical_addresses: The contact's physical addresses.
        web_pages: The contact's web pages.
        groups: The contact's groups.
    """

    id: str
    grant_id: str
    object: str = "contact"
    birthday: Optional[str] = None
    company_name: Optional[str] = None
    display_name: Optional[str] = None
    emails: Optional[List[ContactEmail]] = None
    im_addresses: Optional[List[InstantMessagingAddress]] = None
    given_name: Optional[str] = None
    job_title: Optional[str] = None
    manager_name: Optional[str] = None
    middle_name: Optional[str] = None
    nickname: Optional[str] = None
    notes: Optional[str] = None
    office_location: Optional[str] = None
    picture_url: Optional[str] = None
    picture: Optional[str] = None
    suffix: Optional[str] = None
    surname: Optional[str] = None
    source: Optional[SourceType] = None
    phone_numbers: Optional[List[PhoneNumber]] = None
    physical_addresses: Optional[List[PhysicalAddress]] = None
    web_pages: Optional[List[WebPage]] = None
    groups: Optional[List[ContactGroupId]] = None


class FindContactQueryParams(TypedDict):
    """
    The available query parameters for finding a contact.
    Attributes:
        profile_picture: If true and picture_url is present, the response includes a Base64 binary data blob that
            you can use to view information as an image file.
        select: Comma-separated list of fields to return in the response.
            This allows you to receive only the portion of object data that you're interested in.
    """

    profile_picture: NotRequired[bool]
    select: NotRequired[str]


class WriteablePhoneNumber(TypedDict):
    """
    A phone number for a contact.

    Attributes:
        number: The phone number.
        type: The type of phone number.
    """

    number: NotRequired[str]
    type: NotRequired[str]


class WriteablePhysicalAddress(TypedDict):
    """
    A physical address for a contact.

    Attributes:
        format: The format of the address.
        street_address: The street address of the contact.
        city: The city of the contact.
        postal_code: The postal code of the contact.
        state: The state of the contact.
        country: The country of the contact.
        type: The type of address.
    """

    format: NotRequired[str]
    street_address: NotRequired[str]
    city: NotRequired[str]
    postal_code: NotRequired[str]
    state: NotRequired[str]
    country: NotRequired[str]
    type: NotRequired[str]


class WriteableWebPage(TypedDict):
    """
    A web page for a contact.

    Attributes:
        url: The URL of the web page.
        type: The type of web page.
    """

    url: NotRequired[str]
    type: NotRequired[str]


class WriteableContactEmail(TypedDict):
    """
    An email address for a contact.

    Attributes:
        email: The email address.
        type: The type of email address.
    """

    email: NotRequired[str]
    type: NotRequired[str]


class WriteableContactGroupId(TypedDict):
    """
    A contact group ID for a contact.

    Attributes:
        id: The contact group ID.
    """

    id: str


class WriteableInstantMessagingAddress(TypedDict):
    """
    An instant messaging address for a contact.

    Attributes:
        im_address: The instant messaging address.
        type: The type of instant messaging address.
    """

    im_address: NotRequired[str]
    type: NotRequired[str]


class CreateContactRequest(TypedDict):
    """
    Interface for creating a Nylas contact.

    Attributes:
        birthday: The contact's birthday.
        company_name: The contact's company name.
        display_name: The contact's display name.
        emails: The contact's email addresses.
        im_addresses: The contact's instant messaging addresses.
        given_name: The contact's given name.
        job_title: The contact's job title.
        manager_name: The contact's manager name.
        middle_name: The contact's middle name.
        nickname: The contact's nickname.
        notes: The contact's notes.
        office_location: The contact's office location.
        picture_url: The contact's picture URL.
        picture: The contact's picture.
        suffix: The contact's suffix.
        surname: The contact's surname.
        source: The contact's source.
        phone_numbers: The contact's phone numbers.
        physical_addresses: The contact's physical addresses.
        web_pages: The contact's web pages.
        groups: The contact's groups.
    """

    birthday: NotRequired[str]
    company_name: NotRequired[str]
    display_name: NotRequired[str]
    emails: NotRequired[List[WriteableContactEmail]]
    im_addresses: NotRequired[List[WriteableInstantMessagingAddress]]
    given_name: NotRequired[str]
    job_title: NotRequired[str]
    manager_name: NotRequired[str]
    middle_name: NotRequired[str]
    nickname: NotRequired[str]
    notes: NotRequired[str]
    office_location: NotRequired[str]
    picture_url: NotRequired[str]
    picture: NotRequired[str]
    suffix: NotRequired[str]
    surname: NotRequired[str]
    source: NotRequired[SourceType]
    phone_numbers: NotRequired[List[WriteablePhoneNumber]]
    physical_addresses: NotRequired[List[WriteablePhysicalAddress]]
    web_pages: NotRequired[List[WriteableWebPage]]
    groups: NotRequired[List[WriteableContactGroupId]]


UpdateContactRequest = CreateContactRequest
"""Interface for updating a Nylas contact."""


class ListContactsQueryParams(ListQueryParams):
    """
    Interface representing the query parameters for listing contacts.

    Attributes:
        email: Return contacts with matching email address.
        phone_number: Return contacts with matching phone number.
        source: Return contacts from a specific source.
        group: Return contacts from a specific group.
        recurse: Return contacts from all sub-groups of the specified group.
        select (NotRequired[str]): Comma-separated list of fields to return in the response.
            This allows you to receive only the portion of object data that you're interested in.
        limit (NotRequired[int]): The maximum number of objects to return.
            This field defaults to 50. The maximum allowed value is 200.
        page_token (NotRequired[str]): An identifier that specifies which page of data to return.
            This value should be taken from a ListResponse object's next_cursor parameter.
    """

    email: NotRequired[str]
    phone_number: NotRequired[str]
    source: NotRequired[SourceType]
    group: NotRequired[str]
    recurse: NotRequired[bool]


class GroupType(str, Enum):
    """Enum representing the different types of contact groups."""

    USER = "user"
    SYSTEM = "system"
    OTHER = "other"


@dataclass_json
@dataclass
class ContactGroup:
    """
    Class representation of a Nylas contact group object.

    Attributes:
        id: Globally unique object identifier.
        grant_id: Grant ID representing the user's account.
        object: The type of object.
        group_type: The type of contact group.
        name: The name of the contact group.
        path: The path of the contact group.
    """

    id: str
    grant_id: str
    object: str = "contact_group"
    group_type: Optional[GroupType] = None
    name: Optional[str] = None
    path: Optional[str] = None


ListContactGroupsQueryParams = ListQueryParams
"""The available query parameters for listing contact groups."""

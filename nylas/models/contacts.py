from dataclasses import dataclass
from enum import Enum
from typing import Optional, List
from typing_extensions import TypedDict, NotRequired

from dataclasses_json import dataclass_json


class ContactType(str, Enum):
    work = "work"
    home = "home"
    other = "other"


class SourceType(str, Enum):
    address_book = "address_book"
    inbox = "inbox"
    domain = "domain"


@dataclass_json
@dataclass
class PhoneNumber:
    number: Optional[str] = None
    type: Optional[ContactType] = None


@dataclass_json
@dataclass
class PhysicalAddress:
    format: Optional[str] = None
    street_address: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    type: Optional[ContactType] = None


@dataclass_json
@dataclass
class WebPage:
    url: Optional[str] = None
    type: Optional[ContactType] = None


@dataclass_json
@dataclass
class ContactEmail:
    email: Optional[str] = None
    type: Optional[ContactType] = None


@dataclass_json
@dataclass
class ContactGroupId:
    id: str


@dataclass_json
@dataclass
class InstantMessagingAddress:
    im_address: Optional[str] = None
    type: Optional[ContactType] = None


@dataclass_json
@dataclass
class Contact:
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


class WriteablePhoneNumber(TypedDict):
    number: NotRequired[str]
    type: NotRequired[ContactType]


class WriteablePhysicalAddress(TypedDict):
    format: NotRequired[str]
    street_address: NotRequired[str]
    city: NotRequired[str]
    postal_code: NotRequired[str]
    state: NotRequired[str]
    country: NotRequired[str]
    type: NotRequired[ContactType]


class WriteableWebPage(TypedDict):
    url: NotRequired[str]
    type: NotRequired[ContactType]


class WriteableContactEmail(TypedDict):
    email: NotRequired[str]
    type: NotRequired[ContactType]


class WriteableContactGroupId(TypedDict):
    id: str


class WriteableInstantMessagingAddress(TypedDict):
    im_address: NotRequired[str]
    type: NotRequired[ContactType]


class CreateContactRequest(TypedDict):
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

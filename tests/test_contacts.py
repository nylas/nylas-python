import json
from datetime import date
import pytest
from six import binary_type
from nylas.client.restful_models import Contact


@pytest.mark.usefixtures("mock_contacts")
def test_list_contacts(api_client):
    contacts = list(api_client.contacts)
    assert len(contacts) == 3
    assert all(isinstance(x, Contact) for x in contacts)


@pytest.mark.usefixtures("mock_contact")
def test_get_contact(api_client):
    contact = api_client.contacts.get("9hga75n6mdvq4zgcmhcn7hpys")
    assert contact is not None
    assert isinstance(contact, Contact)
    assert contact.given_name == "Given"
    assert contact.surname == "Sur"
    assert contact.birthday == date(1964, 10, 5)
    assert contact.source == "inbox"


@pytest.mark.usefixtures("mock_contacts")
def test_create_contact(api_client, mocked_responses):
    contact = api_client.contacts.create()
    contact.given_name = "Monkey"
    contact.surname = "Business"
    assert not mocked_responses.calls
    contact.save()
    assert len(mocked_responses.calls) == 1
    assert contact.id is not None
    assert contact.given_name == "Monkey"
    assert contact.surname == "Business"


@pytest.mark.usefixtures("mock_contact")
def test_update_contact(api_client, mocked_responses):
    contact = api_client.contacts.get("9hga75n6mdvq4zgcmhcn7hpys")
    assert len(mocked_responses.calls) == 1
    assert contact.job_title == "QA Tester"
    contact.job_title = "Factory Owner"
    contact.office_location = "Willy Wonka Factory"
    contact.save()
    assert len(mocked_responses.calls) == 2
    assert contact.id == "9hga75n6mdvq4zgcmhcn7hpys"
    assert contact.job_title == "Factory Owner"
    assert contact.office_location == "Willy Wonka Factory"


@pytest.mark.usefixtures("mock_contact")
def test_contact_picture(api_client, mocked_responses):
    contact = api_client.contacts.get("9hga75n6mdvq4zgcmhcn7hpys")
    assert len(mocked_responses.calls) == 1
    assert contact.picture_url
    picture = contact.get_picture()
    assert len(mocked_responses.calls) == 2
    picture_call = mocked_responses.calls[1]
    assert contact.picture_url == picture_call.request.url
    assert picture.headers["Content-Type"] == "image/jpeg"
    content = picture.read()
    assert isinstance(content, binary_type)


@pytest.mark.usefixtures("mock_contacts")
def test_contact_no_picture(api_client, mocked_responses):
    contact = api_client.contacts.get("4zqkfw8k1d12h0k784ipeh498")
    assert len(mocked_responses.calls) == 1
    assert not contact.picture_url
    picture = contact.get_picture()
    assert len(mocked_responses.calls) == 1
    assert not picture


@pytest.mark.usefixtures("mock_contact")
def test_contact_emails(api_client):
    contact = api_client.contacts.get("9hga75n6mdvq4zgcmhcn7hpys")
    assert isinstance(contact.emails, dict)
    assert contact.emails["first"] == ["one@example.com"]
    assert contact.emails["second"] == ["two@example.com"]
    assert contact.emails["primary"] == ["abc@example.com", "xyz@example.com"]
    assert contact.emails[None] == ["unknown@example.com"]
    assert "absent" not in contact.emails


@pytest.mark.usefixtures("mock_contact")
def test_contact_im_addresses(api_client):
    contact = api_client.contacts.get("9hga75n6mdvq4zgcmhcn7hpys")
    assert isinstance(contact.im_addresses, dict)
    assert contact.im_addresses["aim"] == ["SmarterChild"]
    assert contact.im_addresses["gtalk"] == ["fake@gmail.com", "fake2@gmail.com"]
    assert "absent" not in contact.im_addresses


@pytest.mark.usefixtures("mock_contact")
def test_contact_physical_addresses(api_client):
    contact = api_client.contacts.get("9hga75n6mdvq4zgcmhcn7hpys")
    assert isinstance(contact.physical_addresses, dict)
    addr = contact.physical_addresses["home"][0]
    assert isinstance(addr, dict)
    assert addr["format"] == "structured"
    assert addr["street_address"] == "123 Awesome Street"
    assert "absent" not in contact.physical_addresses


@pytest.mark.usefixtures("mock_contact")
def test_contact_phone_numbers(api_client):
    contact = api_client.contacts.get("9hga75n6mdvq4zgcmhcn7hpys")
    assert isinstance(contact.phone_numbers, dict)
    assert contact.phone_numbers["home"] == ["555-555-5555"]
    assert contact.phone_numbers["mobile"] == ["555-555-5555", "987654321"]
    assert "absent" not in contact.phone_numbers


@pytest.mark.usefixtures("mock_contact")
def test_contact_web_pages(api_client):
    contact = api_client.contacts.get("9hga75n6mdvq4zgcmhcn7hpys")
    assert isinstance(contact.web_pages, dict)
    profiles = ["http://www.facebook.com/abc", "http://www.twitter.com/abc"]
    assert contact.web_pages["profile"] == profiles
    assert contact.web_pages[None] == ["http://example.com"]
    assert "absent" not in contact.web_pages


@pytest.mark.usefixtures("mock_contact")
def test_update_contact_special_values(api_client, mocked_responses):
    contact = api_client.contacts.get("9hga75n6mdvq4zgcmhcn7hpys")
    assert len(mocked_responses.calls) == 1
    contact.birthday = date(1999, 3, 6)
    contact.emails["absent"].append("absent@fake.com")
    contact.im_addresses["absent"].append("absent-im")
    contact.physical_addresses["absent"].append(
        {
            "type": "absent",
            "format": "structured",
            "street_address": "123 Absent Street",
        }
    )
    contact.phone_numbers["absent"].append("222-333-4444")
    contact.web_pages["absent"].append("http://absent.com/me")
    contact.save()
    assert len(mocked_responses.calls) == 2
    assert contact.id == "9hga75n6mdvq4zgcmhcn7hpys"
    assert contact.emails["absent"] == ["absent@fake.com"]
    assert contact.im_addresses["absent"] == ["absent-im"]
    assert contact.physical_addresses["absent"] == [
        {
            "type": "absent",
            "format": "structured",
            "street_address": "123 Absent Street",
        }
    ]
    assert contact.phone_numbers["absent"] == ["222-333-4444"]
    assert contact.web_pages["absent"] == ["http://absent.com/me"]

    request = mocked_responses.calls[-1].request
    req_body = json.loads(request.body)
    birthday = "1999-03-06"
    email_address = {"type": "absent", "email": "absent@fake.com"}
    im_address = {"type": "absent", "im_address": "absent-im"}
    physical_address = {
        "type": "absent",
        "format": "structured",
        "street_address": "123 Absent Street",
    }
    phone_number = {"type": "absent", "number": "222-333-4444"}
    web_page = {"type": "absent", "url": "http://absent.com/me"}
    assert req_body["birthday"] == birthday
    assert email_address in req_body["emails"]
    assert im_address in req_body["im_addresses"]
    assert physical_address in req_body["physical_addresses"]
    assert phone_number in req_body["phone_numbers"]
    assert web_page in req_body["web_pages"]

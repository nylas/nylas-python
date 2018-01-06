import pytest
from six import binary_type
from nylas.client.restful_models import Contact


@pytest.mark.usefixtures("mock_contacts")
def test_list_contacts(api_client):
    contacts = api_client.contacts
    contacts = [c for c in contacts]
    assert len(contacts) == 3
    assert all(isinstance(x, Contact) for x in contacts)


@pytest.mark.usefixtures("mock_contact")
def test_get_contact(api_client):
    contact = api_client.contacts.get('5x6b54whvcz1j22ggiyorhk9v')
    assert contact is not None
    assert isinstance(contact, Contact)
    assert contact.given_name == 'Charlie'
    assert contact.surname == 'Bucket'


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
    contact = api_client.contacts.get('5x6b54whvcz1j22ggiyorhk9v')
    assert len(mocked_responses.calls) == 1
    assert contact.job_title == "Student"
    contact.job_title = "Factory Owner"
    contact.office_location = "Willy Wonka Factory"
    contact.save()
    assert len(mocked_responses.calls) == 2
    assert contact.id == '5x6b54whvcz1j22ggiyorhk9v'
    assert contact.job_title == "Factory Owner"
    assert contact.office_location == "Willy Wonka Factory"


@pytest.mark.usefixtures("mock_contact")
def test_contact_picture(api_client, mocked_responses):
    contact = api_client.contacts.find('5x6b54whvcz1j22ggiyorhk9v')
    assert len(mocked_responses.calls) == 1
    assert contact.picture_url
    f = contact.get_picture()
    assert len(mocked_responses.calls) == 2
    picture_call = mocked_responses.calls[1]
    assert contact.picture_url == picture_call.request.url
    assert f.headers["Content-Type"] == "image/jpeg"
    content = f.read()
    assert isinstance(content, binary_type)


@pytest.mark.usefixtures("mock_contacts")
def test_contact_no_picture(api_client, mocked_responses):
    contact = api_client.contacts.find('4zqkfw8k1d12h0k784ipeh498')
    assert len(mocked_responses.calls) == 1
    assert not contact.picture_url
    f = contact.get_picture()
    assert len(mocked_responses.calls) == 1
    assert not f

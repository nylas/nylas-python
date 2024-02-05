from nylas.resources.contacts import Contacts

from nylas.models.contacts import (
    Contact,
    ContactEmail,
    ContactGroupId,
    InstantMessagingAddress,
    PhoneNumber,
    PhysicalAddress,
    WebPage,
)


class TestContact:
    def test_contact_deserialization(self):
        contact_json = {
            "birthday": "1960-12-31",
            "company_name": "Nylas",
            "emails": [{"type": "work", "email": "john-work@example.com"}],
            "given_name": "John",
            "grant_id": "41009df5-bf11-4c97-aa18-b285b5f2e386",
            "groups": [{"id": "starred"}],
            "id": "5d3qmne77v32r8l4phyuksl2x",
            "im_addresses": [{"type": "other", "im_address": "myjabberaddress"}],
            "job_title": "Software Engineer",
            "manager_name": "Bill",
            "middle_name": "Jacob",
            "nickname": "JD",
            "notes": "Loves ramen",
            "object": "contact",
            "office_location": "123 Main Street",
            "phone_numbers": [{"type": "work", "number": "+1-555-555-5555"}],
            "physical_addresses": [
                {
                    "type": "work",
                    "street_address": "123 Main Street",
                    "postal_code": 94107,
                    "state": "CA",
                    "country": "US",
                    "city": "San Francisco",
                }
            ],
            "picture_url": "https://example.com/picture.jpg",
            "suffix": "Jr.",
            "surname": "Doe",
            "web_pages": [
                {"type": "work", "url": "http://www.linkedin.com/in/johndoe"}
            ],
        }

        contact = Contact.from_dict(contact_json)

        assert contact.birthday == "1960-12-31"
        assert contact.company_name == "Nylas"
        assert contact.emails == [
            ContactEmail(email="john-work@example.com", type="work")
        ]
        assert contact.given_name == "John"
        assert contact.grant_id == "41009df5-bf11-4c97-aa18-b285b5f2e386"
        assert contact.groups == [ContactGroupId(id="starred")]
        assert contact.id == "5d3qmne77v32r8l4phyuksl2x"
        assert contact.im_addresses == [
            InstantMessagingAddress(type="other", im_address="myjabberaddress")
        ]
        assert contact.job_title == "Software Engineer"
        assert contact.manager_name == "Bill"
        assert contact.middle_name == "Jacob"
        assert contact.nickname == "JD"
        assert contact.notes == "Loves ramen"
        assert contact.object == "contact"
        assert contact.office_location == "123 Main Street"
        assert contact.phone_numbers == [
            PhoneNumber(type="work", number="+1-555-555-5555")
        ]
        assert contact.physical_addresses == [
            PhysicalAddress(
                type="work",
                street_address="123 Main Street",
                postal_code="94107",
                state="CA",
                country="US",
                city="San Francisco",
            )
        ]
        assert contact.picture_url == "https://example.com/picture.jpg"
        assert contact.suffix == "Jr."
        assert contact.surname == "Doe"
        assert contact.web_pages == [
            WebPage(type="work", url="http://www.linkedin.com/in/johndoe")
        ]

    def test_list_contacts(self, http_client_list_response):
        contacts = Contacts(http_client_list_response)

        contacts.list(identifier="abc-123")

        http_client_list_response._execute.assert_called_once_with(
            "GET", "/v3/grants/abc-123/contacts", None, None, None
        )

    def test_list_contacts_with_query_params(self, http_client_list_response):
        contacts = Contacts(http_client_list_response)

        contacts.list(identifier="abc-123", query_params={"limit": 20})

        http_client_list_response._execute.assert_called_once_with(
            "GET", "/v3/grants/abc-123/contacts", None, {"limit": 20}, None
        )

    def test_find_contact(self, http_client_response):
        contacts = Contacts(http_client_response)

        contacts.find(identifier="abc-123", contact_id="contact-123")

        http_client_response._execute.assert_called_once_with(
            "GET", "/v3/grants/abc-123/contacts/contact-123", None, None, None
        )

    def test_find_contact_with_query_params(self, http_client_response):
        contacts = Contacts(http_client_response)

        contacts.find(
            identifier="abc-123",
            contact_id="contact-123",
            query_params={"profile_picture": True},
        )

        http_client_response._execute.assert_called_once_with(
            "GET",
            "/v3/grants/abc-123/contacts/contact-123",
            None,
            {"profile_picture": True},
            None,
        )

    def test_create_contact(self, http_client_response):
        contacts = Contacts(http_client_response)
        request_body = {
            "given_name": "John",
            "surname": "Doe",
            "company_name": "Nylas",
        }

        contacts.create(identifier="abc-123", request_body=request_body)

        http_client_response._execute.assert_called_once_with(
            "POST",
            "/v3/grants/abc-123/contacts",
            None,
            None,
            request_body,
        )

    def test_update_contact(self, http_client_response):
        contacts = Contacts(http_client_response)
        request_body = {
            "given_name": "John",
            "surname": "Doe",
            "company_name": "Nylas",
        }

        contacts.update(
            identifier="abc-123", contact_id="contact-123", request_body=request_body
        )

        http_client_response._execute.assert_called_once_with(
            "PUT",
            "/v3/grants/abc-123/contacts/contact-123",
            None,
            None,
            request_body,
        )

    def test_destroy_contact(self, http_client_delete_response):
        contacts = Contacts(http_client_delete_response)

        contacts.destroy(identifier="abc-123", contact_id="contact-123")

        http_client_delete_response._execute.assert_called_once_with(
            "DELETE",
            "/v3/grants/abc-123/contacts/contact-123",
            None,
            None,
            None,
        )

    def test_list_groups(self, http_client_list_response):
        contacts = Contacts(http_client_list_response)

        contacts.list_groups(identifier="abc-123", query_params={"limit": 20})

        http_client_list_response._execute.assert_called_once_with(
            method="GET",
            path="/v3/grants/abc-123/contacts/groups",
            query_params={"limit": 20},
        )

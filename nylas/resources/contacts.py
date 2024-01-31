from nylas.handler.api_resources import (
    ListableApiResource,
    FindableApiResource,
    CreatableApiResource,
    UpdatableApiResource,
    DestroyableApiResource,
)
from nylas.models.contacts import (
    Contact,
    CreateContactRequest,
    UpdateContactRequest,
    ListContactsQueryParams,
    FindContactQueryParams,
    ListContactGroupsQueryParams,
    ContactGroup,
)
from nylas.models.response import Response, ListResponse, DeleteResponse


class Contacts(
    ListableApiResource,
    FindableApiResource,
    CreatableApiResource,
    UpdatableApiResource,
    DestroyableApiResource,
):
    """
    Nylas Contacts API

    The Contacts API allows you to manage contacts and contact groups for a user.
    """

    def list(
        self, identifier: str, query_params: ListContactsQueryParams = None
    ) -> ListResponse[Contact]:
        """
        Return all Contacts.

        Attributes:
            identifier: The identifier of the Grant to act upon.
            query_params: The query parameters to include in the request.

        Returns:
            The list of contacts.
        """

        return super().list(
            path=f"/v3/grants/{identifier}/contacts",
            query_params=query_params,
            response_type=Contact,
        )

    def find(
        self,
        identifier: str,
        contact_id: str,
        query_params: FindContactQueryParams = None,
    ) -> Response[Contact]:
        """
        Return a Contact.

        Attributes:
            identifier: The identifier of the Grant to act upon.
            contact_id: The ID of the contact to retrieve.
            query_params: The query parameters to include in the request.

        Returns:
            The contact.
        """
        return super().find(
            path=f"/v3/grants/{identifier}/contacts/{contact_id}",
            response_type=Contact,
            query_params=query_params,
        )

    def create(
        self, identifier: str, request_body: CreateContactRequest
    ) -> Response[Contact]:
        """
        Create a Contact.

        Attributes:
            identifier: The identifier of the Grant to act upon.
            request_body: The values to create the Contact with.

        Returns:
            The created contact.
        """
        return super().create(
            path=f"/v3/grants/{identifier}/contacts",
            response_type=Contact,
            request_body=request_body,
        )

    def update(
        self, identifier: str, contact_id: str, request_body: UpdateContactRequest
    ) -> Response[Contact]:
        """
        Update a Contact.

        Attributes:
            identifier: The identifier of the Grant to act upon.
            contact_id: The ID of the Contact to update.
                Use "primary" to refer to the primary Contact associated with the Grant.
            request_body: The values to update the Contact with.

        Returns:
            The updated contact.
        """
        return super().update(
            path=f"/v3/grants/{identifier}/contacts/{contact_id}",
            response_type=Contact,
            request_body=request_body,
        )

    def destroy(self, identifier: str, contact_id: str) -> DeleteResponse:
        """
        Delete a Contact.

        Attributes:
            identifier: The identifier of the Grant to act upon.
            contact_id: The ID of the Contact to delete.
                Use "primary" to refer to the primary Contact associated with the Grant.

        Returns:
            The deletion response.
        """
        return super().destroy(path=f"/v3/grants/{identifier}/contacts/{contact_id}")

    def list_groups(
        self, identifier: str, query_params: ListContactGroupsQueryParams = None
    ) -> ListResponse[ContactGroup]:
        """
        Return all contact groups.

        Attributes:
            identifier: The identifier of the Grant to act upon.
            query_params: The query parameters to include in the request.

        Returns:
            The list of contact groups.
        """
        json_response = self._http_client._execute(
            method="GET",
            path=f"/v3/grants/{identifier}/contacts/groups",
            query_params=query_params,
        )

        return ListResponse.from_dict(json_response, ContactGroup)

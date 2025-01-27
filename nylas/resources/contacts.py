from nylas.config import RequestOverrides
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
        self,
        identifier: str,
        query_params: ListContactsQueryParams = None,
        overrides: RequestOverrides = None,
    ) -> ListResponse[Contact]:
        """
        Return all Contacts.

        Attributes:
            identifier: The identifier of the Grant to act upon.
            query_params: The query parameters to include in the request.
            overrides: The request overrides to use for the request.

        Returns:
            The list of contacts.
        """

        return super().list(
            path=f"/v3/grants/{identifier}/contacts",
            query_params=query_params,
            response_type=Contact,
            overrides=overrides,
        )

    def find(
        self,
        identifier: str,
        contact_id: str,
        query_params: FindContactQueryParams = None,
        overrides: RequestOverrides = None,
    ) -> Response[Contact]:
        """
        Return a Contact.

        Attributes:
            identifier: The identifier of the Grant to act upon.
            contact_id: The ID of the contact to retrieve.
            query_params: The query parameters to include in the request.
            overrides: The request overrides to use for the request.

        Returns:
            The contact.
        """
        return super().find(
            path=f"/v3/grants/{identifier}/contacts/{contact_id}",
            response_type=Contact,
            query_params=query_params,
            overrides=overrides,
        )

    def create(
        self,
        identifier: str,
        request_body: CreateContactRequest,
        overrides: RequestOverrides = None,
    ) -> Response[Contact]:
        """
        Create a Contact.

        Attributes:
            identifier: The identifier of the Grant to act upon.
            request_body: The values to create the Contact with.
            overrides: The request overrides to use for the request.

        Returns:
            The created contact.
        """
        return super().create(
            path=f"/v3/grants/{identifier}/contacts",
            response_type=Contact,
            request_body=request_body,
            overrides=overrides,
        )

    def update(
        self,
        identifier: str,
        contact_id: str,
        request_body: UpdateContactRequest,
        overrides: RequestOverrides = None,
    ) -> Response[Contact]:
        """
        Update a Contact.

        Attributes:
            identifier: The identifier of the Grant to act upon.
            contact_id: The ID of the Contact to update.
                Use "primary" to refer to the primary Contact associated with the Grant.
            request_body: The values to update the Contact with.
            overrides: The request overrides to use for the request.

        Returns:
            The updated contact.
        """
        return super().update(
            path=f"/v3/grants/{identifier}/contacts/{contact_id}",
            response_type=Contact,
            request_body=request_body,
            overrides=overrides,
        )

    def destroy(
        self,
        identifier: str,
        contact_id: str,
        overrides: RequestOverrides = None,
    ) -> DeleteResponse:
        """
        Delete a Contact.

        Attributes:
            identifier: The identifier of the Grant to act upon.
            contact_id: The ID of the Contact to delete.
                Use "primary" to refer to the primary Contact associated with the Grant.
            overrides: The request overrides to use for the request.

        Returns:
            The deletion response.
        """
        return super().destroy(
            path=f"/v3/grants/{identifier}/contacts/{contact_id}", overrides=overrides
        )

    def list_groups(
        self,
        identifier: str,
        query_params: ListContactGroupsQueryParams = None,
        overrides: RequestOverrides = None,
    ) -> ListResponse[ContactGroup]:
        """
        Return all contact groups.

        Attributes:
            identifier: The identifier of the Grant to act upon.
            query_params: The query parameters to include in the request.
            overrides: The request overrides to use for the request.

        Returns:
            The list of contact groups.
        """
        json_response, headers = self._http_client._execute(
            method="GET",
            path=f"/v3/grants/{identifier}/contacts/groups",
            query_params=query_params,
            overrides=overrides,
        )

        return ListResponse.from_dict(json_response, ContactGroup, headers)

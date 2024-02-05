import urllib.parse

from nylas.handler.api_resources import (
    ListableApiResource,
    FindableApiResource,
    CreatableApiResource,
    UpdatableApiResource,
    DestroyableApiResource,
)
from nylas.models.response import Response, ListResponse
from nylas.models.webhooks import (
    Webhook,
    WebhookWithSecret,
    WebhookDeleteResponse,
    WebhookIpAddressesResponse,
    CreateWebhookRequest,
    UpdateWebhookRequest,
)


class Webhooks(
    ListableApiResource,
    FindableApiResource,
    CreatableApiResource,
    UpdatableApiResource,
    DestroyableApiResource,
):
    """
    Nylas Webhooks API

    The Nylas webhooks API allows you to manage webhook destinations for your Nylas application.
    """

    def list(self) -> ListResponse[Webhook]:
        """
        List all webhook destinations

        Returns:
            The list of webhook destinations
        """
        return super().list(path="/v3/webhooks", response_type=Webhook)

    def find(self, webhook_id: str) -> Response[Webhook]:
        """
        Get a webhook destination

        Parameters:
            webhook_id: The ID of the webhook destination to get

        Returns:
            The webhook destination
        """
        return super().find(path=f"/v3/webhooks/{webhook_id}", response_type=Webhook)

    def create(self, request_body: CreateWebhookRequest) -> Response[WebhookWithSecret]:
        """
        Create a webhook destination

        Parameters:
            request_body: The request body to create the webhook destination

        Returns:
            The created webhook destination
        """
        return super().create(
            path="/v3/webhooks",
            request_body=request_body,
            response_type=WebhookWithSecret,
        )

    def update(
        self, webhook_id: str, request_body: UpdateWebhookRequest
    ) -> Response[Webhook]:
        """
        Update a webhook destination

        Parameters:
            webhook_id: The ID of the webhook destination to update
            request_body: The request body to update the webhook destination

        Returns:
            The updated webhook destination
        """
        return super().update(
            path=f"/v3/webhooks/{webhook_id}",
            request_body=request_body,
            response_type=Webhook,
        )

    def destroy(self, webhook_id: str) -> WebhookDeleteResponse:
        """
        Delete a webhook destination

        Parameters:
            webhook_id: The ID of the webhook destination to delete

        Returns:
            The response from deleting the webhook destination
        """
        return super().destroy(
            path=f"/v3/webhooks/{webhook_id}", response_type=WebhookDeleteResponse
        )

    def rotate_secret(self, webhook_id: str) -> Response[WebhookWithSecret]:
        """
        Update the webhook secret value for a destination

        Parameters:
            webhook_id: The ID of the webhook destination to update

        Returns:
            The updated webhook destination
        """
        res = self._http_client._execute(
            method="PUT",
            path=f"/v3/webhooks/{webhook_id}/rotate-secret",
            request_body={},
        )
        return Response.from_dict(res, WebhookWithSecret)

    def ip_addresses(self) -> Response[WebhookIpAddressesResponse]:
        """
        Get the current list of IP addresses that Nylas sends webhooks from

        Returns:
            The list of IP addresses that Nylas sends webhooks from
        """
        res = self._http_client._execute(method="GET", path="/v3/webhooks/ip-addresses")
        return Response.from_dict(res, WebhookIpAddressesResponse)


def extract_challenge_parameter(url: str) -> str:
    """
    Extract the challenge parameter from a URL

    Parameters:
        url: The URL sent by Nylas containing the challenge parameter

    Returns:
        The challenge parameter
    """
    url_object = urllib.parse.urlparse(url)
    query = urllib.parse.parse_qs(url_object.query)
    challenge_parameter = query.get("challenge")
    if not challenge_parameter:
        raise ValueError("Invalid URL or no challenge parameter found.")

    return challenge_parameter[0]

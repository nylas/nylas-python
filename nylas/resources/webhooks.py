from nylas.handler.admin_api_resources import (
    ListableAdminApiResource,
    FindableAdminApiResource,
    CreatableAdminApiResource,
    UpdatableAdminApiResource,
    DestroyableAdminApiResource,
)
from nylas.models.webhooks import Webhook, WebhookWithSecret, WebhookDeleteResponse


class Webhooks(
    ListableAdminApiResource[Webhook],
    FindableAdminApiResource[Webhook],
    CreatableAdminApiResource[WebhookWithSecret],
    UpdatableAdminApiResource[Webhook],
    DestroyableAdminApiResource[WebhookDeleteResponse],
):
    def __init__(self, http_client):
        super(Webhooks, self).__init__("webhooks", http_client)

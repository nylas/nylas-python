from nylas.handler.admin_api_resources import (
    ListableAdminApiResource,
    FindableAdminApiResource,
    CreatableAdminApiResource,
    UpdatableAdminApiResource,
    DestroyableAdminApiResource,
)
from nylas.models.reditect_uri import RedirectUri


class RedirectUris(
    ListableAdminApiResource[RedirectUri],
    FindableAdminApiResource[RedirectUri],
    CreatableAdminApiResource[RedirectUri],
    UpdatableAdminApiResource[RedirectUri],
    DestroyableAdminApiResource,
):
    def __init__(self, http_client):
        super(RedirectUris, self).__init__("redirect-uris", http_client)

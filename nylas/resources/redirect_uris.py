from nylas.handler.admin_api_resources import (
    ListableAdminApiResource,
    FindableAdminApiResource,
    CreatableAdminApiResource,
    UpdatableAdminApiResource,
    DestroyableAdminApiResource,
)


class RedirectUris(
    ListableAdminApiResource,
    FindableAdminApiResource,
    CreatableAdminApiResource,
    UpdatableAdminApiResource,
    DestroyableAdminApiResource,
):
    def __init__(self, http_client):
        super(RedirectUris, self).__init__("redirect-uris", http_client)

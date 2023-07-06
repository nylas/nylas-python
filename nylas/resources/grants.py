from nylas.handler.admin_api_resources import (
    ListableAdminApiResource,
    FindableAdminApiResource,
    CreatableAdminApiResource,
    UpdatableAdminApiResource,
    DestroyableAdminApiResource,
)


class Grants(
    ListableAdminApiResource,
    FindableAdminApiResource,
    CreatableAdminApiResource,
    UpdatableAdminApiResource,
    DestroyableAdminApiResource,
):
    def __init__(self, http_client):
        super(Grants, self).__init__("grants", http_client)

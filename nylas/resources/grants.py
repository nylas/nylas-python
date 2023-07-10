from nylas.handler.admin_api_resources import (
    ListableAdminApiResource,
    FindableAdminApiResource,
    CreatableAdminApiResource,
    UpdatableAdminApiResource,
    DestroyableAdminApiResource,
)
from nylas.models.grant import Grant


class Grants(
    ListableAdminApiResource[Grant],
    FindableAdminApiResource[Grant],
    CreatableAdminApiResource[Grant],
    UpdatableAdminApiResource[Grant],
    DestroyableAdminApiResource,
):
    def __init__(self, http_client):
        super(Grants, self).__init__("grants", http_client)

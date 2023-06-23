from nylas.handler.grants_api_resources import (
    ListableGrantsApiResource,
    FindableGrantsApiResource,
    CreatableGrantsApiResource,
    UpdatableGrantsApiResource,
    DestroyableGrantsApiResource,
)


class Events(
    ListableGrantsApiResource,
    FindableGrantsApiResource,
    CreatableGrantsApiResource,
    UpdatableGrantsApiResource,
    DestroyableGrantsApiResource,
):
    def __init__(self, http_client):
        super(Events, self).__init__("events", http_client)

from nylas.handler.grants_api_resources import (
    ListableGrantsApiResource,
    FindableGrantsApiResource,
    CreatableGrantsApiResource,
    UpdatableGrantsApiResource,
    DestroyableGrantsApiResource,
)


class Calendars(
    ListableGrantsApiResource,
    FindableGrantsApiResource,
    CreatableGrantsApiResource,
    UpdatableGrantsApiResource,
    DestroyableGrantsApiResource,
):
    def __init__(self, http_client):
        super(Calendars, self).__init__("calendars", http_client)

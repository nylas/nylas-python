from nylas.handler.grants_api_resources import (
    ListableGrantsApiResource,
    FindableGrantsApiResource,
    CreatableGrantsApiResource,
    UpdatableGrantsApiResource,
    DestroyableGrantsApiResource,
)
from nylas.models.calendar import Calendar


class Calendars(
    ListableGrantsApiResource[Calendar],
    FindableGrantsApiResource[Calendar],
    CreatableGrantsApiResource[Calendar],
    UpdatableGrantsApiResource[Calendar],
    DestroyableGrantsApiResource,
):
    def __init__(self, http_client):
        super(Calendars, self).__init__("calendars", http_client)

from nylas.handler.api_resources import (
    ListableApiResource,
    FindableApiResource,
    CreatableApiResource,
    UpdatableApiResource,
    DestroyableApiResource,
)
from nylas.models.calendar import Calendar
from nylas.models.delete_response import DeleteResponse
from nylas.models.list_response import ListResponse
from nylas.models.response import Response


class Calendars(
    ListableApiResource[Calendar],
    FindableApiResource[Calendar],
    CreatableApiResource[Calendar],
    UpdatableApiResource[Calendar],
    DestroyableApiResource,
):
    def __init__(self, http_client):
        super(Calendars, self).__init__("calendars", http_client)

    def list(self, identifier: str) -> ListResponse[Calendar]:
        return super(Calendars, self).list(path=f"/v3/grants/{identifier}/calendars")

    def find(self, identifier: str, calendar_id: str) -> Response[Calendar]:
        return super(Calendars, self).find(
            path=f"/v3/grants/{identifier}/calendars/{calendar_id}"
        )

    def create(self, identifier: str, request_body: dict) -> Response[Calendar]:
        return super(Calendars, self).create(
            path=f"/v3/grants/{identifier}/calendars", request_body=request_body
        )

    def update(
        self, identifier: str, calendar_id: str, request_body: dict
    ) -> Response[Calendar]:
        return super(Calendars, self).update(
            path=f"/v3/grants/{identifier}/calendars/{calendar_id}",
            request_body=request_body,
        )

    def destroy(self, identifier: str, calendar_id: str) -> DeleteResponse:
        return super(Calendars, self).destroy(
            path=f"/v3/grants/{identifier}/calendars/{calendar_id}"
        )

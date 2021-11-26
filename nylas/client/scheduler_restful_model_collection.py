import copy

from nylas.client.restful_model_collection import RestfulModelCollection
from nylas.client.restful_models import Scheduler
from nylas.client.scheduler_models import (
    SchedulerTimeSlot,
    SchedulerBookingConfirmation,
)


class SchedulerRestfulModelCollection(RestfulModelCollection):
    def __init__(self, api):
        # Make a copy of the API as we need to change the base url for Scheduler calls
        scheduler_api = copy.copy(api)
        scheduler_api.api_server = "https://api.schedule.nylas.com"
        RestfulModelCollection.__init__(self, Scheduler, scheduler_api)

    def get_google_availability(self):
        return self._execute_provider_availability("google")

    def get_office_365_availability(self):
        return self._execute_provider_availability("o365")

    def get_page_slug(self, slug):
        page_response = self.api._get_resource_raw(
            self.model_class, slug, extra="info", path="schedule"
        ).json()
        return Scheduler.create(self.api, **page_response)

    def get_available_time_slots(self, slug):
        response = self.api._get_resource_raw(
            self.model_class, slug, extra="timeslots", path="schedule"
        ).json()
        return [
            SchedulerTimeSlot.create(self.api, **x) for x in response if x is not None
        ]

    def book_time_slot(self, slug, timeslot):
        response = self.api._post_resource(
            self.model_class, slug, "timeslots", timeslot.as_json(), path="schedule"
        )
        return SchedulerBookingConfirmation.create(self.api, **response)

    def cancel_booking(self, slug, edit_hash, reason):
        return self.api._post_resource(
            self.model_class,
            slug,
            "{}/cancel".format(edit_hash),
            {"reason": reason},
            path="schedule",
        )

    def confirm_booking(self, slug, edit_hash):
        booking_response = self.api._post_resource(
            self.model_class, slug, "{}/confirm".format(edit_hash), {}, path="schedule"
        )
        return SchedulerBookingConfirmation.create(self.api, **booking_response)

    def _execute_provider_availability(self, provider):
        return self.api._get_resource_raw(
            self.model_class,
            None,
            extra="availability/{}".format(provider),
            path="schedule",
        ).json()

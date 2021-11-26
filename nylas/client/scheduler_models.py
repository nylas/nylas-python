from nylas.client.restful_models import RestfulModel


class SchedulerTimeSlot(RestfulModel):
    attrs = ["account_id", "calendar_id", "host_name", "emails"]
    datetime_attrs = {"start": "start", "end": "end"}

    def __init__(self, api):
        RestfulModel.__init__(self, SchedulerTimeSlot, api)


class SchedulerBookingConfirmation(RestfulModel):
    attrs = [
        "id",
        "account_id",
        "additional_field_values",
        "calendar_event_id",
        "calendar_id",
        "edit_hash",
        "is_confirmed",
        "location",
        "recipient_email",
        "recipient_locale",
        "recipient_name",
        "recipient_tz",
        "title",
    ]
    datetime_attrs = {"start_time": "start_time", "end_time": "end_time"}

    def __init__(self, api):
        RestfulModel.__init__(self, SchedulerBookingConfirmation, api)


class SchedulerBookingRequest(RestfulModel):
    attrs = [
        "additional_values",
        "additional_emails",
        "email",
        "locale",
        "name",
        "page_hostname",
        "replaces_booking_hash",
        "timezone",
        "slot",
    ]

    def __init__(self, api):
        RestfulModel.__init__(self, SchedulerBookingRequest, api)

    def as_json(self):
        dct = RestfulModel.as_json(self)
        if "additional_values" not in dct or dct["additional_values"] is None:
            dct["additional_values"] = {}
        if "additional_emails" not in dct or dct["additional_emails"] is None:
            dct["additional_emails"] = []
        if "slot" in dct and isinstance(dct["slot"], SchedulerTimeSlot):
            dct["slot"] = dct["slot"].as_json()

        return dct

from nylas.client.restful_models import RestfulModel, Draft


class OutboxMessage(RestfulModel):
    attrs = Draft.attrs + [
        "send_at",
        "retry_limit_datetime",
        "original_send_at",
    ]
    datetime_attrs = {
        "send_at": "send_at",
        "retry_limit_datetime": "retry_limit_datetime",
        "original_send_at": "original_send_at"
    }
    read_only_attrs = {"send_at", "retry_limit_datetime", "original_send_at"}
    collection_name = "v2/outbox"

    def __init__(self, api):
        RestfulModel.__init__(self, OutboxMessage, api)


class OutboxJobStatus(RestfulModel):
    attrs = [
        "account_id",
        "job_status_id",
        "status",
        "original_data",
    ]
    collection_name = "v2/outbox"

    def __init__(self, api):
        RestfulModel.__init__(self, OutboxJobStatus, api)


class SendGridVerifiedStatus(RestfulModel):
    attrs = [
        "domain_verified",
        "sender_verified",
    ]
    collection_name = "v2/outbox/onboard"

    def __init__(self, api):
        RestfulModel.__init__(self, SendGridVerifiedStatus, api)


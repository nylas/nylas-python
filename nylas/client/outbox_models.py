from datetime import datetime

from nylas.client.restful_models import RestfulModel, Draft
from nylas.utils import timestamp_from_dt


class OutboxMessage(RestfulModel):
    attrs = Draft.attrs + [
        "send_at",
        "retry_limit_datetime",
        "original_send_at",
    ]
    datetime_attrs = {
        "send_at": "send_at",
        "retry_limit_datetime": "retry_limit_datetime",
        "original_send_at": "original_send_at",
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


class Outbox:
    def __init__(self, api):
        self.api = api

    def send(self, draft, send_at, retry_limit_datetime=None):
        """
        Send a message via Outbox

        Args:
            draft (Draft | OutboxMessage): The message to send
            send_at (datetime | int): The date and time to send the message. If set to 0, Outbox will send this message immediately.
            retry_limit_datetime (datetime | int): Optional date and time to stop retry attempts for a message.

        Returns:
            OutboxJobStatus: The Outbox message job status

        Raises:
            ValueError: If the date and times provided are not valid
        """
        draft_json = draft.as_json()
        send_at, retry_limit_datetime = self._validate_and_format_datetime(
            send_at, retry_limit_datetime
        )

        draft_json["send_at"] = send_at
        if retry_limit_datetime is not None:
            draft_json["retry_limit_datetime"] = retry_limit_datetime

        return self.api._create_resource(OutboxJobStatus, draft_json)

    def update(
        self, job_status_id, draft=None, send_at=None, retry_limit_datetime=None
    ):
        """
        Update a scheduled Outbox message

        Args:
            job_status_id (str): The ID of the outbox job status
            draft (Draft | OutboxMessage): The message object with updated values
            send_at (datetime | int): The date and time to send the message. If set to 0, Outbox will send this message immediately.
            retry_limit_datetime (datetime | int): Optional date and time to stop retry attempts for a message.

        Returns:
            OutboxJobStatus: The updated Outbox message job status

        Raises:
            ValueError: If the date and times provided are not valid
        """
        payload = {}
        if draft:
            payload = draft.as_json()
        send_at, retry_limit_datetime = self._validate_and_format_datetime(
            send_at, retry_limit_datetime
        )

        if send_at is not None:
            payload["send_at"] = send_at
        if retry_limit_datetime is not None:
            payload["retry_limit_datetime"] = retry_limit_datetime

        response = self.api._patch_resource(OutboxJobStatus, job_status_id, payload)
        return OutboxJobStatus.create(self.api, **response)

    def delete(self, job_status_id):
        """
        Delete a scheduled Outbox message

        Args:
            job_status_id (str): The ID of the outbox job status to delete
        """

        self.api._delete_resource(OutboxJobStatus, job_status_id)

    def send_grid_verification_status(self):
        """
        SendGrid - Check Authentication and Verification Status

        Returns:
            SendGridVerifiedStatus: The status of the domain authentication and the single sender verification for SendGrid integrations

        Raises:
            RuntimeError: If the server returns an object without results
        """
        response = self.api._get_resource_raw(
            SendGridVerifiedStatus, None, extra="verified_status"
        )
        response_body = response.json()
        if "results" not in response_body:
            raise RuntimeError(
                "Unexpected response from the API server. Returned 200 but no 'ics' string found."
            )
        return SendGridVerifiedStatus.create(self.api, **response_body["results"])

    def delete_send_grid_sub_user(self, email_address):
        """
        SendGrid -  Delete SendGrid Subuser and UAS Grant

        Args:
            email_address (str): Email address for SendGrid subuser to delete
        """
        payload = {"email": email_address}

        self.api._delete_resource(SendGridVerifiedStatus, "subuser", data=payload)

    def _validate_and_format_datetime(self, send_at, retry_limit_datetime):
        send_at_epoch = (
            timestamp_from_dt(send_at) if isinstance(send_at, datetime) else send_at
        )
        retry_limit_datetime_epoch = (
            timestamp_from_dt(retry_limit_datetime)
            if isinstance(retry_limit_datetime, datetime)
            else retry_limit_datetime
        )
        now_epoch = timestamp_from_dt(datetime.today())

        if send_at_epoch and send_at_epoch != 0 and send_at_epoch < now_epoch:
            raise ValueError(
                "Cannot set message to be sent at a time before the current time."
            )

        if retry_limit_datetime_epoch and retry_limit_datetime_epoch != 0:
            current_send_at = (
                send_at_epoch if send_at_epoch and send_at_epoch != 0 else now_epoch
            )
            if retry_limit_datetime_epoch < current_send_at:
                raise ValueError(
                    "Cannot set message to stop retrying before time to send at."
                )

        return send_at_epoch, retry_limit_datetime_epoch

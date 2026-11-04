from dataclasses import dataclass
from typing import List, Literal, Optional, Union

from dataclasses_json import dataclass_json
from typing_extensions import TypedDict, NotRequired

from nylas.models.errors import NylasApiErrorResponseData
from nylas.models.events import (
    CreateEventQueryParams,
    CreateEventRequest,
    Event,
    UpdateEventRequest,
)


class BatchCreateEventOperation(TypedDict):
    """
    Interface representing a batch operation that creates an event.

    Attributes:
        method: The operation to run. Always "create".
        body: The values to create the event with.
    """

    method: Literal["create"]
    body: CreateEventRequest


class BatchUpdateEventOperation(TypedDict):
    """
    Interface representing a batch operation that updates an event.

    Attributes:
        method: The operation to run. Always "update".
        event_id: The ID of the event to update.
        body: The values to update the event with.
    """

    method: Literal["update"]
    event_id: str
    body: UpdateEventRequest


class BatchDeleteEventOperation(TypedDict):
    """
    Interface representing a batch operation that deletes an event.

    Attributes:
        method: The operation to run. Always "delete".
        event_id: The ID of the event to delete.
    """

    method: Literal["delete"]
    event_id: str


BatchEventOperation = Union[
    BatchCreateEventOperation, BatchUpdateEventOperation, BatchDeleteEventOperation
]
""" Union type representing the operations that a batch request can run. """


class BatchEventsRequest(TypedDict):
    """
    Interface representing a request to run a batch of event operations.

    Attributes:
        operations: The operations to run.
    """

    operations: List[BatchEventOperation]


class BatchEventsQueryParams(CreateEventQueryParams):
    """
    Interface representing the query parameters for a batch of event operations.
    The query parameters apply to every operation in the batch.

    Attributes:
        calendar_id: The ID of the calendar that every operation in the batch acts on.
        notify_participants: Whether to send email notifications containing the calendar event to all
            event participants. Defaults to true. Microsoft does not support setting this to false.
        tentative_as_busy: When set to false, treats tentative calendar events as busy:false.
            Only applicable for Microsoft calendars. Defaults to true.
        grant_email: The email address of the grant. Create operations default to the grant's email address.
        select: Comma-separated list of fields to return in the event data of each result.
    """

    grant_email: NotRequired[str]
    select: NotRequired[str]


@dataclass_json
@dataclass
class BatchEventResult:
    """
    Class representation of the result of one operation in a batch.

    Attributes:
        status: The HTTP status code of the operation.
        data: The created or updated event. Not set for delete operations or for failed operations.
        error: The error details. Only set if the operation failed.
        retry_after: The number of seconds to wait before retrying the operation. Can be 0.
            Only set on failed operations, when the provider throttled the request.
        provider_event_created: True if the provider created the event before a later step failed.
            Retrying the operation would create a duplicate event.
    """

    status: int
    data: Optional[Event] = None
    error: Optional[NylasApiErrorResponseData] = None
    retry_after: Optional[int] = None
    provider_event_created: Optional[bool] = None

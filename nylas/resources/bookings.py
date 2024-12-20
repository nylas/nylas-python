from nylas.config import RequestOverrides
from nylas.handler.api_resources import (
    CreatableApiResource,
    DestroyableApiResource,
    FindableApiResource,
    ListableApiResource,
    UpdatableApiResource,
    UpdatablePatchApiResource,
)
from nylas.models.response import DeleteResponse, Response
from nylas.models.scheduler import (
    Booking,
    ConfirmBookingQueryParams,
    ConfirmBookingRequest,
    CreateBookingQueryParams,
    CreateBookingRequest,
    DeleteBookingRequest,
    DestroyBookingQueryParams,
    RescheduleBookingRequest,
    FindBookingQueryParams,
    RescheduleBookingQueryParams,
)


class Bookings(
    ListableApiResource,
    FindableApiResource,
    CreatableApiResource,
    UpdatableApiResource,
    UpdatablePatchApiResource,
    DestroyableApiResource,
):
    """
    Nylas Bookings API

    The Nylas Bookings API allows you to create new bookings or manage existing ones, as well as getting
    bookings details for a user.

    A booking can be accessed by one, or several people, and can contain events.
    """

    def find(
        self,
        booking_id: str,
        query_params: FindBookingQueryParams = None,
        overrides: RequestOverrides = None,
    ) -> Response[Booking]:
        """
        Return a Booking.

        Args:
                identifier: The identifier of the Grant to act upon.
                booking_id: The identifier of the Booking to get.
                query_params: The query parameters to include in the request.
                overrides: The request overrides to use for the request.

        Returns:
                The Booking.
        """

        return super().find(
            path=f"/v3/scheduling/bookings/{booking_id}",
            query_params=query_params,
            response_type=Booking,
            overrides=overrides,
        )

    def create(
        self,
        request_body: CreateBookingRequest,
        query_params: CreateBookingQueryParams = None,
        overrides: RequestOverrides = None,
    ) -> Response[Booking]:
        """
        Create a Booking.

        Args:
                request_body: The values to create booking with.
                overrides: The request overrides to use for the request.
                query_params: The query parameters to include in the request.
                overrides: The request overrides to use for the request.

        Returns:
                The created Booking.
        """

        return super().create(
            path="/v3/scheduling/bookings",
            request_body=request_body,
            query_params=query_params,
            response_type=Booking,
            overrides=overrides,
        )

    def confirm(
        self,
        booking_id: str,
        request_body: ConfirmBookingRequest,
        query_params: ConfirmBookingQueryParams = None,
        overrides: RequestOverrides = None,
    ) -> Response[Booking]:
        """
        Confirm a Booking.

        Args:
                booking_id: The identifier of the Booking to confirm.
                request_body: The values to confirm booking with.
                query_params: The query parameters to include in the request.
                overrides: The request overrides to use for the request.

        Returns:
                The confirmed Booking.
        """

        return super().update(
            path=f"/v3/scheduling/bookings/{booking_id}",
            request_body=request_body,
            query_params=query_params,
            response_type=Booking,
            overrides=overrides,
        )

    def reschedule(
        self,
        booking_id: str,
        request_body: RescheduleBookingRequest,
        query_params: RescheduleBookingQueryParams = None,
        overrides: RequestOverrides = None,
    ) -> Response[Booking]:
        """
        Reschedule a Booking.

        Args:
                booking_id: The identifier of the Booking to reschedule.
                request_body: The values to reschedule booking with.
                query_params: The query parameters to include in the request.
                overrides: The request overrides to use for the request.

        Returns:
                The rescheduled Booking.
        """

        return super().patch(
            path=f"/v3/scheduling/bookings/{booking_id}",
            request_body=request_body,
            query_params=query_params,
            response_type=Booking,
            overrides=overrides,
        )

    def destroy(
        self,
        booking_id: str,
        request_body: DeleteBookingRequest,
        query_params: DestroyBookingQueryParams = None,
        overrides: RequestOverrides = None,
    ) -> DeleteResponse:
        """
        Delete a Booking.

        Args:
                booking_id: The identifier of the Booking to delete.
                request_body: The reason to delete booking with.
                query_params: The query parameters to include in the request.
                overrides: The request overrides to use for the request.

        Returns:
                None.
        """

        return super().destroy(
            path=f"/v3/scheduling/bookings/{booking_id}",
            request_body=request_body,
            query_params=query_params,
            overrides=overrides,
        )

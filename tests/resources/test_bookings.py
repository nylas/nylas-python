from nylas.resources.bookings import Bookings

from nylas.models.scheduler import Booking

class TestBooking:
  def test_booking_deserialization(self):
    booking_json = {
      "booking_id": "AAAA-BBBB-1111-2222",
      "event_id": "CCCC-DDDD-3333-4444",
      "title": "My test event",
      "organizer": {
        "name": "John Doe",
        "email": "user@example.com"
      },
      "status": "booked",
      "description": "This is an example of a description."
    }

    booking = Booking.from_dict(booking_json)

    assert booking.booking_id == "AAAA-BBBB-1111-2222"
    assert booking.event_id == "CCCC-DDDD-3333-4444"
    assert booking.title == "My test event"
    assert booking.organizer == {"name": "John Doe", "email": "user@example.com"}
    assert booking.status == "booked"
    assert booking.description == "This is an example of a description."

  def test_find_booking(self, http_client_find_response):
    bookings = Bookings(http_client_find_response)

    bookings.find(booking_id="booking-123")

    http_client_find_response._execute.assert_called_once_with(
      "GET", "/v3/scheduling/bookings/booking-123", query_params=None, overrides=None
    )

  def test_create_booking(self, http_client_create_response):
    bookings = Bookings(http_client_create_response)
    request_body = {
      "start_time": 1730725200,
      "end_time": 1730727000,
      "participants": [
        {
          "email": "test@nylas.com"
        }
      ],
      "guest": {
        "name": "TEST",
        "email": "user@gmail.com"
      }
    }
    bookings.create(request_body=request_body)
    http_client_create_response._execute.assert_called_once_with(
      "POST", 
      "/v3/scheduling/bookings", 
      query_params=None, 
      request_body=request_body, 
      overrides=None
    )

  def test_confirm_booking(self, http_client_update_response):
    bookings = Bookings(http_client_update_response)
    request_body = {
      "salt": "_zfg12it",
      "status": "cancelled",
    }

    bookings.confirm(booking_id="booking-123", request_body=request_body)
    http_client_update_response._execute.assert_called_once_with(
      "PUT",
      "/v3/scheduling/bookings/booking-123",
      query_params=None,
      request_body=request_body,
      overrides=None
    )

  def test_reschedule_booking(self, http_client_update_response):
    bookings = Bookings(http_client_update_response)
    request_body = {
      "start_time": 1730725200,
      "end_time": 1730727000,
    }

    bookings.reschedule(booking_id="booking-123", request_body=request_body)
    http_client_update_response._execute.assert_called_once_with(
      "PATCH",
      "/v3/scheduling/bookings/booking-123",
      query_params=None,
      request_body=request_body,
      overrides=None
    )

  def test_destroy_booking(self, http_client_delete_response):
    bookings = Bookings(http_client_delete_response)
    request_body = {
      "cancellation_reason": "I am no longer available at this time."
    }
    bookings.destroy(booking_id="booking-123")

    http_client_delete_response._execute.assert_called_once_with(
      "DELETE",
      "/v3/scheduling/bookings/booking-123",
      request_body=request_body,
      query_params=None,
      overrides=None
    )
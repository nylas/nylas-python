from dataclasses import dataclass
from typing import Dict, Optional, List

from dataclasses_json import dataclass_json
from typing_extensions import TypedDict, NotRequired, Literal
from nylas.models.events import Conferencing
from nylas.models.availability import AvailabilityRules, OpenHours

BookingType = Literal["booking", "organizer-confirmation"]
BookingReminderType = Literal["email", "webhook"]
BookingRecipientType = Literal["host", "guest", "all"]
EmailLanguage = Literal["en", "es", "fr", "de", "nl", "sv", "ja", "zh"]
AdditionalFieldType = Literal[
    "text",
    "multi_line_text",
    "email",
    "phone_number",
    "dropdown",
    "date",
    "checkbox",
    "radio_button",
]
AdditonalFieldOptionsType = Literal[
    "text", "email", "phone_number", "date", "checkbox", "radio_button"
]


@dataclass_json
@dataclass
class BookingConfirmedTemplate:
    """
    Class representation of booking confirmed template settings.

    Attributes:
        title: The title to replace the default 'Booking Confirmed' title.
        body: The additional body to be appended after the default body.
    """

    title: Optional[str] = None
    body: Optional[str] = None


@dataclass_json
@dataclass
class EmailTemplate:
    """
    Class representation of email template settings.

    Attributes:
        logo: The URL to a custom logo that appears at the top of the booking email.
        booking_confirmed: Configurable settings specifically for booking confirmed emails.
    """

    # logo: Optional[str] = None
    booking_confirmed: Optional[BookingConfirmedTemplate] = None


@dataclass_json
@dataclass
class AdditionalField:
    """
    Class representation of an additional field.

    Atributes:
        label: The text label to be displayed in the Scheduler UI.
        type: The field type. Supported values are text, multi_line_text,
            email, phone_number, dropdown, date, checkbox, and radio_button
        required: Whether the field is required to be filled out by the guest when booking an event.
        pattern: A regular expression pattern that the value of the field must match.
        order: The order in which the field will be displayed in the Scheduler UI.
            Fields with lower order values will be displayed first.
        options: A list of options for the dropdown or radio_button types.
            This field is required for the dropdown and radio_button types.
    """

    label: str
    type: AdditionalFieldType
    required: bool
    pattern: Optional[str] = None
    order: Optional[int] = None
    options: Optional[AdditonalFieldOptionsType] = None


@dataclass_json
@dataclass
class SchedulerSettings:
    """
    Class representation of scheduler settings.

    Attributes:
        additional_fields: Definitions for additional fields to be displayed in the Scheduler UI.
        available_days_in_future: Number of days in the future that Scheduler is available for scheduling events.
        min_booking_notice: Minimum number of minutes in the future that a user can make a new booking.
        min_cancellation_notice: Minimum number of minutes before a booking can be cancelled.
        cancellation_policy: A message about the cancellation policy to display when booking an event.
        rescheduling_url: The URL used to reschedule bookings.
        cancellation_url: The URL used to cancel bookings.
        organizer_confirmation_url: The URL used to confirm or cancel pending bookings.
        confirmation_redirect_url: The custom URL to redirect to once the booking is confirmed.
        hide_rescheduling_options: Whether the option to reschedule an event
            is hidden in booking confirmations and notifications.
        hide_cancellation_options: Whether the option to cancel an event 
            is hidden in booking confirmations and notifications.
        hide_additional_guests: Whether to hide the additional guests field on the scheduling page.
        email_template: Configurable settings for booking emails.
    """

    additional_fields: Optional[Dict[str, AdditionalField]] = None
    available_days_in_future: Optional[int] = None
    min_booking_notice: Optional[int] = None
    min_cancellation_notice: Optional[int] = None
    cancellation_policy: Optional[str] = None
    rescheduling_url: Optional[str] = None
    cancellation_url: Optional[str] = None
    organizer_confirmation_url: Optional[str] = None
    confirmation_redirect_url: Optional[str] = None
    hide_rescheduling_options: Optional[bool] = None
    hide_cancellation_options: Optional[bool] = None
    hide_additional_guests: Optional[bool] = None
    email_template: Optional[EmailTemplate] = None


@dataclass_json
@dataclass
class BookingReminder:
    """
    Class representation of a booking reminder.

    Attributes:
        type: The reminder type.
        minutes_before_event: The number of minutes before the event to send the reminder.
        recipient: The recipient of the reminder.
        email_subject: The subject of the email reminder.
    """

    type: str
    minutes_before_event: int
    recipient: Optional[str] = None
    email_subject: Optional[str] = None


@dataclass_json
@dataclass
class EventBooking:
    """
    Class representation of an event booking.

    Attributes:
        title: The title of the event.
        description: The description of the event.
        location: The location of the event.
        timezone: The timezone for displaying times in confirmation email messages and reminders.
        booking_type: The type of booking.
        conferencing: Conference details for the event.
        disable_emails: Whether Nylas sends email messages when an event is booked, cancelled, or rescheduled.
        reminders: The list of reminders to send to participants before the event starts.
    """

    title: str
    description: Optional[str] = None
    location: Optional[str] = None
    timezone: Optional[str] = None
    booking_type: Optional[BookingType] = None
    conferencing: Optional[Conferencing] = None
    disable_emails: Optional[bool] = None
    reminders: Optional[List[BookingReminder]] = None


@dataclass_json
@dataclass
class Availability:
    """
    Class representation of availability settings.

    Attributes:
        duration_minutes: The total number of minutes the event should last.
        interval_minutes: The interval between meetings in minutes.
        round_to: Nylas rounds each time slot to the nearest multiple of this number of minutes.
        availability_rules: Availability rules for scheduling configuration.
    """

    duration_minutes: int
    interval_minutes: Optional[int] = None
    round_to: Optional[int] = None
    availability_rules: Optional[AvailabilityRules] = None


@dataclass_json
@dataclass
class ParticipantBooking:
    """
    Class representation of a participant booking.

    Attributes:
        calendar_id: The calendar ID that the event is created in.
    """

    calendar_id: str


@dataclass_json
@dataclass
class ParticipantAvailability:
    """
    Class representation of participant availability.

    Attributes:
        calendar_ids: List of calendar IDs associated with the participant's email address.
        open_hours: Open hours for this participant. The endpoint searches for free time slots during these open hours.
    """

    calendar_ids: List[str]
    open_hours: Optional[List[OpenHours]] = None


@dataclass_json
@dataclass
class ConfigParticipant:
    """
    Class representation of a booking participant.

    Attributes:
        email: Participant's email address.
        availability: Availability data for the participant.
        booking: Booking data for the participant.
        name: Participant's name.
        is_organizer: Whether the participant is the organizer of the event.
        timezone: The participant's timezone.
    """

    email: str
    availability: ParticipantAvailability
    booking: ParticipantBooking
    name: Optional[str] = None
    is_organizer: Optional[bool] = None
    timezone: Optional[str] = None


@dataclass_json
@dataclass
class Configuration:
    """
    Class representation of a scheduler configuration.

    Attributes:
        participants: List of participants included in the scheduled event.
        availability: Rules that determine available time slots for the event.
        event_booking: Booking data for the event.
        slug: Unique identifier for the Configuration object.
        requires_session_auth: If true, scheduling Availability and Bookings endpoints require a valid session ID.
        scheduler: Settings for the Scheduler UI.
        appearance: Appearance settings for the Scheduler UI.
    """

    id: str
    participants: List[ConfigParticipant]
    availability: Availability
    event_booking: EventBooking
    slug: Optional[str] = None
    requires_session_auth: Optional[bool] = None
    scheduler: Optional[SchedulerSettings] = None
    appearance: Optional[Dict[str, str]] = None


class CreateConfigurationRequest(TypedDict):
    """
    Interface of a Nylas create configuration request.

    Attributes:
        participants: List of participants included in the scheduled event.
        availability: Rules that determine available time slots for the event.
        event_booking: Booking data for the event.
        slug: Unique identifier for the Configuration object.
        requires_session_auth: If true, scheduling Availability and Bookings endpoints require a valid session ID.
        scheduler: Settings for the Scheduler UI.
        appearance: Appearance settings for the Scheduler UI.
    """

    participants: List[ConfigParticipant]
    availability: Availability
    event_booking: EventBooking
    slug: NotRequired[str]
    requires_session_auth: NotRequired[bool]
    scheduler: NotRequired[SchedulerSettings]
    appearance: NotRequired[Dict[str, str]]


class UpdateConfigurationRequest(TypedDict):
    """
    Interface of a Nylas update configuration request.

    Attributes:
        participants: List of participants included in the scheduled event.
        availability: Rules that determine available time slots for the event.
        event_booking: Booking data for the event.
        slug: Unique identifier for the Configuration object.
        requires_session_auth: If true, scheduling Availability and Bookings endpoints require a valid session ID.
        scheduler: Settings for the Scheduler UI.
        appearance: Appearance settings for the Scheduler UI.
    """
    participants: NotRequired[List[ConfigParticipant]]
    availability: NotRequired[Availability]
    event_booking: NotRequired[EventBooking]
    slug: NotRequired[str]
    requires_session_auth: NotRequired[bool]
    scheduler: NotRequired[SchedulerSettings]
    appearance: NotRequired[Dict[str, str]]


class CreateSessionRequest(TypedDict):
    """
    Interface of a Nylas create session request.

    Attributes:
        configuration_id: The ID of the Configuration object whose settings are used for calculating availability.
            If you're using session authentication (requires_session_auth is set to true),
            configuration_id is not required.
        slug: The slug of the Configuration object whose settings are used for calculating availability.
            If you're using session authentication (requires_session_auth is set to true) or using configurationId,
            slug is not required.
        time_to_live: The time-to-live in seconds for the session
    """
    configuration_id: NotRequired[str]
    slug: NotRequired[str]
    time_to_live: NotRequired[int]


@dataclass_json
@dataclass
class Session:
    """
    Class representation of a session.

    Attributes:
        session_id: The ID of the session.
    """

    session_id: str


@dataclass_json
@dataclass
class BookingGuest:
    """
    Class representation of a booking guest.

    Attributes:
        email: The email address of the guest.
        name: The name of the guest.
    """

    email: str
    name: str


@dataclass_json
@dataclass
class BookingParticipant:
    """
    Class representation of a booking participant.

    Attributes:
        email: The email address of the participant to include in the booking.
    """

    email: str


@dataclass_json
@dataclass
class CreateBookingRequest:
    """
    Class representation of a create booking request.

    Attributes:
        start_time: The event's start time, in Unix epoch format.
        end_time: The event's end time, in Unix epoch format.
        guest: Details about the guest that is creating the booking.
        participants: List of participant email addresses from the
            Configuration object to include in the booking.
        timezone: The guest's timezone that is used in email notifications.
        email_language: The language of the guest email notifications.
        additional_guests: List of additional guest email addresses to include in the booking.
        additional_fields: Dictionary of additional field keys mapped to 
            values populated by the guest in the booking form.
    """

    start_time: int
    end_time: int
    guest: BookingGuest
    participants: Optional[List[BookingParticipant]] = None
    timezone: Optional[str] = None
    email_language: Optional[EmailLanguage] = None
    additional_guests: Optional[List[BookingGuest]] = None
    additional_fields: Optional[Dict[str, str]] = None


@dataclass_json
@dataclass
class BookingOrganizer:
    """
    Class representation of a booking organizer.

    Attributes:
        email: The email address of the participant designated as the organizer of the event.
        name: The name of the participant designated as the organizer of the event.
    """

    email: str
    name: Optional[str] = None


BookingStatus = Literal["pending", "confirmed", "cancelled"]
ConfirmBookingStatus = Literal["confirm", "cancel"]


@dataclass_json
@dataclass
class Booking:
    """
    Class representation of a booking.

    Attributes:
        booking_id: The unique ID of the booking.
        event_id: The unique ID of the event associated with the booking.
        title: The title of the event.
        organizer: The participant designated as the organizer of the event.
        status: The current status of the booking.
        description: The description of the event.
    """

    booking_id: str
    event_id: str
    title: str
    organizer: BookingOrganizer
    status: BookingStatus
    description: Optional[str] = None


@dataclass_json
@dataclass
class ConfirmBookingRequest:
    """
    Class representation of a confirm booking request.

    Attributes:
        salt: The salt extracted from the booking reference embedded in the organizer confirmation link.
        status: The action to take on the pending booking.
        cancellation_reason: The reason the booking is being cancelled.
    """

    salt: str
    status: ConfirmBookingStatus
    cancellation_reason: Optional[str] = None


@dataclass_json
@dataclass
class DeleteBookingRequest:
    """
    Class representation of a delete booking request.

    Attributes:
        cancellation_reason: The reason the booking is being cancelled.
    """

    cancellation_reason: Optional[str] = None


@dataclass_json
@dataclass
class RescheduleBookingRequest:
    """
    Class representation of a reschedule booking request.

    Attributes:
        start_time: The event's start time, in Unix epoch format.
        end_time: The event's end time, in Unix epoch format.
    """

    start_time: int
    end_time: int


@dataclass_json
@dataclass
class CreateBookingQueryParams:
    """
    Class representation of query parameters for creating a booking.

    Attributes:
      configuration_id: The ID of the Configuration object whose settings are used for calculating availability.
        If you're using session authentication (requires_session_auth is set to true), configuration_id is not required.
      slug: The slug of the Configuration object whose settings are used for calculating availability.
        If you're using session authentication (requires_session_auth is set to true) or using configurationId,
          slug is not required.
      timezone: The timezone to use for the booking. 
        If not provided, Nylas uses the timezone from the Configuration object.
    """

    configuration_id: Optional[str] = None
    slug: Optional[str] = None
    timezone: Optional[str] = None


class FindBookingQueryParams:
    """
    Class representation of query parameters for finding a booking.

    Attributes:
      configuration_id: The ID of the Configuration object whose settings are used for calculating availability.
        If you're using session authentication (requires_session_auth is set to true), configuration_id is not required.
      slug:  The slug of the Configuration object whose settings are used for calculating availability.
        If you're using session authentication (requires_session_auth is set to true)
        or using configurationId, slug is not required.
      client_id: The client ID that was used to create the Configuration object.
        client_id is required only if using slug.
    """

    configuration_id: Optional[str] = None
    slug: Optional[str] = None
    client_id: Optional[str] = None


ConfirmBookingQueryParams = FindBookingQueryParams
RescheduleBookingQueryParams = FindBookingQueryParams
DestroyBookingQueryParams = FindBookingQueryParams

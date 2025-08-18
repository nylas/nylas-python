nylas-python Changelog
======================

Unreleased
----------
* Fixed KeyError when processing events with empty or incomplete conferencing objects

v6.11.0
----------------
* Added `unknown` to ConferencingProvider

v6.10.0
----------------
* Added support for `single_level` query parameter in `ListFolderQueryParams` for Microsoft accounts to control folder hierarchy traversal
* Added support for `earliest_message_date` query parameter for threads
* Fixed `earliest_message_date` not being an optional response field
* Added support for new message fields query parameter values: `include_tracking_options` and `raw_mime`
* Added `tracking_options` field to Message model for message tracking settings
* Added `raw_mime` field to Message model for Base64url-encoded message data
* Added TrackingOptions model for message tracking configuration
* Maintained backwards compatibility for existing message functionality
* Added support for `include_hidden_folders` query parameter for listing folders (Microsoft only)

v6.9.0
----------------
* Added support for for tentative_as_busy parameter to the availability request
* Added missing webhook triggers
* Added support for Notetaker APIs
* Added support for Notetaker via the calendar and event APIs

v6.8.0
----------------
* Added support for `list_import_events`

v6.7.0
----------------
* Added support for `select` query parameter in list calendars, list events, and list messages.

v6.6.0
----------------
* Added response headers to all responses from the Nylas API

v6.5.0
----------------
* Added support for Scheduler APIs
* Added metadata field support for drafts and messages through CreateDraftRequest and Message model
* Fixed attachment download response handling

v6.4.0
----------------
* Added support for from field for sending messages
* Added missing schedule-specific fields to Message model
* Added migration grant properties
* Fixed from field not being optional causing deserialization errors
* Fixed IMAP identifiers not encoding correctly
* Fixed NylasOAuthError not setting the status code properly

v6.3.1
----------------
* Fixed typo on Clean Messages
* Fixed request session being reused across multiple requests
* Added Folder Webhooks
* Removed use of TestCommand

v6.3.0
----------------
* Added Folder query param support
* Added `master_event_id` field to events
* Fixed issue with application models not being deserialized correctly

v6.2.0
----------------
* Added support for custom headers field for drafts and messages
* Added support for overriding various fields of outgoing requests
* Added support for `provider` field in code exchange response
* Added support for `event_type` filtering field for listing events
* Added clean messages support
* Added additional webhook triggers
* Fixed issue where attachments < 3mb were not being encoded correctly
* Fixed issue deserializing event and code exchange responses

v6.1.1
----------------
* Improved message sending and draft create/update performance
* Change default timeout to match API (90 seconds)

v6.1.0
----------------
* Added support for `round_to` field in availability response
* Added support for `attributes` field in folder model
* Added support for icloud as an auth provider
* Fixed webhook secret not returning on creation of webhook
* Fixed issue with free busy and scheduled message responses not being deserialized correctly
* Removed `client_id` from `detect_provider()`

v6.0.1
----------------
* Fix deserialization error when getting token info or verifying access token
* Fix schemas issue in the `Event` and `CodeExchangeResponse` models

v6.0.0
----------------
* **BREAKING CHANGE**: Python SDK v6 supports the Nylas API v3 exclusively, dropping support for any endpoints that are not available in v3
* **BREAKING CHANGE**: Drop support for Python < v3.8
* **BREAKING CHANGE**: Dropped the use of 'Collections' in favor of 'Resources'
* **BREAKING CHANGE**: Removed all REST calls from models and moved them directly into resources
* **BREAKING CHANGE**: Models no longer inherit from `dict` but instead either are a `dataclass` or inherit from `TypedDict`
* **BREAKING CHANGE**: Renamed the SDK entrypoint from `APIClient` to `Client`
* **REMOVED**: Local Webhook development support is removed due to incompatibility
* Rewritten the majority of SDK to be more intuitive, explicit, and efficient
* Created models for all API resources and endpoints, for all HTTP methods to reduce confusion on which fields are available for each endpoint
* Created error classes for the different API errors as well as SDK-specific errors

v5.14.1
----------------
* Fix error when trying to iterate on list after calling count
* Fix error when setting participant status on create event

v5.14.0
----------------
* Add support for `view` parameter in `Threads.search()`

v5.14.1
----------------
* Fix error when trying to iterate on list after calling count
* Fix error when setting participant status on create event

v5.14.0
----------------
* Add support for verifying webhook signatures
* Add optional parameter for token-info endpoint

v5.13.1
----------------
* Fix `send_authorization` not returning the correct dict
* Fix expanded threads not inflating the messages objects properly
* Fix class attributes with leading underscores not serializing as expected

v5.13.0
----------------
* Add local webhook development support
* Use PEP508 syntax for conditional dependencies

v5.12.1
----------------
* Only install enum34 on python34 and below

v5.12.0
----------------
* Add support for sending raw MIME messages

v5.11.0
----------------
* Add support for calendar colors (for Microsoft calendars)
* Add support for rate limit errors
* Add support for visibility field in Event

v5.10.2
----------------
* Update package setup to be compatible with PEP 517

v5.10.1
----------------
* Fix authentication for integrations

v5.10.0
----------------
* Add `metadata` field to `JobStatus`
* Add missing hosted authentication parameters
* Add support for `calendar` field in free-busy, availability, and consecutive availability queries

v5.9.2
----------------
* Add `enforce_read_only` parameter to overriding `as_json` functions

v5.9.1
----------------
* Add option to include read only params in `as_json`
* Change config file in `hosted-oauth` example to match new Flask rules
* Fix unauthorized error for `revoke_token`

v5.9.0
----------------
* Add support for collective and group events

v5.8.0
----------------
* Add support for getting the number of queried objects (count view)
* Improve usage of read only fields in models
* Fix Calendar availability functions not using the correct authentication method

v5.7.0
----------------
* Add Outbox support
* Add support for new (beta) Integrations authentication (Integrations API, Grants API, Hosted Authentication for Integrations)
* Add support for `limit` and `offset` for message/thread search
* Add `authentication_type` field to `Account`
* Enable Nylas API v2.5 support
* Fix `Draft` not sending metadata

v5.6.0
----------------
* Add Delta support
* Add Webhook support
* Omit `None` values from resulting `as_json()` object
* Enable Nylas API v2.4 support

v5.5.1
----------------
* Add validation for `send_authorization`
* Fix `native-authentication-gmail` example app

v5.5.0
----------------
* Add support for `Event` to ICS
* Enable full payload response for exchanging the token for code

v5.4.2
----------------
* Add missing `source` field in `Contact` class

v5.4.1
----------------
* Fix issue where keyword arguments calling `_update_resource` were not correctly resolving to URL params
* Improved support for Application Details

v5.4.0
----------------
* Add job status support
* Add `is_primary` field to Calendar
* Fix bug where updating an Event results in an API error

v5.3.0
----------------
* Add support for Scheduler API
* Add support for Event notifications
* Add support for Component CRUD
* Add metadata support for `Calendar`, `Message` and `Account`
* Improve error details returned from the API

v5.2.0
----------------
* Add support for calendar consecutive availability
* Add dynamic conferencing link creation support

v5.1.0
----------------
* Add Event conferencing support
* Add filtering of "None" value attributes before making requests
* Fix `categorized_at` type to be `epoch` in `NeuralCategorizer`

v5.0.0
----------------
* Transitioned from `app_id` and `app_secret` naming to `client_id` and `client_secret`
* Add support for the Nylas Neural API
* Add `metadata` field in the Event model to support new event metadata feature
* Add new Room Resource fields
* Add `Nylas-API-Version` header support
* Fix adding a tracking object to an existing `draft`
* Fix issue when converting offset-aware `datetime` objects to `timestamp`
* Fix `limit` value in filter not being used when making `.all()` call
* Fix `from_` field set by attribute on draft ignored
* Remove `bumpversion` from a required dependency to an extra dependency

v4.12.1
-------
* Bugfix: Previously, if you passed a timedelta to the calendar availability
  API endpoint, it was converted to a float. Now, it is coerced to an int.

v4.12.0
-------
* Add calendar availability information, available at `/calendars/availability` API endpoint

v4.11.0
-------
* Bugfix: Previously, if you specified a limit of 50 or more for any resource, you would receive ALL the resources available on the server. The SDK now properly respects the limit provided.
* Add `has_attachments` to Thread model

v4.10.0
-------
* Add `ical_uid` to Event model, only available on API version 2.1 or above. See https://headwayapp.co/nylas-changelog/icaluid-support-132816
* Add RoomResource model, available at `/resources` API endpoint
* Add free/busy information, available at `/calendars/free-busy` API endpoint

v4.9.0
------
* Add `provider` to Account model
* Add `reply_to` to Message model
* Add `Event.rsvp()` method

v4.8.1
------
* Bugfix: `/token-info` endpoint

v4.8.0
------
* Add support for `/token-info` endpoint, which allows you to query the
  available scopes and validity of a given access token for an account.
* Add message.from_ alias
* Bugfix: contact.email_addresses renamed to contact.emails

v4.7.0
------
* Add support for `/ip_addresses` endpoint.

v4.6.0
------
* You can now pass a list of `scopes` when calling `APIClient.authentication_url()`
  in order to enable
  [selective sync](https://docs.nylas.com/docs/how-to-use-selective-sync).
  Previously, we only set `scope=email` by default; now, the default is to use
  all scopes.
* Add X-Nylas-Client-Id header for HTTP requests

v4.4.0
------
* Add support for `revoke-all` endpoint.


v4.3.0
------
* Raise `UnsyncedError` when a message isn't ready to be retrieved yet (HTTP 202) when
fetching a raw message.


v4.2.0
------



v3.0.0
------

## Large changes

* The Nylas Python SDK now fully supports both Python 2.7 and Python 3.3+.
* The SDK has a new dependency: the
  [URLObject](https://pypi.python.org/pypi/URLObject) library.
  This dependency will be automatically installed when you upgrade.
* The SDK now automatically converts between timestamps and Python datetime
  objects. These automatic conversions are opt-in: your existing code should
  continue to work unmodified. See the "Timestamps and Datetimes"
  section of this document for more information.

## Small changes

* The SDK now has over 95% automated test coverage.
* Previously, trying to access the following model properties would raise an error:
  `Folder.threads`, `Folder.messages`, `Label.threads`, `Label.messages`.
  These properties should now work as expected.
* The `Thread` model now exposes the `last_message_received_timestamp` and
  `last_message_sent_timestamp` properties, obtained from the Nylas API.
* Previously, if you created a `Draft` object, saved it, and then
  deleted it without modifying it further, the deletion would fail silently.
  Now, the SDK will actually attempt to delete a newly-saved `Draft` object,
  and will raise an error if it is unable to do so.
* Previously, you could initialize an `APIClient` with an `api_server`
  value set to an `http://` URL. Now, `APIClient` will verify that the
  `api_server` value starts with `https://`, and will raise an error if it
  does not.
* The `APIClient` constructor no longers accepts the `auth_server` argument,
  as it was never used for anything.
* The `nylas.client.util.url_concat` and `nylas.client.util.generate_id`
  functions have been removed. These functions were meant for internal use,
  and were never documented or expected to be used by others.
* You can now pass a `state` argument to `APIClient.authentication_url`,
  as per the OAuth 2.0 spec.

## Timestamps and Datetimes

Some properties in the Nylas API use timestamp integers to represent a specific
moment in time, such as `Message.date`. The Python SDK now exposes new properties
that have converted these existing properties from integers to Python datetime
objects. You can still access the existing properties to get the timestamp
integer -- these new properties are just a convenient way to access Python
datetime objects, if you want them.

This table summarizes the new datetime properties, and which existing timestamp
properties they match up with.

| New Property (datetime)           | Existing Property (timestamp)            |
| --------------------------------- | ---------------------------------------- |
| `Message.received_at`             | `Message.date`                           |
| `Thread.first_message_at`         | `Thread.first_message_timestamp`         |
| `Thread.last_message_at`          | `Thread.last_message_timestamp`          |
| `Thread.last_message_received_at` | `Thread.last_message_received_timestamp` |
| `Thread.last_message_sent_at`     | `Thread.last_message_sent_timestamp`     |
| `Draft.last_modified_at`          | `Draft.date`                             |
| `Event.original_start_at`         | `Event.original_start_time`              |

You can also use datetime objects when filtering on models with the `.where()`
method. For example, if you wanted to find all messages that were received
before Jan 1, 2015, previously you would run this code:

```python
client.messages.where(received_before=1420070400).all()
```

That code will still work, but if you prefer, you can run this code instead:

```python
from datetime import datetime

client.messages.where(received_before=datetime(2015, 1, 1)).all()
```

You can now use datetimes with the following filters:

* `client.messages.where(received_before=datetime())`
* `client.messages.where(received_after=datetime())`
* `client.threads.where(last_message_before=datetime())`
* `client.threads.where(last_message_after=datetime())`
* `client.threads.where(started_before=datetime())`
* `client.threads.where(started_after=datetime())`


[Full Changelog](https://github.com/nylas/nylas-python/compare/v2.0.0...v3.0.0)


v2.0.0
------

Release May 18, 2017:
- Add support for expanded message view
- Remove deprecated "Inbox" name
- Send correct auth headers for account management
- Respect the offset parameter for restfulmodelcollection
- Add ability to revoke token

[Full Changelog](https://github.com/nylas/nylas-python/compare/v1.2.3...v2.0.0)


v1.2.3
------

Release August 9, 2016:
- Adds full-text search support for Messages and Threads

v1.2.2
------

Released March 25, 2016:
- API client now uses Bearer Token Authorization headers instead of Basic Auth

v1.2.1
------

Released February 5, 2016:
- Fixes a bug that prevented the offset parameter from being used in queries

v1.2.0
------

Released December 17, 2015:

- Deprecate tags and tag-related functions.
- Return message object when sending a draft
- Support passing parameters and request bodies on delete

v1.1.0
------

Released October 8, 2015:

- Add client.account property

v1.0.2
------

Released September 22, 2015:

- Add handling for 405 responses
- Surface SMTP server errors
- Expose Message attributes: events, snippet
- Expose Folder and Label attributes: object, account_id
- Expose Thread attribute: received_recent_date
- Expose Draft attributes: reply_to_message_id, reply_to, starred, snippet
- Expose File attributes: content_id, message_ids
- Expose "object" attribute on Calendar, Event, and Contact
- Add local token for tests

v1.0.1
------

Released September 17, 2015:

Expose "owner" attribute on Events
Clean up raw message data

v1.0.0
------

Released August 28, 2015:

Don't first save draft objects when a direct send is possible.
Remove deprecated namespaces support from SDK
Account management fixes and upgrade/downgrade changes
Added tests

v0.3.5
------
Drafts can now be sent without an implicit intermediate save to the mail provider.


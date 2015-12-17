nylas-python Changelog
======================

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


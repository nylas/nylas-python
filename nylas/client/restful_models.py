from datetime import datetime
from collections import defaultdict
from enum import Enum

from six import StringIO
from nylas.client.restful_model_collection import RestfulModelCollection
from nylas.client.errors import FileUploadError, UnSyncedError, NylasApiError
from nylas.utils import timestamp_from_dt

# pylint: disable=attribute-defined-outside-init


def typed_dict_attr(items, attr_name=None):
    if attr_name:
        pairs = [(item["type"], item[attr_name]) for item in items]
    else:
        pairs = [(item["type"], item) for item in items]
    dct = defaultdict(list)
    for key, value in pairs:
        dct[key].append(value)
    return dct


def _is_subclass(cls, parent):
    for base in cls.__bases__:
        if base.__name__.lower() == parent:
            return True
    return False


class RestfulModel(dict):
    attrs = []
    date_attrs = {}
    datetime_attrs = {}
    datetime_filter_attrs = {}
    typed_dict_attrs = {}
    read_only_attrs = {}
    # The Nylas API holds most objects for an account directly under '/',
    # but some of them are under '/a' (mostly the account-management
    # and billing code). api_root is a tiny metaprogramming hack to let
    # us use the same code for both.
    api_root = None

    def __init__(self, cls, api):
        self.id = None
        self.cls = cls
        self.api = api
        super(RestfulModel, self).__init__()

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    __getattr__ = dict.get

    @classmethod
    def create(cls, api, **kwargs):
        object_type = kwargs.get("object")
        cls_object_type = getattr(cls, "object_type", cls.__name__.lower())
        # These are classes that should bypass the check below because they
        # often represent other types (e.g. a delta's object type might be event)
        class_check_whitelist = ["jobstatus", "delta"]
        if (
            object_type
            and object_type != cls_object_type
            and object_type != "account"
            and cls_object_type not in class_check_whitelist
            and not _is_subclass(cls, object_type)
        ):
            # We were given a specific object type and we're trying to
            # instantiate something different; abort. (Relevant for folders
            # and labels API.)
            # We need a special case for accounts because the /accounts API
            # is different between the open source and hosted API.
            # And a special case for job status because the object refers to
            # the type of objects' job status
            return
        obj = cls(api)  # pylint: disable=no-value-for-parameter
        obj.cls = cls
        for attr in cls.attrs:
            # Support attributes we want to override with properties where
            # the property names overlap with the JSON names (e.g. folders)
            attr_name = attr
            if attr_name.startswith("_"):
                attr = attr_name[1:]
            if attr in kwargs:
                obj[attr_name] = kwargs[attr]
                if attr_name == "from":
                    obj["from_"] = kwargs[attr]
        for date_attr, iso_attr in cls.date_attrs.items():
            if kwargs.get(iso_attr):
                obj[date_attr] = datetime.strptime(kwargs[iso_attr], "%Y-%m-%d").date()
        for dt_attr, ts_attr in cls.datetime_attrs.items():
            if kwargs.get(ts_attr):
                try:
                    obj[dt_attr] = datetime.utcfromtimestamp(kwargs[ts_attr])
                except TypeError:
                    # If the datetime format is in the format of ISO8601
                    obj[dt_attr] = datetime.strptime(
                        kwargs[ts_attr], "%Y-%m-%dT%H:%M:%S.%fZ"
                    )
        for attr, value_attr_name in cls.typed_dict_attrs.items():
            obj[attr] = typed_dict_attr(kwargs.get(attr, []), attr_name=value_attr_name)

        if "id" not in kwargs:
            obj["id"] = None

        return obj

    def as_json(self):
        dct = {}
        # Some API parameters like "from" and "in" also are
        # Python reserved keywords. To work around this, we rename
        # them to "from_" and "in_". The API still needs them in
        # their correct form though.
        reserved_keywords = ["from", "in"]
        for attr in self.cls.attrs:
            if attr in self.read_only_attrs:
                continue
            if hasattr(self, attr):
                if attr in reserved_keywords:
                    attr_value = getattr(self, "{}_".format(attr))
                else:
                    attr_value = getattr(self, attr)
                if attr_value is not None:
                    dct[attr] = attr_value
        for date_attr, iso_attr in self.cls.date_attrs.items():
            if date_attr in self.read_only_attrs:
                continue
            if self.get(date_attr):
                dct[iso_attr] = self[date_attr].strftime("%Y-%m-%d")
        for dt_attr, ts_attr in self.cls.datetime_attrs.items():
            if dt_attr in self.read_only_attrs:
                continue
            if self.get(dt_attr):
                dct[ts_attr] = timestamp_from_dt(self[dt_attr])
        for attr, value_attr in self.cls.typed_dict_attrs.items():
            if attr in self.read_only_attrs:
                continue
            typed_dict = getattr(self, attr)
            if value_attr:
                dct[attr] = []
                for key, values in typed_dict.items():
                    for value in values:
                        dct[attr].append({"type": key, value_attr: value})
            else:
                dct[attr] = []
                for values in typed_dict.values():
                    for value in values:
                        dct[attr].append(value)
        return dct


class NylasAPIObject(RestfulModel):
    def __init__(self, cls, api):
        RestfulModel.__init__(self, cls, api)

    def child_collection(self, cls, **filters):
        return RestfulModelCollection(cls, self.api, **filters)

    def save(self, **kwargs):
        if self.id:
            new_obj = self.api._update_resource(
                self.cls, self.id, self.as_json(), **kwargs
            )
        else:
            new_obj = self.api._create_resource(self.cls, self.as_json(), **kwargs)
        for attr in self.cls.attrs:
            if hasattr(new_obj, attr):
                setattr(self, attr, getattr(new_obj, attr))

    def update(self):
        new_obj = self.api._update_resource(self.cls, self.id, self.as_json())
        for attr in self.cls.attrs:
            if hasattr(new_obj, attr):
                setattr(self, attr, getattr(new_obj, attr))


class Message(NylasAPIObject):
    attrs = [
        "bcc",
        "body",
        "cc",
        "date",
        "events",
        "files",
        "from",
        "id",
        "account_id",
        "object",
        "snippet",
        "starred",
        "subject",
        "thread_id",
        "job_status_id",
        "to",
        "unread",
        "starred",
        "metadata",
        "_folder",
        "_labels",
        "headers",
        "reply_to",
    ]
    datetime_attrs = {"received_at": "date"}
    datetime_filter_attrs = {
        "received_before": "received_before",
        "received_after": "received_after",
    }
    collection_name = "messages"

    def __init__(self, api):
        NylasAPIObject.__init__(self, Message, api)

    @property
    def attachments(self):
        return self.child_collection(File, message_id=self.id)

    @property
    def folder(self):
        # Instantiate a Folder object from the API response
        if self._folder:
            return Folder.create(self.api, **self._folder)

    @property
    def labels(self):
        if self._labels:
            return [Label.create(self.api, **l) for l in self._labels]
        return []

    def update_folder(self, folder_id):
        update = {"folder": folder_id}
        new_obj = self.api._update_resource(self.cls, self.id, update)
        for attr in self.cls.attrs:
            if hasattr(new_obj, attr):
                setattr(self, attr, getattr(new_obj, attr))
        return self.folder

    def update_labels(self, label_ids=None):
        label_ids = label_ids or []
        update = {"labels": label_ids}
        new_obj = self.api._update_resource(self.cls, self.id, update)
        for attr in self.cls.attrs:
            if hasattr(new_obj, attr):
                setattr(self, attr, getattr(new_obj, attr))
        return self.labels

    def add_labels(self, label_ids=None):
        label_ids = label_ids or []
        labels = [l.id for l in self.labels]
        labels = list(set(labels).union(set(label_ids)))
        return self.update_labels(labels)

    def add_label(self, label_id):
        return self.add_labels([label_id])

    def remove_labels(self, label_ids=None):
        label_ids = label_ids or []
        labels = [l.id for l in self.labels]
        labels = list(set(labels) - set(label_ids))
        return self.update_labels(labels)

    def remove_label(self, label_id):
        return self.remove_labels([label_id])

    def mark_as_seen(self):
        self.mark_as_read()

    def mark_as_read(self):
        update = {"unread": False}
        self.api._update_resource(self.cls, self.id, update)
        self.unread = False

    def mark_as_unread(self):
        update = {"unread": True}
        self.api._update_resource(self.cls, self.id, update)
        self.unread = True

    def star(self):
        update = {"starred": True}
        self.api._update_resource(self.cls, self.id, update)
        self.starred = True

    def unstar(self):
        update = {"starred": False}
        self.api._update_resource(self.cls, self.id, update)
        self.starred = False

    @property
    def raw(self):
        headers = {"Accept": "message/rfc822"}
        response = self.api._get_resource_raw(Message, self.id, headers=headers)
        if response.status_code == 202:
            raise UnSyncedError(response.content)
        return response.content


class Folder(NylasAPIObject):
    attrs = ["id", "display_name", "name", "object", "account_id", "job_status_id"]
    collection_name = "folders"

    def __init__(self, api):
        NylasAPIObject.__init__(self, Folder, api)

    @property
    def threads(self):
        return self.child_collection(Thread, folder_id=self.id)

    @property
    def messages(self):
        return self.child_collection(Message, folder_id=self.id)


class Label(NylasAPIObject):
    attrs = ["id", "display_name", "name", "object", "account_id", "job_status_id"]
    collection_name = "labels"

    def __init__(self, api):
        NylasAPIObject.__init__(self, Label, api)

    @property
    def threads(self):
        return self.child_collection(Thread, label_id=self.id)

    @property
    def messages(self):
        return self.child_collection(Message, label_id=self.id)


class Thread(NylasAPIObject):
    attrs = [
        "draft_ids",
        "id",
        "message_ids",
        "account_id",
        "object",
        "participants",
        "snippet",
        "subject",
        "subject_date",
        "last_message_timestamp",
        "first_message_timestamp",
        "last_message_received_timestamp",
        "last_message_sent_timestamp",
        "unread",
        "starred",
        "version",
        "_folders",
        "_labels",
        "received_recent_date",
        "has_attachments",
    ]
    datetime_attrs = {
        "first_message_at": "first_message_timestamp",
        "last_message_at": "last_message_timestamp",
        "last_message_received_at": "last_message_received_timestamp",
        "last_message_sent_at": "last_message_sent_timestamp",
    }
    datetime_filter_attrs = {
        "last_message_before": "last_message_before",
        "last_message_after": "last_message_after",
        "started_before": "started_before",
        "started_after": "started_after",
    }
    collection_name = "threads"

    def __init__(self, api):
        NylasAPIObject.__init__(self, Thread, api)

    @property
    def messages(self):
        return self.child_collection(Message, thread_id=self.id)

    @property
    def drafts(self):
        return self.child_collection(Draft, thread_id=self.id)

    @property
    def folders(self):
        if self._folders:
            return [Folder.create(self.api, **f) for f in self._folders]
        return []

    @property
    def labels(self):
        if self._labels:
            return [Label.create(self.api, **l) for l in self._labels]
        return []

    def update_folder(self, folder_id):
        update = {"folder": folder_id}
        new_obj = self.api._update_resource(self.cls, self.id, update)
        for attr in self.cls.attrs:
            if hasattr(new_obj, attr):
                setattr(self, attr, getattr(new_obj, attr))
        return self.folder

    def update_labels(self, label_ids=None):
        label_ids = label_ids or []
        update = {"labels": label_ids}
        new_obj = self.api._update_resource(self.cls, self.id, update)
        for attr in self.cls.attrs:
            if hasattr(new_obj, attr):
                setattr(self, attr, getattr(new_obj, attr))
        return self.labels

    def add_labels(self, label_ids=None):
        label_ids = label_ids or []
        labels = [l.id for l in self.labels]
        labels = list(set(labels).union(set(label_ids)))
        return self.update_labels(labels)

    def add_label(self, label_id):
        return self.add_labels([label_id])

    def remove_labels(self, label_ids=None):
        label_ids = label_ids or []
        labels = [l.id for l in self.labels]
        labels = list(set(labels) - set(label_ids))
        return self.update_labels(labels)

    def remove_label(self, label_id):
        return self.remove_labels([label_id])

    def mark_as_seen(self):
        self.mark_as_read()

    def mark_as_read(self):
        update = {"unread": False}
        self.api._update_resource(self.cls, self.id, update)
        self.unread = False

    def mark_as_unread(self):
        update = {"unread": True}
        self.api._update_resource(self.cls, self.id, update)
        self.unread = True

    def star(self):
        update = {"starred": True}
        self.api._update_resource(self.cls, self.id, update)
        self.starred = True

    def unstar(self):
        update = {"starred": False}
        self.api._update_resource(self.cls, self.id, update)
        self.starred = False

    def create_reply(self):
        draft = self.drafts.create()
        draft.thread_id = self.id
        draft.subject = self.subject
        return draft


# This is a dummy class that allows us to use the create_resource function
# and pass in a 'Send' object that will translate into a 'send' endpoint.
class Send(Message):
    collection_name = "send"

    def __init__(self, api):  # pylint: disable=super-init-not-called
        NylasAPIObject.__init__(
            self, Send, api
        )  # pylint: disable=non-parent-init-called


class Draft(Message):
    attrs = [
        "bcc",
        "cc",
        "body",
        "date",
        "files",
        "from",
        "id",
        "account_id",
        "object",
        "subject",
        "thread_id",
        "to",
        "job_status_id",
        "unread",
        "version",
        "file_ids",
        "reply_to_message_id",
        "reply_to",
        "starred",
        "snippet",
        "tracking",
    ]
    datetime_attrs = {"last_modified_at": "date"}
    collection_name = "drafts"

    def __init__(self, api, thread_id=None):  # pylint: disable=unused-argument
        Message.__init__(self, api)
        NylasAPIObject.__init__(
            self, Thread, api
        )  # pylint: disable=non-parent-init-called
        self.file_ids = []

    def attach(self, file):
        if not file.id:
            file.save()

        self.file_ids.append(file.id)

    def detach(self, file):
        if file.id in self.file_ids:
            self.file_ids.remove(file.id)

    def send(self):
        if not self.id:
            data = self.as_json()
        else:
            data = {"draft_id": self.id}
            if hasattr(self, "version"):
                data["version"] = self.version
            if hasattr(self, "tracking") and self.tracking is not None:
                data["tracking"] = self.tracking

        msg = self.api._create_resource(Send, data)
        if msg:
            return msg

    def delete(self):
        if self.id and self.version is not None:
            data = {"version": self.version}
            self.api._delete_resource(self.cls, self.id, data=data)


class File(NylasAPIObject):
    attrs = [
        "content_type",
        "filename",
        "id",
        "content_id",
        "account_id",
        "object",
        "size",
        "message_ids",
    ]
    collection_name = "files"

    def save(self):  # pylint: disable=arguments-differ
        stream = getattr(self, "stream", None)
        if not stream:
            data = getattr(self, "data", None)
            if data:
                stream = StringIO(data)

        if not stream:
            message = (
                "File object not properly formatted, "
                "must provide either a stream or data."
            )
            raise FileUploadError(message)

        file_info = (self.filename, stream, self.content_type, {})  # upload headers

        new_obj = self.api._create_resources(File, {"file": file_info})
        new_obj = new_obj[0]
        for attr in self.attrs:
            if hasattr(new_obj, attr):
                setattr(self, attr, getattr(new_obj, attr))

    def download(self):
        if not self.id:
            message = "Can't download a file that hasn't been uploaded."
            raise FileUploadError(message)

        return self.api._get_resource_data(File, self.id, extra="download")

    def __init__(self, api):
        NylasAPIObject.__init__(self, File, api)


class Contact(NylasAPIObject):
    attrs = [
        "id",
        "object",
        "account_id",
        "given_name",
        "middle_name",
        "surname",
        "suffix",
        "nickname",
        "company_name",
        "job_title",
        "job_status_id",
        "manager_name",
        "office_location",
        "source",
        "notes",
        "picture_url",
    ]
    date_attrs = {"birthday": "birthday"}
    typed_dict_attrs = {
        "emails": "email",
        "im_addresses": "im_address",
        "physical_addresses": None,
        "phone_numbers": "number",
        "web_pages": "url",
    }
    collection_name = "contacts"

    def __init__(self, api):
        NylasAPIObject.__init__(self, Contact, api)

    def get_picture(self):
        if not self.get("picture_url", None):
            return None

        response = self.api._get_resource_raw(
            Contact, self.id, extra="picture", stream=True
        )
        if response.status_code >= 400:
            raise NylasApiError(response)
        return response.raw


class Calendar(NylasAPIObject):
    attrs = [
        "id",
        "account_id",
        "name",
        "description",
        "job_status_id",
        "metadata",
        "read_only",
        "is_primary",
        "object",
    ]
    collection_name = "calendars"

    def __init__(self, api):
        NylasAPIObject.__init__(self, Calendar, api)

    @property
    def events(self):
        return self.child_collection(Event, calendar_id=self.id)


class Event(NylasAPIObject):
    attrs = [
        "id",
        "account_id",
        "title",
        "description",
        "conferencing",
        "location",
        "read_only",
        "when",
        "busy",
        "participants",
        "calendar_id",
        "recurrence",
        "status",
        "master_event_id",
        "job_status_id",
        "owner",
        "original_start_time",
        "object",
        "message_id",
        "ical_uid",
        "metadata",
        "notifications",
    ]
    datetime_attrs = {"original_start_at": "original_start_time"}
    collection_name = "events"

    def __init__(self, api):
        NylasAPIObject.__init__(self, Event, api)

    def as_json(self):
        dct = NylasAPIObject.as_json(self)
        # Filter some parameters we got from the API
        if dct.get("when"):
            # Currently, the event (self) and the dict (dct) share the same
            # reference to the `'when'` dict.  We need to clone the dict so
            # that when we remove the object key, the original event's
            # `'when'` reference is unmodified.
            dct["when"] = dct["when"].copy()
            dct["when"].pop("object", None)

        if dct.get("participants") and isinstance(dct.get("participants"), list):
            # The status of a participant cannot be updated and, if the key is
            # included, it will return an error from the API
            for participant in dct.get("participants"):
                participant.pop("status", None)

        return dct

    def rsvp(self, status, comment=None):
        if not self.message_id:
            raise ValueError(
                "This event was not imported from an iCalendar invite, and so it is not possible to RSVP via Nylas"
            )
        if status not in {"yes", "no", "maybe"}:
            raise ValueError("invalid status: {status}".format(status=status))

        url = "{api_server}/send-rsvp".format(api_server=self.api.api_server)
        data = {
            "event_id": self.id,
            "status": status,
            "comment": comment,
        }
        response = self.api.session.post(url, json=data)
        if response.status_code >= 400:
            raise NylasApiError(response)
        result = response.json()
        return Event.create(self, **result)

    def generate_ics(self, ical_uid=None, method=None, prodid=None):
        """
        Generate an ICS file server-side, from an Event

        Args:
            ical_uid (str): Unique identifier used events across calendaring systems
            method (str): Description of invitation and response methods for attendees
            prodid (str): Company-specific unique product identifier

        Returns:
            str: String for writing directly into an ICS file

        Raises:
            ValueError: If the event does not have calendar_id or when set
            RuntimeError: If the server returns an object without an ics string
        """
        if not self.calendar_id or not self.when:
            raise ValueError(
                "Cannot generate an ICS file for an event without a Calendar ID or when set"
            )

        payload = {}
        ics_options = {}
        if self.id:
            payload["event_id"] = self.id
        else:
            payload = self.as_json()

        if ical_uid:
            ics_options["ical_uid"] = ical_uid
        if method:
            ics_options["method"] = method
        if prodid:
            ics_options["prodid"] = prodid

        if ics_options:
            payload["ics_options"] = ics_options

        response = self.api._post_resource(Event, None, "to-ics", payload)
        if "ics" in response:
            return response["ics"]
        raise RuntimeError(
            "Unexpected response from the API server. Returned 200 but no 'ics' string found."
        )

    def save(self, **kwargs):
        if (
            self.conferencing
            and "details" in self.conferencing
            and "autocreate" in self.conferencing
        ):
            raise ValueError(
                "Cannot set both 'details' and 'autocreate' in conferencing object."
            )

        super(Event, self).save(**kwargs)


class RoomResource(NylasAPIObject):
    attrs = [
        "object",
        "email",
        "name",
        "capacity",
        "building",
        "floor_name",
        "floor_number",
    ]
    object_type = "room_resource"
    collection_name = "resources"

    def __init__(self, api):
        NylasAPIObject.__init__(self, RoomResource, api)


class JobStatus(NylasAPIObject):
    attrs = [
        "id",
        "account_id",
        "job_status_id",
        "action",
        "object",
        "status",
        "original_data",
    ]
    datetime_attrs = {"created_at": "created_at"}
    collection_name = "job-statuses"

    def __init__(self, api):
        NylasAPIObject.__init__(self, JobStatus, api)

    def is_successful(self):
        return self.status == "successful"


class Scheduler(NylasAPIObject):
    attrs = [
        "id",
        "access_tokens",
        "app_client_id",
        "app_organization_id",
        "config",
        "edit_token",
        "name",
        "slug",
    ]
    date_attrs = {
        "created_at": "created_at",
        "modified_at": "modified_at",
    }
    collection_name = "manage/pages"

    def __init__(self, api):
        NylasAPIObject.__init__(self, Scheduler, api)

    def get_available_calendars(self):
        if not self.id:
            raise ValueError("Cannot get calendars for a page without an ID")

        response = self.api._get_resource_raw(Scheduler, self.id, extra="calendars")
        response_body = response.json()
        for body in response_body:
            for i in range(len(body["calendars"])):
                body["calendars"][i] = Calendar.create(self.api, **body["calendars"][i])

        return response_body

    def upload_image(self, content_type, object_name):
        if not self.id:
            raise ValueError("Cannot upload an image to a page without an ID")

        data = {"contentType": content_type, "objectName": object_name}
        response = self.api._put_resource(
            Scheduler, self.id, data, extra="upload-image"
        )
        return response


class Component(NylasAPIObject):
    attrs = [
        "id",
        "account_id",
        "name",
        "type",
        "action",
        "active",
        "settings",
        "public_account_id",
        "public_token_id",
        "public_application_id",
        "access_token",
        "allowed_domains",
    ]
    datetime_attrs = {
        "created_at": "created_at",
        "updated_at": "updated_at",
    }
    read_only_attrs = {"id", "public_application_id", "created_at", "updated_at"}

    collection_name = None
    api_root = "component"

    def __init__(self, api):
        NylasAPIObject.__init__(self, Component, api)

    def as_json(self):
        dct = NylasAPIObject.as_json(self)
        # "type" cannot be modified after created
        if self.id:
            dct.pop("type")
        return dct


class Webhook(NylasAPIObject):
    attrs = (
        "id",
        "callback_url",
        "state",
        "triggers",
        "application_id",
        "version",
    )
    read_only_attrs = {"id", "application_id", "version"}

    collection_name = "webhooks"
    api_root = "a"

    def __init__(self, api):
        NylasAPIObject.__init__(self, Webhook, api)

    def as_json(self):
        dct = {}
        # Only 'state' can get updated
        if self.id:
            dct["state"] = self.state
        else:
            dct = NylasAPIObject.as_json(self)
        return dct

    class Trigger(str, Enum):
        """
        This is an Enum representing all the possible webhook triggers

        see more: https://developer.nylas.com/docs/developer-tools/webhooks/available-webhooks
        """

        ACCOUNT_CONNECTED = "account.connected"
        ACCOUNT_RUNNING = "account.running"
        ACCOUNT_STOPPED = "account.stopped"
        ACCOUNT_INVALID = "account.invalid"
        ACCOUNT_SYNC_ERROR = "account.sync_error"
        MESSAGE_CREATED = "message.created"
        MESSAGE_OPENED = "message.opened"
        MESSAGE_UPDATED = "message.updated"
        MESSAGE_LINK_CLICKED = "message.link_clicked"
        THREAD_REPLIED = "thread.replied"
        CONTACT_CREATED = "contact.created"
        CONTACT_UPDATED = "contact.updated"
        CONTACT_DELETED = "contact.deleted"
        CALENDAR_CREATED = "calendar.created"
        CALENDAR_UPDATED = "calendar.updated"
        CALENDAR_DELETED = "calendar.deleted"
        EVENT_CREATED = "event.created"
        EVENT_UPDATED = "event.updated"
        EVENT_DELETED = "event.deleted"
        JOB_SUCCESSFUL = "job.successful"
        JOB_FAILED = "job.failed"

    class State(str, Enum):
        """
        This is an Enum representing all the possible webhook states

        see more: https://developer.nylas.com/docs/developer-tools/webhooks/#enable-and-disable-webhooks
        """

        ACTIVE = "active"
        INACTIVE = "inactive"


class Namespace(NylasAPIObject):
    attrs = [
        "account",
        "email_address",
        "id",
        "account_id",
        "object",
        "provider",
        "name",
        "organization_unit",
    ]
    collection_name = "n"

    def __init__(self, api):
        NylasAPIObject.__init__(self, Namespace, api)

    def child_collection(self, cls, **filters):
        return RestfulModelCollection(cls, self.api, self.id, **filters)


class Account(NylasAPIObject):
    api_root = "a"

    attrs = [
        "account_id",
        "billing_state",
        "email",
        "id",
        "namespace_id",
        "provider",
        "sync_state",
        "trial",
        "metadata",
    ]

    collection_name = "accounts"

    def __init__(self, api):
        NylasAPIObject.__init__(self, Account, api)

    def as_json(self):
        dct = {"metadata": self.metadata}
        return dct

    def upgrade(self):
        return self.api._call_resource_method(self, self.account_id, "upgrade", None)

    def downgrade(self):
        return self.api._call_resource_method(self, self.account_id, "downgrade", None)


class APIAccount(NylasAPIObject):
    attrs = [
        "account_id",
        "email_address",
        "id",
        "name",
        "object",
        "organization_unit",
        "provider",
        "sync_state",
    ]
    datetime_attrs = {"linked_at": "linked_at"}

    collection_name = "accounts"

    def __init__(self, api):
        NylasAPIObject.__init__(self, APIAccount, api)

    def as_json(self):
        dct = NylasAPIObject.as_json(self)
        return dct


class SingletonAccount(APIAccount):
    # This is an APIAccount that lives under /account.
    collection_name = "account"

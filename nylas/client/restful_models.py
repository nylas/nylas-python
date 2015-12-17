from .restful_model_collection import RestfulModelCollection
from .errors import FileUploadError
from six import StringIO
import base64
import json


class NylasAPIObject(dict):
    attrs = []
    # The Nylas API holds most objects for an account directly under '/',
    # but some of them are under '/a' (mostly the account-management
    # and billing code). api_root is a tiny metaprogramming hack to let
    # us use the same code for both.
    api_root = 'n'

    def __init__(self, cls, api):
        self.id = None
        self.cls = cls
        self.api = api

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    __getattr__ = dict.get

    @classmethod
    def create(cls, api, **kwargs):
        object_type = kwargs.get('object')
        if (object_type and object_type != cls.__name__.lower() and
                object_type != 'account'):
            # We were given a specific object type and we're trying to
            # instantiate something different; abort. (Relevant for folders
            # and labels API.)
            # We need a special case for accounts because the /accounts API
            # is different between the open source and hosted API.
            return
        obj = cls(api)
        obj.cls = cls
        for attr in cls.attrs:
            # Support attributes we want to override with properties where
            # the property names overlap with the JSON names (e.g. folders)
            attr_name = attr
            if attr_name.startswith('_'):
                attr = attr_name[1:]
            if attr in kwargs:
                obj[attr_name] = kwargs[attr]
        if 'id' not in kwargs:
            obj['id'] = None

        return obj

    def as_json(self):
        dct = {}
        for attr in self.cls.attrs:
            if hasattr(self, attr):
                dct[attr] = getattr(self, attr)
        return dct

    def child_collection(self, cls, **filters):
        return RestfulModelCollection(cls, self.api, **filters)

    def save(self, **kwargs):
        if self.id:
            new_obj = self.api._update_resource(self.cls, self.id,
                                                self.as_json(), **kwargs)
        else:
            new_obj = self.api._create_resource(self.cls,
                                                self.as_json(), **kwargs)
        for attr in self.cls.attrs:
            if hasattr(new_obj, attr):
                setattr(self, attr, getattr(new_obj, attr))

    def update(self):
        new_obj = self.api._update_resource(self.cls,
                                            self.id, self.as_json())
        for attr in self.cls.attrs:
            if hasattr(new_obj, attr):
                setattr(self, attr, getattr(new_obj, attr))


class Message(NylasAPIObject):
    attrs = ["bcc", "body", "cc", "date", "events", "files", "from", "id",
             "account_id", "object", "snippet", "starred", "subject",
             "thread_id", "to", "unread", "starred", "_folder", "_labels"]
    collection_name = 'messages'

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
            return [Label.create(self.api, **l)
                    for l in self._labels]
        else:
            return []

    def update_folder(self, folder_id):
        update = {'folder': folder_id}
        new_obj = self.api._update_resource(self.cls, self.id, update)
        for attr in self.cls.attrs:
            if hasattr(new_obj, attr):
                setattr(self, attr, getattr(new_obj, attr))
        return self.folder

    def update_labels(self, label_ids=[]):
        update = {'labels': label_ids}
        new_obj = self.api._update_resource(self.cls, self.id, update)
        for attr in self.cls.attrs:
            if hasattr(new_obj, attr):
                setattr(self, attr, getattr(new_obj, attr))
        return self.labels

    def add_labels(self, label_ids=[]):
        labels = [l.id for l in self.labels]
        labels = list(set(labels).union(set(label_ids)))
        return self.update_labels(labels)

    def add_label(self, label_id):
        return self.add_labels([label_id])

    def remove_labels(self, label_ids=[]):
        labels = [l.id for l in self.labels]
        labels = list(set(labels) - set(label_ids))
        return self.update_labels(labels)

    def remove_label(self, label_id):
        return self.remove_labels([label_id])

    def mark_as_seen(self):
        self.mark_as_read()

    def mark_as_read(self):
        update = {'unread': False}
        self.api._update_resource(self.cls, self.id, update)
        self.unread = False

    def mark_as_unread(self):
        update = {'unread': True}
        self.api._update_resource(self.cls, self.id, update)
        self.unread = True

    def star(self):
        update = {'starred': True}
        self.api._update_resource(self.cls, self.id, update)
        self.starred = True

    def unstar(self):
        update = {'starred': False}
        self.api._update_resource(self.cls, self.id, update)
        self.starred = False

    @property
    def raw(self):
        headers = {"Accept": "message/rfc822"}
        data = self.api._get_resource_data(Message, self.id, headers=headers)
        return data


class Folder(NylasAPIObject):
    attrs = ["id", "display_name", "name", "object", "account_id"]
    collection_name = "folders"

    def __init__(self, api):
        NylasAPIObject.__init__(self, Folder, api)

    @property
    def threads(self):
        return self.child_collection({'in': self.id})

    @property
    def messages(self):
        return self.child_collection({'in': self.id})


class Label(NylasAPIObject):
    attrs = ["id", "display_name", "name", "object", "account_id"]
    collection_name = "labels"

    def __init__(self, api):
        NylasAPIObject.__init__(self, Label, api)

    @property
    def threads(self):
        return self.child_collection({'in': self.id})

    @property
    def messages(self):
        return self.child_collection({'in': self.id})


class Thread(NylasAPIObject):
    attrs = ["draft_ids", "id", "message_ids", "account_id", "object",
             "participants", "snippet", "subject", "subject_date",
             "last_message_timestamp", "first_message_timestamp",
             "unread", "starred", "version", "_folders", "_labels",
             "received_recent_date"]
    collection_name = 'threads'

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
            return [Folder.create(self.api, **f)
                    for f in self._folders]
        else:
            return []

    @property
    def labels(self):
        if self._labels:
            return [Label.create(self.api, **l)
                    for l in self._labels]
        else:
            return []

    def update_folder(self, folder_id):
        update = {'folder': folder_id}
        new_obj = self.api._update_resource(self.cls, self.id, update)
        for attr in self.cls.attrs:
            if hasattr(new_obj, attr):
                setattr(self, attr, getattr(new_obj, attr))
        return self.folder

    def update_labels(self, label_ids=[]):
        update = {'labels': label_ids}
        new_obj = self.api._update_resource(self.cls, self.id, update)
        for attr in self.cls.attrs:
            if hasattr(new_obj, attr):
                setattr(self, attr, getattr(new_obj, attr))
        return self.labels

    def add_labels(self, label_ids=[]):
        labels = [l.id for l in self.labels]
        labels = list(set(labels).union(set(label_ids)))
        return self.update_labels(labels)

    def add_label(self, label_id):
        return self.add_labels([label_id])

    def remove_labels(self, label_ids=[]):
        labels = [l.id for l in self.labels]
        labels = list(set(labels) - set(label_ids))
        return self.update_labels(labels)

    def remove_label(self, label_id):
        return self.remove_labels([label_id])

    def mark_as_seen(self):
        self.mark_as_read()

    def mark_as_read(self):
        update = {'unread': False}
        self.api._update_resource(self.cls, self.id, update)
        self.unread = False

    def mark_as_unread(self):
        update = {'unread': True}
        self.api._update_resource(self.cls, self.id, update)
        self.unread = True

    def star(self):
        update = {'starred': True}
        self.api._update_resource(self.cls, self.id, update)
        self.starred = True

    def unstar(self):
        update = {'starred': False}
        self.api._update_resource(self.cls, self.id, update)
        self.starred = False

    def create_reply(self):
        d = self.drafts.create()
        d.thread_id = self.id
        d.subject = self.subject
        return d

# This is a dummy class that allows us to use the create_resource function
# and pass in a 'Send' object that will translate into a 'send' endpoint.
class Send(Message):
    collection_name = 'send'

    def __init__(self, api):
        NylasAPIObject.__init__(self, Send, api)


class Draft(Message):
    attrs = ["bcc", "cc", "body", "date", "files", "from", "id",
             "account_id", "object", "subject", "thread_id", "to",
             "unread", "version", "file_ids", "reply_to_message_id",
             "reply_to", "starred", "snippet"]
    collection_name = 'drafts'

    def __init__(self, api, thread_id=None):
        Message.__init__(self, api)
        NylasAPIObject.__init__(self, Thread, api)
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
            data = {'draft_id': self.id}
            if hasattr(self, 'version'):
                data['version'] = self.version

        msg = self.api._create_resource(Send, data)
        if msg:
            return msg

    def delete(self):
        if self.id and self.version:
            data = {'version': self.version}
            self.api._delete_resource(self.cls, self.id, data=data)

class File(NylasAPIObject):
    attrs = ["content_type", "filename", "id", "content_id",
             "account_id", "object", "size", "message_ids", ]
    collection_name = 'files'

    def save(self):
        if hasattr(self, 'stream') and self.stream is not None:
            data = {self.filename: self.stream}
        elif hasattr(self, 'data') and self.data is not None:
            data = {self.filename: StringIO(self.data)}
        else:
            raise FileUploadError(message=("File object not properly "
                                               "formatted, must provide "
                                               "either a stream or data."))

        new_obj = self.api._create_resources(File, data)
        new_obj = new_obj[0]
        for attr in self.attrs:
            if hasattr(new_obj, attr):
                setattr(self, attr, getattr(new_obj, attr))

    def download(self):
        if not self.id:
            raise FileUploadError(message=("Can't download a file that "
                                               "hasn't been uploaded."))

        return self.api._get_resource_data(File, self.id,
                                           extra='download')

    def __init__(self, api):
        NylasAPIObject.__init__(self, File, api)


class Contact(NylasAPIObject):
    attrs = ["id", "account_id", "name", "email", "object"]
    collection_name = 'contacts'

    def __init__(self, api):
        NylasAPIObject.__init__(self, Contact, api)


class Calendar(NylasAPIObject):
    attrs = ["id", "account_id", "name", "description", "read_only", "object"]
    collection_name = 'calendars'

    def __init__(self, api):
        NylasAPIObject.__init__(self, Calendar, api)

    @property
    def events(self):
        return self.child_collection(Event, calendar_id=self.id)


class Event(NylasAPIObject):
    attrs = ["id", "account_id", "title", "description", "location",
             "read_only", "when", "busy", "participants", "calendar_id",
             "recurrence", "status", "master_event_id", "owner",
             "original_start_time", "object"]
    collection_name = 'events'

    def __init__(self, api):
        NylasAPIObject.__init__(self, Event, api)

    def as_json(self):
        dct = NylasAPIObject.as_json(self)
        # Filter some parameters we got from the API
        if 'when' in dct:
            if 'object' in dct['when']:
                del dct['when']['object']

        return dct


class Namespace(NylasAPIObject):
    attrs = ["account", "email_address", "id", "account_id", "object",
             "provider", "name", "organization_unit"]
    collection_name = 'n'

    def __init__(self, api):
        NylasAPIObject.__init__(self, Namespace, api)

    def child_collection(self, cls, **filters):
        return RestfulModelCollection(cls, self.api, self.id, **filters)


class Account(NylasAPIObject):
    api_root = 'a'

    attrs = ["account_id", "trial", "trial_expires", "sync_state",
             "billing_state", "account_id"]

    collection_name = 'accounts'

    def __init__(self, api):
        NylasAPIObject.__init__(self, Account, api)

    def as_json(self):
        dct = NylasAPIObject.as_json(self)
        return dct

    def upgrade(self):
        self.api._call_resource_method(self, self.account_id,
                                       'upgrade', None)

    def downgrade(self):
        self.api._call_resource_method(self, self.account_id,
                                       'downgrade', None)


class APIAccount(NylasAPIObject):
    attrs = ["email_address", "id", "account_id", "object",
             "provider", "name", "organization_unit"]

    collection_name = 'accounts'

    def __init__(self, api):
        NylasAPIObject.__init__(self, APIAccount, api)

    def as_json(self):
        dct = NylasAPIObject.as_json(self)
        return dct


class SingletonAccount(APIAccount):
    # This is an APIAccount that lives under /account.
    collection_name = 'account'
